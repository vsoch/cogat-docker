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
        :param relations: list of relations to include. If not defined, will use default for task
        '''
        if get_relations == True:
            if relations == None:
                relations = self.relations
        parents = graph.find(self.name, field, uid)
        nodes = []
        for parent in parents:
            new_node = {}
            new_node.update(parent.properties)

            if relations != None and get_relations == True:
                relation_nodes = []
                new_relations = graph.match(parent)
                for new_relation in new_relations:
                    new_relation_node = {}
                    new_relation_node.update(new_relation.end_node.properties)
                    new_relation_node["relationship_type"] = new_relation.type
                    relation_nodes.append(new_relation_node)
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


class Task(Node):

    def __init__(self):
        self.name = "task"
        self.fields = ["id","name","definition"]
        self.relations = ["HASCONDITION","ASSERTS","HASCONTRAST"]    


class Disorder(Node):

    def __init__(self):
        self.name = "disorder"
        self.fields = ["id","name","classification"]

class Condition(Node):

    def __init__(self):
        self.name = "condition"
        self.fields = ["id","name","description"]


class Contrast(Node):

    def __init__(self):
        self.name = "contrast"
        self.fields = ["id","name","description"]


class Battery(Node):

    def __init__(self):
        self.name = "battery"
        self.fields = ["id","name","collection"]


class Theory(Node):

    def __init__(self):
        self.name = "theory"
        self.fields = ["id","name"]


# Query helper functions

def do_query(query,fields,output_format="dict"):
    '''do_query will return the result of a cypher query in the format specified (default is dict)
    :param query: string of cypher query
    :param output_format: desired output format. Default is "dict"
    '''
    result = graph.cypher.execute(query)
    df = pandas.DataFrame(result.records, columns=result.columns)
    df.columns = fields
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
