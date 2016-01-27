from cognitive.settings import graph
import pandas

class Node:

    def __init__(self,name,fields=["id","name"]):
        '''Node is a general class to represent a neo4j node
        '''
        self.name = name
        self.fields = fields



    def all(self,limit=None,format="df",order_by=None,desc=True):
        '''all returns all concepts, or up to a limit
        :param limit: return N=limit concepts only (default None)
        :param order_by: order the results by a particular field
        :param desc: if order by is not None, do descending (default True) 
        '''
        query = "MATCH (n:%s) RETURN n.id,n.name" %self.name

        if order_by != None:
            query = "%s ORDER BY n.%s" %(query,order_by)      
            if desc==True:
                query = "%s desc" %(query)

        if limit != None:
            query = "%s LIMIT %s" %(query,limit) 

        result = graph.cypher.execute(query)
        df = pandas.DataFrame(result.records, columns=result.columns)
        if format == "df":
            return df
        else:
            return map(tuple,df.values)


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
        for r in range(len(results)):       
            df.loc[r] = [x for x in results[r].one]
        return df



# Each type of Cognitive Atlas Class extends Node class

class Concept(Node):

    def __init__(self):
        self.name = "concept"
        self.fields = ["id","name"]
            

class Task(Node):

    def __init__(self):
        self.name = "task"
        self.fields = ["id","name"]
