from cognitive.apps.atlas.query import Concept, Task, Disorder, Contrast, Battery, Theory, search
from cognitive.apps.atlas.utils import clean_html, update_lookup, add_update
from django.shortcuts import render
from django.template import loader
import numpy

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
    concept = Concept.get(uid)[0]

    # For each measured by (contrast), get the task
    if "MEASUREDBY" in concept["relations"]:
        for c in range(len(concept["relations"]["MEASUREDBY"])):
            contrast = concept["relations"]["MEASUREDBY"][c]
            tasks = Contrast.get_tasks(contrast["id"])
            concept["relations"]["MEASUREDBY"][c]["tasks"] = tasks

    context = {"concept":concept}

    return render(request,'atlas/view_concept.html',context)


def view_task(request,uid):
    task = Task.get(uid)[0]
 
    # Replace newlines with <br>, etc.
    task["definition"] = clean_html(task["definition"])
    contrasts = Task.get_contrasts(task["id"])

    # Make a lookup dictionary based on concept id
    concept_lookup = dict()
    contrast_lookup = dict()
    for contrast in contrasts:
        concept_lookup = update_lookup(concept_lookup,contrast["concept_id"],contrast)
        contrast_lookup = update_lookup(contrast_lookup,contrast["contrast_id"],contrast)

    # If we want association of conditions with contrasts
    #conditions = {x:Contrast.get_conditions(x) for x in list(contrast_lookup.keys())}
    conditions = dict()
    for contrast_id in list(contrast_lookup.keys()):
        new_conditions = Contrast.get_conditions(contrast_id)
        for new_condition in new_conditions:
            if new_condition["condition_id"] not in conditions:
                conditions[new_condition["condition_id"]] = new_condition

    context = {"task":task,
               "concepts":concept_lookup,
               "contrasts":contrast_lookup,
               "conditions":conditions}

    return render(request,'atlas/view_task.html',context)


def view_contrast(request,uid):
    return render(request,'atlas/view_contrast.html',context)


def view_battery(request,uid):
    return render(request,'atlas/view_battery.html',context)


def view_theory(request,uid):
    return render(request,'atlas/view_theory.html',context)


def view_disorder(request,uid):
    disorder = Disorder.get(uid)[0]
    context = {"disorder":disorder}
    return render(request,'atlas/view_disorder.html',context)


def view_theory(request,uid):
    return render(request,'atlas/view_theory.html',context)


# ADD NEW TERMS ###################################################################

def contribute_term(request):
    '''contribute_term will return the contribution detail page for a term that is
    posted, or visiting the page without a POST will return the original form
    '''

    context = {"message":"Please specify the term you want to contribute."}

    if request.method == "POST":      
        term_name = request.POST.get('newterm', '')

        # Does the term exist in the atlas?
        results = search(term_name)   
        matches = [x["name"] for x in results if x["name"]==term_name]
        message = "Please further define %s" %(term_name)

        if len(matches) > 0:
            message = "Term %s already exists in the Cognitive Atlas." %(term_name)
            context["already_exists"] = "anything"

        context["message"] = message
        context["term_name"] = term_name
        context["other_terms"] = results

    return render(request,'atlas/contribute_term.html',context)


def add_term(request):
    '''add_term will add a new term to the atlas
    '''

    if request.method == "POST":
        term_type = request.POST.get('term_type', '')
        term_name = request.POST.get('term_name', '')
        definition_text = request.POST.get('definition_text', '')

        properties = None
        if definition_text != '':
            properties = {"definition":definition_text}

        if term_type == "concept":
            node = Concept.create(name=term_name,properties=properties)        
            return view_concept(request,node["id"])

        elif term_type == "task":
            node = Task.create(name=term_name,properties=properties)        
            return view_task(request,node["id"])


def contribute_disorder(request):

    return render(request,'atlas/contribute_disorder.html',context)

# UPDATE TERMS ####################################################################

def update_concept(request,uid):
    if request.method == "POST":
        definition = request.POST.get('definition', '')
        updates = add_update("definition",definition)
        Concept.update(uid,updates=updates)
    return view_concept(request,uid)

def update_task(request,uid):
    if request.method == "POST":
        definition = request.POST.get('definition', '')
        updates = add_update("definition",definition)
        Task.update(uid,updates=updates)
    return view_task(request,uid)

def update_disorder(request,uid):
    if request.method == "POST":
        definition = request.POST.get('disorder_definition', '')
        name = request.POST.get('disorder_name','')
        updates = add_update("name",name)
        updates = add_update("definition",definition,updates)
        Disorder.update(uid,updates=updates)
    return view_disorder(request,uid)
