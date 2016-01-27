from cognitive.settings import graph
import pandas

class Node:

    def __init__(self,name,fields=["id","name"]):
        '''Node is a general class to represent a neo4j node'''
        self.name = name
        self.fields = fields


    def __import__(self):
        print "imported!"

    def all(self,limit=None):
        '''all returns all concepts, or up to a limit
        :param limit: return N=limit concepts only (default None)
        '''
        if limit != None:
            query = "MATCH (n:%s) RETURN n LIMIT %s" %(self.name,limit) 
        else:
            query = "MATCH (n:%s) RETURN n.id,n.name" %(self.name) 
        result = graph.cypher.execute(query)
        return pandas.DataFrame(result.records, columns=result.columns)


    def get(self,params,field="id"):
        '''get returns one or more nodes based on a field of interest
        :param params: list of parameters to search for, eg [trm_123]
        :param field: field to search (default id)
        '''
        if isinstance(params,str):
            params = [params]

        df = pandas.DataFrame(columns=self.fields)
        return_fields = ",".join(["c.%s" %(x) for x in self.fields])
        query = 'MATCH (c:%s) WHERE c.%s = {A} RETURN %s;' %(self.name,field,return_fields)
        tx = graph.cypher.begin()
        for param in params:
            tx.append(query, {"A": param})
        results = tx.commit()
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
