# Create your views here.
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from django.template import RequestContext
from django.shortcuts import render_to_response


def index(request):
	#return HttpResponse("Rango says hello world!") # old code CH3
	context = RequestContext(request)
	
	##context_dict = {'boldmessage': "I am from the context"}
	
	#CH6 code below
	category_list = Category.objects.order_by('-likes')[:5]
	context_dict = {'categories': category_list}
	
	for category in category_list:
		category.url = category.name.replace(' ', '_')
	
	return render_to_response('rango/index.html', context_dict, context)
	
def about_page(request):
	return HttpResponse("Rango says this is the about page")

def category(request, category_name_url):
	context = RequestContext(request)
	
	category_name = category_name_url.replace('_', ' ')
	
	context_dict = {'category_name': category_name}
	
	try:
		category = Category.objects.get(name=category_name)
		
		pages = Page.objects.filter(category=category)
		
		context_dict['pages'] = pages
		
		context_dict['category'] = category
	except Category.DoesNotExist:
		
		pass
		
	return render_to_response('rango/category.html', context_dict, context)
