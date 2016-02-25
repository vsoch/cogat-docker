from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from .query import Concept, Contrast, Disorder, Task, do_query

Concept = Concept()
Contrast = Contrast()
Disorder = Disorder()
Task = Task()

class ConceptAPI(APIView):
    def get(self, request, format=None):
        fields = {}
        id = request.GET.get("id", "")
        name = request.GET.get("name", "")
        contrast_id = request.GET.get("contrast_id", "")
        print(len(request.GET))
        if id:
            concept = Concept.get(id, 'id')
        elif name:
            concept = Concept.get(name, 'name')
        elif contrast_id:
            concept = Contrast.get_by_relation(contrast_id, "id", "concept", "MEASUREDBY")
        else:
            concept = Concept.all()
        
        if concept is None:
            raise NotFound('Concept not found')
        return Response(concept)

class TaskAPI(APIView):
    def get(self, request, format=None):
        id = request.GET.get("id", "")
        name = request.GET.get("name", "")
        
        if id:
            task = Task.get_full(id, 'id')
        elif name:
            task = Task.get_full(name, 'name')
        else:
            task = Task.all()
        
        print(task)
        if task is None:
            raise NotFound('Task not found')
        return Response(task)

class DisorderAPI(APIView):
    def get(self, request, format=None):
        id = request.GET.get("id", "")
        name = request.GET.get("name", "")
        
        if id:
            disorder = Disorder.get(id, 'id')
        elif name:
            disorder = Disorder.get(name, 'name')
        else:
            disorder = Disorder.all()
        
        if disorder is None:
            raise NotFound('Disorder not found')
        return Response(disorder)


class SearchAPI(APIView):
    def get(self, request, format=None):
        search_classes = [Concept, Contrast, Disorder, Task]
        queries = request.GET.get("q", "")
        results = []
        for cls in search_classes:
            result = cls.search_all_fields(queries)
            results += result
        if not results:
            raise NotFound('No results found')
        return Response(results)
