from rest_framework.response import Response
from rest_framework.views import APIView

from .query import Task
from .serializers import TaskSerializer

class TaskAPIList(APIView):

    def get(self, request, format=None):
        tasks = Task.all()
        ser_tasks = [TaskSerializer(x) for x in tasks]
        return Response(ser_tasks)
