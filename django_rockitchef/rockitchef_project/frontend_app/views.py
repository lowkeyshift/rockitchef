
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

def frontend(request):
    template = loader.get_template('index.html')
    html = template.render()
    return HttpResponse(html)