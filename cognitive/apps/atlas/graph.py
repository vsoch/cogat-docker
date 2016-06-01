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

# GRAPH GIST ######################################################################
# These are export functions for concepts, tasks, etc to be previewed as graph gists

# Can't test this until we have this on a server

def task_gist(request,uid):
    context = {"task_id":uid}
    return render(request,'graph/task_gist.html',context)

# Eg, This is the URL that can be linked to from a page
# http://portal.graphgist.org/graph_gists/by_url?url=hello
# Note: may need to this: https://docs.djangoproject.com/en/1.9/howto/outputting-csv/
