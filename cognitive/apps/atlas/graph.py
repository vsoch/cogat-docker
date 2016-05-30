from django.shortcuts import render
from django.http import JsonResponse
from cognitive.apps.atlas.query import Task, Concept

Task = Task()
Concept = Concept()

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

