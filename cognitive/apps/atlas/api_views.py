import pandas

from rest_framework.response import Response
from rest_framework.views import APIView

from .query import Concept, Contrast, Disorder, Task

Concept = Concept()
Contrast = Contrast()
Disorder = Disorder()
Task = Task()

class SearchAPI(APIView):
    def get(self, request, format=None):
        return Response()

class ConceptAPI(APIView):
    def get(self, request, format=None):
        fields = {}
        id = request.GET.get("id", "")
        name = request.GET.get("name", "")
        contrast_id = request.GET.get("contrast_id", "")
        
        if id:
            concept = Concept.get(id, 'id')
        elif name:
            concept = Concept.get(name, 'name')
        elif contrast_id:
            concept = Contrast.get_by_relation(contrast_id, "id", "concept", "MEASUREDBY")
        else:
            concept = Concept.all()
        
        return Response(concept())

class TaskAPI(APIView):
    def get(self, request, format=None):
        id = request.GET.get("id", "")
        name = request.GET.get("name", "")
        
        if id:
            task = Task.get(id, 'id')
        elif name:
            task = Task.get(name, 'name')
        else:
            task = Task.all()
        
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
        
        return Response(disorder)


