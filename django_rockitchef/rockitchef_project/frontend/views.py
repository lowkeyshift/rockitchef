from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

def frontend(request):
    # template = loader.get_template('index.html')
    html = '<div>hello</div>'
    # return HttpResponse(html)
    return render(request, 'index.html')