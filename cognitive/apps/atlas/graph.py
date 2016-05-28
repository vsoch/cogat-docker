from django.shortcuts import render
from django.http import JsonResponse
from cognitive.apps.atlas.query import Task

Task = Task()

# Return full graph visualizations

def task_graph(request,uid):

    nodes = Task.graph(uid)

    context = {"graph":nodes}
    return render(request,"graph/task.html",context)

def test_graph(request):

    nodes = {"nodes":[{"name":"Peter","label":"Person","id":1},{"name":"Michael","label":"Person","id":2},
                      {"name":"Neo4j","label":"Database","id":3}],
             "links":[{"source":0, "target":1, "type":"KNOWS", "since":2010},{"source":0, "target":2, "type":"FOUNDED"},
                      {"source":1, "target":2, "type":"WORKS_ON"}]}

    context = {"graph":nodes}
    return render(request,"graph/task.html",context)


# Return just json
def task_json(request,uid):
    nodes = Task.graph(uid)
    return JsonResponse(nodes)

