from cognitive.settings import graph
import pandas

class Node:

    def __init__(self,name,fields=["id","name"]):
        '''Node is a general class to represent a neo4j node
        '''
        self.name = name
        self.fields = fields

    def count(self):
        '''count returns the count :) I am ze-count! One two three...! one two... three! 
        '''
        query = "MATCH (n:%s) RETURN count(*)" %self.name
        return graph.cypher.execute(query).one


    def graph(self,uid,fields=None):
        '''graph returns a graph representation of one or more nodes, meaning a dictionary of nodes/links with
        (minimally) fields name, label, and id. Additional fields are included that are defined in the Node
        objects fields
        '''
        minimum_fields = ["name","id"]
        if fields == None:
            fields = self.fields
            new_fields = [x for x in fields if x not in minimum_fields]
            minimum_fields = minimum_fields + new_fields

        if isinstance(uid,str):
            uid = [uid]

        nodes = []
        links = []
        for uu in uid:
            entity = self.get(uu)[0]      

            # Entity node
            node = {field:entity[field] for field in minimum_fields if field in entity}
            node["label"] = "%s: %s" %(self.name,entity["name"])
            node["color"] = self.color
            nodes.append(node)

            # Relations
            if "relations" in entity:
                for relation_name,relations in entity["relations"].items():
                    for relation in relations:
                        node = {field:relation[field] for field in minimum_fields if field in relation}
                        node["label"] = "%s: %s" %(relation_name,relation["name"])
                        link = {"source":entity["id"],"target":relation["id"],"type":relation_name}
                        links.append(link)
                        nodes.append(node)

        result = {"nodes":nodes,"links":links}
        return result


    def filter(self,filters,format="dict",fields=None):
        '''filter will filter a node based on some set of filters
        :param filters: a list of tuples with [(field,filter,value)], eg [("name","starts_with","a")]. 
        ::note_ 
       
             Currently supported filters are "starts_with"
        '''
        if fields == None:
            fields = self.fields
        return_fields = ",".join(["n.%s" %(x) for x in fields])

        query = "MATCH (n:%s)" %self.name
        for tup in filters:
            filter_field,filter_name,filter_value = tup
            if filter_name == "starts_with":
                query = "%s WHERE n.%s =~ '(?i)%s.*'" %(query,filter_field,filter_value)
        query = "%s RETURN %s" %(query,return_fields)
        return do_query(query,output_format=format,fields=fields)


    def all(self,fields=None,limit=None,format="dict",order_by=None,desc=False):
        '''all returns all concepts, or up to a limit
        :param fields: select a subset of fields to return, default None returns all fields
        :param limit: return N=limit concepts only (default None)
        :param format: return format, either "df" "list" or dict (default)
        :param order_by: order the results by a particular field
        :param desc: if order by is not None, do descending (default True) 
        '''
        if fields == None:
           fields = self.fields

        return_fields = ",".join(["n.%s" %(x) for x in fields])
        query = "MATCH (n:%s) RETURN %s" %(self.name,return_fields)

        if order_by != None:
            query = "%s ORDER BY n.%s" %(query,order_by)      
            if desc==True:
                query = "%s desc" %(query)

        if limit != None:
            query = "%s LIMIT %s" %(query,limit) 

        return do_query(query,fields=fields,output_format=format)

    def get(self,uid,field="id",get_relations=True,relations=None):
        '''get returns one or more nodes based on a field of interest. If get_relations is true, will also return
        the default relations for the node, or those defined in the relations variable
        :param params: list of parameters to search for, eg [trm_123]
        :param field: field to search (default id)
        :param get_relations: default True, return relationships
        :param relations: list of relations to include. If not defined, will return all
        '''
        parents = graph.find(self.name, field, uid)
        nodes = []
        for parent in parents:
            new_node = {}
            new_node.update(parent.properties)

            if get_relations == True:
                relation_nodes = dict()
                new_relations = graph.match(parent)
                for new_relation in new_relations:
                    new_relation_node = {}
                    new_relation_node.update(new_relation.end_node.properties)
                    new_relation_node["relationship_type"] = new_relation.type
                    if new_relation.type in relation_nodes:
                        relation_nodes[new_relation.type].append(new_relation_node)
                    else:
                        relation_nodes[new_relation.type] = [new_relation_node]

                # Does the user want a filtered set?
                if relations != None:
                    relation_nodes = {k:v for k,v in relation_nodes.iteritems() if k in relations}
                new_node["relations"] = relation_nodes

            nodes.append(new_node)            

        return nodes
        
       
    def search_all_fields(self, params):
        if isinstance(params,str):
            params = [params]
        return_fields = ",".join(["c.%s" %(x) for x in self.fields])
        query = "MATCH (c:%s) WHERE c.{0} =~ '(?i).*{1}.*$' RETURN %s;" %(self.name,return_fields)
        queries = []
        for field in self.fields:
            for param in params:
               queries.append(query.format(field, param))
        
        # Combine queries into transaction
        tx = graph.cypher.begin()

        for query in queries:
            tx.append(query)

        # Return as pandas data frame
        results = tx.commit()
        if not results or sum(len(res) for res in results) == 0:
            return {}
        
        df = pandas.DataFrame(columns=self.fields)
        i = 0
        for result in results:
            for record in result.records:
                attr_values = []
                for field in self.fields:
                    attr_name = "c.%s" %(field)
                    attr_values.append(getattr(record, attr_name, ""))
                df.loc[i] = attr_values
                i += 1
        return df.to_dict(orient="records")


# Each type of Cognitive Atlas Class extends Node class

class Concept(Node):

    def __init__(self):
        self.name = "concept"
        self.fields = ["id","name","definition"]
        self.relations = ["PARTOF","KINDOF"]
        self.color = "#3C7263" # sea green

class Task(Node):

    def __init__(self):
        self.name = "task"
        self.fields = ["id","name","definition"]
        self.relations = ["HASCONDITION","ASSERTS","HASCONTRAST"]    
        self.color = "#63506D" #purple

    def get_contrasts(self,task_id):
        '''get_contrasts looks up the contrasts(s) associated with a task, along with concepts
        :param task_id: the task unique id (trm|tsk_*) for the task
        '''
        
        fields = ["concept.id","concept.creation_time","concept.name","concept.last_updated","concept.definition",
                  "contrast.id","contrast.creation_time","contrast.name","contrast.last_updated"]

        return_fields = ",".join(fields)
        query = '''MATCH (t:task)-[:HASCONDITION]->(c:condition) 
                   WHERE t.id='%s'
                   WITH c as condition
                   MATCH (condition)-[:HASCONTRAST]->(con:contrast) 
                   WITH con as contrast
                   MATCH (c:concept)-[:MEASUREDBY]->(contrast)
                   WITH c as concept, contrast
                   RETURN %s''' %(task_id,return_fields)

        fields = [x.replace(".","_") for x in fields]
        
        return do_query(query,fields=fields)
            


class Disorder(Node):

    def __init__(self):
        self.name = "disorder"
        self.fields = ["id","name","classification"]
        self.color = "#337AB7" # neurovault blue

class Condition(Node):

    def __init__(self):
        self.name = "condition"
        self.fields = ["id","name","description"]
        self.color = "#BC1079" # dark pink

class Contrast(Node):
    def __init__(self):
        self.name = "contrast"
        self.fields = ["id","name","description"]
        self.color = "#D89013" #gold

    def get_conditions(self,contrast_id,fields=None):
        '''get_conditions returns conditions associated with a contrast
        :param contrast_id: the contrast unique id (cnt) for the task
        :param fields: condition fields to return
        '''

        if fields == None:
            fields = ["condition.creation_time","condition.id",
                      "condition.last_updated","condition.name"]

        return_fields = ",".join(fields)
        query = '''MATCH (cond:condition)-[:HASCONTRAST]->(c:contrast) 
                   WHERE c.id='%s'
                   WITH cond as condition
                   RETURN %s''' %(contrast_id,return_fields)

        fields = [x.replace(".","_") for x in fields]
        
        return do_query(query,fields=fields)



    def get_tasks(self,contrast_id,fields=None):
        '''get_task looks up the task(s) associated with a contrast
        :param contrast_id: the contrast unique id (cnt) for the task
        :param fields: task fields to return
        '''
        if fields == None:
            fields = ["creation_time","definition","id","last_updated","name"]
        
        # task --> [hascondition] --> condition
        # condition -> [hascontrast] -> contrast

        return_fields = ",".join(["task.%s" %f for f in fields])
        query = '''MATCH (c:concept)-[:MEASUREDBY]->(co:contrast) 
                   WHERE co.id='%s' WITH co as contrast 
                   MATCH (c:condition)-[:HASCONTRAST]->(contrast) WITH c as condition 
                   MATCH (t:task)-[:HASCONDITION]->(condition) 
                   WITH DISTINCT t as task
                   RETURN %s''' %(contrast_id,return_fields)

        return do_query(query,fields=fields)
        

class Battery(Node):

    def __init__(self):
        self.name = "battery"
        self.fields = ["id","name","collection"]
        self.color = "#4BBE00" # bright green

class Theory(Node):

    def __init__(self):
        self.name = "theory"
        self.fields = ["id","name"]
        self.color = "#BE0000" # dark red


# Query helper functions

def do_query(query,fields,output_format="dict"):
    '''do_query will return the result of a cypher query in the format specified (default is dict)
    :param query: string of cypher query
    :param output_format: desired output format. Default is "dict"
    '''
    result = graph.cypher.execute(query)
    df = pandas.DataFrame(result.records, columns=result.columns)
    df.columns = fields
    df = df.drop_duplicates()
    if output_format == "df":
        return df
    elif output_format == "list":
        return df.values.tolist()
    elif output_format == "dict":
        return df.to_dict(orient="records")

def do_transaction(tx=None,query=None,params=None):
    '''do_transaction will return the result of a cypher transaction in the format specified (default is dict). If a transaction object is not supplied, query must be defined, and the function will call get_transactions first. If tx is defined and query is also defined, the query will be added to the transaction before running it.
    :param tx: string of cypher query (optional) if provided, will first call get_transactions to 
    :param query: string of cypher query (optional) if provided, will first call get_transactions to 
    :param params: a list of dictionaries, each dictionary with keys as values to sub in the query, and values as the thing to substitute. Eg: [{"A":name,"B":classification}]
    '''
    if tx == None and query == None:
        print("Please define either transaction or query.")
        return None
    if query != None:
        tx = get_transactions(query,tx=tx,params=params)
    # Return as pandas data frame
    results = tx.commit()
    if not results or sum(len(res) for res in results) == 0:
        return None
    # Return as pandas Data Frame
    column_names = [x.split(".")[-1] for x in results[0].columns]
    df = pandas.DataFrame(columns=column_names)
    for r in range(len(results)):       
        df.loc[r] = [x for x in results[r].one]
    return df


# General search function across nodes
def search(searchstring,fields="name"):
    if isinstance(fields,str):
        fields = [fields]
    return_fields = ",".join(["n.%s" %x for x in fields])
    query = '''MATCH (n) WHERE str(n.name) =~ '(?i).*%s.*' RETURN %s;''' %(searchstring,return_fields)
    return do_query(query,fields=fields)


def get_transactions(query,tx=None,params=None):
    '''get_transactions will append new transactions to a transaction object, or return a new transaction if one does not exist. 
    :param query: string of cypher query
    :param tx: a transaction object (optional)
    :param params: a list of dictionaries, each dictionary with keys as values to sub in the query, and values as the thing to substitute. Eg: [{"A":name,"B":classification}]
    '''
    # Combine queries into transaction
    if tx == None:
       tx = graph.cypher.begin()
    if params:
        for param in params:
            tx.append(query, param)
    else:
        tx.append(query)
    return tx
