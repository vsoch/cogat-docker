from cognitive.apps.atlas.query import Concept, Task, Disorder, Theory, Battery
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from cognitive.settings import DOMAIN
from django.shortcuts import render
from django.template import loader

Concept = Concept()
Task = Task()
Disorder = Disorder()
Theory = Theory()
Battery = Battery()

def base(request):

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
               'disorders':disorders}

    return context

def index(request):
    context = base(request)
    return render(request,'main/index.html',context)


def about(request):
    context = base(request)
    return render(request,'main/about.html',context)

def api(request):
    context = base(request)
    context["domain"] = DOMAIN
    return render(request,'main/api.html',context)


# Error Pages ##################################################################

def handler404(request):
    response = render_to_response('main/404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

def handler500(request):
    response = render_to_response('main/500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response
