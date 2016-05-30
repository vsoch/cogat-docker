from cognitive.apps.atlas.utils import color_by_relation, generate_uid, do_query
from py2neo import Path, Node as NeoNode, Relationship
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


    def create(self,name,properties=None,property_key="id"):
        '''create will create a new node of nodetype with unique id uid, and properties
        :param uid: the unique identifier
        :param name: the name of the node
        :param properties: a dictionary of properties with {field:value} for the node
        '''
        node = None
        uid = generate_uid(self.name) # creation also checks for existence of uid
        if graph.find_one(self.name,property_key='id',property_value=uid) == None:
            timestamp = graph.cypher.execute("RETURN timestamp()").one
            node = NeoNode(self.name, name=name,id=uid,creation_time=timestamp,last_updated=timestamp)
            graph.create(node)
            if properties != None:
                for property_name in properties.keys():
                    node.properties[property_name] = properties[property_name]
                node.push()
        return node


    def link(self,uid,endnode_id,relation_type,properties=None):
        '''link will create a new link (relation) from a uid to a relation, first confirming
        that the relation is valid for the node
        :param uid: the unique identifier for the source node
        :param endnode_id: the unique identifier for the end node
        :param relation_type: the relation type
        :param properties: properties to add to the relation
        '''
        startnode = graph.find_one(self.name,property_key='id',property_value=uid)
        endnode = graph.find_one(self.name,property_key='id',property_value=endnode_id)

        if startnode != None and endnode != None:

            # If the relation_type is allowed for the node type
            if relation_type in self.relations:
                if graph.match_one(start_node=startnode, rel_type=relation_type, end_node=endnode) == None:
                    relation = Relationship(startnode, relation_type, endnode)
                    graph.create(relation)
                    if properties != None:
                        for property_name in properties.keys():
                            relation.properties[property_name] = properties[property_name]
                        relation.push()
            return relation

    def update(self,uid,updates):
        '''update will update a particular field of a node with a new entry
        :param uid: the unique id of the node
        :param updates: a dictionary with {field:value} to update node with
        '''
        node = graph.find_one(self.name,'id', uid)
        if node!= None:
            for field,update in updates.items():
                node[field] = update
            node.push()


    def graph(self,uid,fields=None):
        '''graph returns a graph representation of one or more nodes, meaning a dictionary of nodes/links with
        (minimally) fields name, label, and id. Additional fields are included that are defined in the Node
        objects fields
        '''
        minimum_fields = ["name"]
        if fields == None:
            fields = self.fields
            new_fields = [x for x in fields if x not in minimum_fields]
            minimum_fields = minimum_fields + new_fields

        if isinstance(uid,str):
            uid = [uid]

        nodes = []
        links = []
        lookup = dict()
        count = 1
        for uu in uid:
            entity = self.get(uu)[0]      

            # Entity node
            if entity["id"] not in lookup:
                lookup[entity["id"]] = count
                count+=1

            node = {field:entity[field] for field in minimum_fields if field in entity}
            node["label"] = "%s: %s" %(self.name,entity["name"])
            node["color"] = self.color
            node["id"] = lookup[entity["id"]]
            nodes.append(node)

            # Relations
            if "relations" in entity:
                for relation_name,relations in entity["relations"].items():
                    for relation in relations:
                        if relation["id"] not in lookup:
                            lookup[relation["id"]] = count
                            count+=1

                        node = {field:relation[field] for field in minimum_fields if field in relation}
                        node["label"] = "%s: %s" %(relation_name,relation["name"])
                        node["id"] = lookup[relation["id"]]
                        node["color"] = color_by_relation(relation_name)
                        link = {"source":lookup[entity["id"]],"target":lookup[relation["id"]],"type":relation_name}
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
        self.fields = ["id","name","classification","definition"]
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
        self.fields = ["id","name","description"]
        self.color = "#BE0000" # dark red


# General search function across nodes
def search(searchstring,fields=["name","id"]):
    if isinstance(fields,str):
        fields = [fields]
    return_fields = ",".join(["n.%s" %x for x in fields])
    query = '''MATCH (n) WHERE str(n.name) =~ '(?i).*%s.*' RETURN %s;''' %(searchstring,return_fields)
    return do_query(query,fields=fields)
