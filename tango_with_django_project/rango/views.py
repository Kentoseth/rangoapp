# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
	#return HttpResponse("Rango says hello world!") # old code CH3
	context = RequestContext(request)
	
	context_dict = {'boldmessage': "I am from the context"}
	
	return render_to_response('rango/index.html', context_dict, context)
	
def about_page(request):
	return HttpResponse("Rango says this is the about page")
