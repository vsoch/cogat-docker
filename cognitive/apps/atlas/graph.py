from cognitive.apps.atlas.query import Task, Concept, Condition, Contrast
from cognitive.apps.atlas.utils import merge_cypher
from django.http import JsonResponse, HttpResponse
from django.template import loader,Context
from django.shortcuts import render
import csv

Task = Task()
Concept = Concept()
Condition = Condition()
Contrast = Contrast()

# Return full graph visualizations

def task_graph(request,uid):
    nodes = Task.graph(uid)
    context = {"graph":nodes}
    return render(request,"graph/task.html",context)

def concept_graph(request,uid):
    nodes = Concept.graph(uid)
    context = {"graph":nodes}
    return render(request,"graph/task.html",context)

def explore_graph(request):
    context = {}
    return render(request,"graph/explore.html",context)


# Return just json
def task_json(request,uid):
    nodes = Task.graph(uid)
    return JsonResponse(nodes)

def concept_json(request,uid):
    nodes = Concept.graph(uid)
    return JsonResponse(nodes)

# GRAPH GIST ######################################################################
# These are export functions for concepts, tasks, etc to be previewed as graph gists
    
def contrast_gist(request,uid,query=None,return_gist=False):
    '''contrast_gist is currently a sub for some "view_contrast" view (that should
    be defined as views.view_contrast, as a simple graph seems more appropriate 
    to show a contrast and its conditions than some static thing we would render!
    :param uid: the uid for the contrast
    :param query: a custom query. If not defined, will show a table of concepts asserted.
    :param return_gist: if True, will return the context with all needed variables
    '''
    contrast_cypher,lookup = Contrast.cypher(uid,return_lookup=True)
    contrast_cypher = add_cypher_relations(contrast_cypher,lookup)

    contrast = Contrast.get(uid)[0]
    if query == None:
        query = "MATCH (c:condition)-[r:HASCONTRAST]->(con:contrast) WHERE con.id='%s' RETURN c.name as condition_name,con.name as contrast_name;" %(uid)

    # Join by newline
    contrast_cypher["links"] = "\n".join(contrast_cypher["links"])
    contrast_cypher["nodes"] = "\n".join(contrast_cypher["nodes"])

    context = {"relations":contrast_cypher["links"],
               "nodes":contrast_cypher["nodes"],
               "node_type":"contrast",
               "node_name":contrast["name"],
               "query":query}
    if return_gist == True:
        return context
    return render(request,'graph/gist.html',context)
    

# Eg, This is the URL that can be linked to from a page
# http://portal.graphgist.org/graph_gists/by_url?url=hello
def task_gist(request,uid,query=None,return_gist=False):
    '''task_gist will return a cypher gist for a task, including nodes and relations
    :param uid: the uid for the task
    :param query: a custom query. If not defined, will show a table of concepts asserted.
    :param return_gist: if True, will return the context with all needed variables
    '''    
    task_cypher,lookup = Task.cypher(uid,return_lookup=True)
    task_cypher = add_cypher_relations(task_cypher,lookup)

    task = Task.get(uid)[0]
    if query == None:
        query = "MATCH (t:task)-[r:ASSERTS]->(c:concept) RETURN t.name as task_name,c.name as concept_name;"

    # Join by newline
    task_cypher["links"] = "\n".join(task_cypher["links"])
    task_cypher["nodes"] = "\n".join(task_cypher["nodes"])

    context = {"relations":task_cypher["links"],
               "nodes":task_cypher["nodes"],
               "node_type":"task",
               "node_name":task["name"],
               "query":query}
    if return_gist == True:
        return context
    return render(request,'graph/gist.html',context)

def download_task_gist(request,uid,query=None):
    '''download_task_gist generates the equivalent task gist, but instead downloads 
    it as a .gist file for the user to save locally
    :param uid: the uid for the task
    :param query: a custom query. If not defined, will show a table of concepts asserted.
    '''    
    context = task_gist(request,uid,query,return_gist=True)
    
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="cogat_%s.gist"' %(uid)

    t = loader.get_template('graph/gist.html')
    c = Context(context)
    response.write(t.render(c))
    return response

# Note: may need to this: https://docs.djangoproject.com/en/1.9/howto/outputting-csv/

## Additional Graph Functions

def add_cypher_relations(cypher,lookup):
    '''add_cypher_relations will look up relations for connected nodes returned from an object. This is akin to
    adding one layer of the tree to the graph (and the function could be modified to add more)
    :param cypher: the cypher object, a dictionary with nodes and links as keys, each a list of them.
    '''
    node_types = list(lookup)
    for node_type in node_types:
        for term in lookup[node_type]:
            if node_type == "condition":
                new_cypher,lookup = Condition.cypher(term,lookup=lookup,return_lookup=True)
            elif node_type == "task":
                new_cypher,lookup = Task.cypher(term,lookup=lookup,return_lookup=True)
            elif node_type == "contrast":
                new_cypher,lookup = Contrast.cypher(term,lookup=lookup,return_lookup=True)
            elif node_type == "concept":
                new_cypher,lookup = Concept.cypher(term,lookup=lookup,return_lookup=True)
            cypher = merge_cypher(cypher,new_cypher)
    return cypher
