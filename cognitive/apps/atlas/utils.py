from django.utils.crypto import get_random_string
from py2neo import Path, Node, Relationship
from cognitive.settings import graph
import pandas


def generate_uid(node_type):
    '''generte_uid will generate a unique identifier for a new node, with first three letters
    dependent on the term type
    :param node_type: one of concept, battery, condition, etc.
    '''
    nodetypes = {"concept":"trm",
                 "task":"tsk",
                 "theory":"thc",
                 "contrast":"cnt",
                 "battery":"tco",
                 "disorder":"dso",
                 "collection":"tco",
                 "condition":"con"}

    # generate new node uid that doesn't exist
    result = " "
    while len(result) > 0:
        suffix = get_random_string(13)
        uid = "%s_%s" %(nodetypes[node_type],suffix)    
        query = """start n=node(*)
                   match n
                   where n.id = '%s'
                   return n.id""" %(uid)
        result = do_query(query,fields=["n.id"])
    return uid    


def add_update(field,value,updates=None):
    '''add_update will update the updates dictionary only given that a value is defined (not None or '') for a field
    :param field: the name of the field to update
    :param value: the value to update with
    :param updates: the dictionary to update (optional)
    '''
    if updates == None:
        updates = dict()
    if value not in ["",None]:
        updates[field] = value
    return updates

def clean_html(html,replacements=None):
    '''clean_html will replace newlines with <br> for rendering, along with \r characters
    :param html: the html to clean
    :param replacements: additional list of paired lists eg [["string","replace"]...] (optional)
    '''
    replace_sets = [["\n","<br>"],["\r",""]]

    if replacements != None:
        replace_sets = replace_sets + replacements
    
    for replace_set in replace_sets:
        text = replace_set[0]
        replacement = replace_set[1]
        html = html.replace(text,replacement)
    return html


def update_lookup(lookup,key,entry):
    '''update_lookup will update a lookup dictionary with an entry. If the key exists, the entry is appended to 
    the existing list. if not, it is added.
    :param lookup: dictionary to update
    :param entry: the entry to add to the list
    '''
    if key in lookup:
        lookup[key].append(entry)
    else:
        lookup[key] = [entry]
    return lookup

def color_by_relation(relation_name):
    '''color_by_relation returns node color based on relation type
    :param relation_name: the name of the relation to look up color for
    '''
    colors = {"ASSERTS":"#3C7263", # task --asserts--> concept
              "MEASUREDBY": "#D89013", # concept --measuredby--> contrast
              "DERIVEDFROM": "#63506D", # task --derivedfrom--> task
              "HASCONDITION":"#BC1079", # contrast --hascondition--> condition
              "HASCONTRAST": "#D89013", # condition --hascontrast--> contrast
              "PARTOF":"#3C7263",  # concept
              "KINDOF":"#3C7263"}  # concept

    if relation_name in colors:
        return colors[relation_name]
    return "#FFFFFF"

# Query helper functions #########################################################################

def do_query(query,fields,output_format="dict",drop_duplicates=True):
    '''do_query will return the result of a cypher query in the format specified (default is dict)
    :param query: string of cypher query
    :param output_format: desired output format. Default is "dict"
    '''
    if isinstance(fields,str):
        fields = [fields]
    result = graph.cypher.execute(query)
    df = pandas.DataFrame(result.records, columns=result.columns)
    df.columns = fields
    if drop_duplicates == True:
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
