from rest_framework.response import Response
from rest_framework.views import APIView

from .query import Task

Task = Task()

class TaskAPIList(APIView):

    def get(self, request, format=None):
        tasks = Task.all()
        return Response(tasks)
