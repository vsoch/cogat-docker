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


    def all(self,fields=None,limit=None,format="dict",order_by=None,desc=True):
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

    def get(self,params,field="id"):
        '''get returns one or more nodes based on a field of interest
        :param params: list of parameters to search for, eg [trm_123]
        :param field: field to search (default id)
        '''
        if isinstance(params,str):
            params = [params]

        return_fields = ",".join(["c.%s" %(x) for x in self.fields])
        query = 'MATCH (c:%s) WHERE c.%s = {A} RETURN %s;' %(self.name,field,return_fields)

        # Combine queries into transaction
        tx = graph.cypher.begin()

        for param in params:
            tx.append(query, {"A": param})

        # Return as pandas data frame
        results = tx.commit()
        df = pandas.DataFrame(columns=self.fields)
        df.columns = self.fields
        for r in range(len(results)):       
            df.loc[r] = [x for x in results[r].one]
        return df



# Each type of Cognitive Atlas Class extends Node class

class Concept(Node):

    def __init__(self):
        self.name = "concept"
        self.fields = ["id","name","definition"]
            

class Task(Node):

    def __init__(self):
        self.name = "task"
        self.fields = ["id","name","definition"]


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
