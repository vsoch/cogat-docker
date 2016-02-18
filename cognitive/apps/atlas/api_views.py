from rest_framework.response import Response
from rest_framework.views import APIView

from .query import Concept, Disorder, Task

Concept = Concept()
Disorder = Disorder()
Task = Task()

class SearchAPI(APIView):
    def get(self, request, format=None):
        return Response()

class ConceptAPI(APIView):
    def get(self, request, format=None):
        tasks = Concept.all()
        return Response(tasks)

class TaskAPI(APIView):
    def get(self, request, format=None):
        tasks = Task.all()
        return Response(tasks)

class DisorderAPI(APIView):
    def get(self, request, format=None):
        tasks = Disorder.all()
        return Response(tasks)
