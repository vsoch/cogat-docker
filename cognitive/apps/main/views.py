from cognitive.apps.atlas.query import Concept, Task, Disorder, Contrast
from django.shortcuts import render
from django.template import loader

Concept = Concept()
Task = Task()
Disorder = Disorder()
Contrast = Contrast()

def index(request):

    # We only need id and name for the home page
    fields = ["id","name"]

    concepts = Concept.all(limit=10,order_by="last_updated",fields=fields)
    concepts_count = Concept.count()

    tasks = Task.all(limit=10,order_by="last_updated",fields=fields)
    tasks_count = Task.count()

    disorders = Disorder.all(limit=10,order_by="last_updated",fields=fields)
    disorders_count = Disorder.count()

    contrasts = Contrast.all(limit=7,order_by="last_updated",fields=fields)
    contrasts_count = Contrast.count()
    
    appname = "The Cognitive Atlas"
    context = {'appname': appname,
               'active':'homepage',
               'concepts':concepts,
               'concepts_count':concepts_count,
               'tasks':tasks,
               'tasks_count':tasks_count,
               'contrasts':contrasts,
               'contrasts_count':contrasts_count,
               'disorders':disorders,
               'disorders_count':disorders_count}

    return render(request,'main/index.html',context)
