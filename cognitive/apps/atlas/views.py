from cognitive.apps.atlas.query import Concept, Task, Disorder, Contrast, Battery, Theory
from django.shortcuts import render
from django.template import loader

Concept = Concept()
Task = Task()
Disorder = Disorder()
Contrast = Contrast()
Battery = Battery()
Theory = Theory()

# Needed on all pages
counts = {"disorders":Disorder.count(),
          "tasks":Task.count(),
          "contrasts":Contrast.count(),
          "concepts":Concept.count(),
          "batteries":Battery.count(),
          "theories":Theory.count()}

# VIEWS FOR ALL NODES #############################################################

def all_nodes(request,nodes,node_type):
    '''all_nodes returns view with all nodes for node_type'''

    appname = "The Cognitive Atlas"
    context = {'appname': appname,
               'term_type':node_type[:-1],
               'nodes':nodes,
               'filtered_nodes_count':counts[node_type],
               'counts':counts}

    return render(request,"atlas/all_terms.html",context)

def all_concepts(request):
    '''all_concepts returns page with list of all concepts'''

    concepts = Concept.all(order_by="name")
    return all_nodes(request,concepts,"concepts")
    
def all_tasks(request):
    '''all_tasks returns page with list of all tasks'''

    tasks = Task.all(order_by="name")
    return all_nodes(request,tasks,"tasks")    

def all_batteries(request):
    '''all_collections returns page with list of all collections'''

    batteries = Battery.all(order_by="name")
    return all_nodes(request,tasks,"batteries")    


def all_theories(request):
    '''all_collections returns page with list of all collections'''

    theories = Theory.all(order_by="name")
    return all_nodes(request,theories,"theories")    

def all_disorders(request):
    '''all_disorders returns page with list of all disorders'''

    disorders = Disorder.all(order_by="name")    
    for d in range(len(disorders)):
        disorder = disorders[d]
        if disorder["classification"] == None:
            disorder["classification"] = "None"
            disorders[d] = disorder

    context = {'appname': "The Cognitive Atlas",
               'active':"disorders",
               'nodes':disorders,
               'counts':counts}

    return render(request,"atlas/all_disorders.html",context)

def all_contrasts(request):
    '''all_contrasts returns page with list of all contrasts'''

    contrasts = Contrast.all(order_by="name",fields=fields)
    return all_nodes(request,contrasts,counts["contrasts"],"contasts")    


# VIEWS BY LETTER #############################################################

def nodes_by_letter(request,letter,nodes,nodes_count,node_type):
    '''nodes_by_letter returns node view for a certain letter'''

    appname = "The Cognitive Atlas"
    context = {'appname': appname,
               'nodes':nodes,
               'letter':letter,
               'term_type':node_type[:-1],
               'filtered_nodes_count':nodes_count,
               'counts':counts}

    return render(request,"atlas/terms_by_letter.html",context)

def concepts_by_letter(request,letter):
    '''concepts_by_letter returns concept view for a certain letter'''
    concepts = Concept.filter(filters=[("name","starts_with",letter)])
    concepts_count = len(concepts)
    return nodes_by_letter(request,letter,concepts,concepts_count,"concepts")

def tasks_by_letter(request,letter):
    '''tasks_by_letter returns task view for a certain letter'''
    tasks = Task.filter(filters=[("name","starts_with",letter)])
    tasks_count = len(tasks)
    return nodes_by_letter(request,letter,tasks,tasks_count,"tasks")


# VIEWS FOR SINGLE NODES ##########################################################

def view_concept(request,uid):
    concept = Concept.get(uid)
    context = {"concept":concept}
    return render(request,'atlas/view_concept.html',context)


def view_task(request,uid):
    return render(request,'atlas/view_task.html',context)


def view_contrast(request,uid):
    return render(request,'atlas/view_contrast.html',context)


def view_battery(request,uid):
    return render(request,'atlas/view_battery.html',context)


def view_theory(request,uid):
    return render(request,'atlas/view_theory.html',context)


def view_disorder(request,uid):
    return render(request,'atlas/view_disorder.html',context)


def view_theory(request,uid):
    return render(request,'atlas/view_theory.html',context)


# ADD NEW TERMS ###################################################################

def contribute_term(request):
    # Get form data from post, check if term exist,
    # if term exists, define already_exists, and add to context
    term_name = "hello!"
    message = "message"

    context = {"message":message,
              "term_name":term_name}
    
    if 1==1:
        context["already_exists"] = "anything"

    return render(request,'atlas/contribute_term.html',context)

def contribute_disorder(request):

    return render(request,'atlas/contribute_disorder.html',context)
