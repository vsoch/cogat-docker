from cognitive.apps.atlas.query import Concept
from django.shortcuts import render
from django.template import loader

def index(request):
    appname = "The Cognitive Atlas"
    context = {'appname': appname,
               'active':'home'}
    return render(request,'main/index.html',context)
