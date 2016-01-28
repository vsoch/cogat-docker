from cognitive.apps.atlas.query import Concept, Task, Disorder, Contrast
from django.shortcuts import render
from django.template import loader

Concept = Concept()
Task = Task()
Disorder = Disorder()
Contrast = Contrast()

# VIEWS FOR ALL NODES #############################################################

def all_nodes(request,nodes,node_count,node_type):
    '''all_nodes returns view with all nodes for node_type'''

    template = "atlas/all_%s.html" %node_type
    appname = "The Cognitive Atlas"
    context = {'appname': appname,
               'active':node_type,
               'nodes',nodes,
               'concepts_count':node_count}

    return render(request,template,context)

def all_concepts(request):
    '''all_concepts returns page with list of all concepts'''

    concepts = Concept.all(limit=10,order_by="last_updated")
    concepts_count = Concept.count()
    return all_nodes(request,concepts,concepts_count,"concepts")
    
def all_tasks(request):
    '''all_tasks returns page with list of all tasks'''

    tasks = Task.all(limit=10,order_by="last_updated",fields=fields)
    tasks_count = Task.count()
    return all_nodes(request,tasks,tasks_count,"tasks")    

def all_disorders(request):
    '''all_disorders returns page with list of all disorders'''

    disorders = Disorder.all(limit=10,order_by="last_updated",fields=fields)
    disorders_count = Disorder.count()
    return all_nodes(request,disorders,disorders_count,"disorders")

def all_contrasts(request):
    '''all_contrasts returns page with list of all contrasts'''

    contrasts = Contrast.all(limit=7,order_by="last_updated",fields=fields)
    contrasts_count = Contrast.count()
    return all_nodes(request,contrasts,contrasts_count,"concepts")    


# VIEWS BY LETTER #############################################################

def nodes_by_letter(request,letter,nodes,node_count,node_type):
    '''nodes_by_letter returns node view for a certain letter'''

    template = "atlas/%s_by_letter.html" %(node_type)
    appname = "The Cognitive Atlas"
    context = {'appname': appname,
               'active':node_type,
               'nodes',nodes,
               'letter':letter,
               'nodes_count':nodes_count}

    return render(request,template,context)

def concepts_by_letter(request,letter):
    '''concepts_by_letter returns concept view for a certain letter'''
    concepts = Concept.filter(filter=[("name","starts_with",letter)])
    concepts_count = Concept.count()
    return nodes_by_letter(request,letter,concepts,concepts_count,"concepts")

def tasks_by_letter(request,letter):
    '''tasks_by_letter returns task view for a certain letter'''
    tasks = Task.filter(filter=[("name","starts_with",letter)])
    tasks_count = Task.count()
    return nodes_by_letter(request,letter,tasks,tasks_count,"tasks")


# VIEWS FOR SINGLE NODES ##########################################################
