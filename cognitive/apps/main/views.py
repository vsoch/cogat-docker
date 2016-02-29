from cognitive.apps.atlas.query import Concept, Task, Disorder, Theory, Battery
from django.shortcuts import render
from django.template import loader

Concept = Concept()
Task = Task()
Disorder = Disorder()
Theory = Theory()
Battery = Battery()

# Needed on all pages
counts = {"disorders":Disorder.count(),
          "tasks":Task.count(),
          "concepts":Concept.count(),
          "theories":Theory.count(),
          "batteries":Battery.count()}

def index(request):

    # We only need id and name for the home page
    fields = ["id","name"]

    concepts = Concept.all(limit=10,order_by="last_updated",fields=fields)
    tasks = Task.all(limit=10,order_by="last_updated",fields=fields)
    disorders = Disorder.all(limit=10,order_by="last_updated",fields=fields)
    theories = Theory.all(limit=7,order_by="last_updated",fields=fields)
    
    appname = "The Cognitive Atlas"
    context = {'appname': appname,
               'active':'homepage',
               'concepts':concepts,
               'tasks':tasks,
               'theories':theories,
               'disorders':disorders,
               'counts':counts}

    return render(request,'main/index.html',context)
