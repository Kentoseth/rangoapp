# Create your views here.
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm

def encode_url(str):
	return str.replace(' ','_')
	
def decode_url(str):
	return str.replace('_', ' ')

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
	
	context_dict = {'category_name': category_name, 'category_name_url': category_name_url}
	
	try:
		category = Category.objects.get(name=category_name)
		
		pages = Page.objects.filter(category=category)
		
		context_dict['pages'] = pages
		
		context_dict['category'] = category
	except Category.DoesNotExist:
		
		pass
		
	return render_to_response('rango/category.html', context_dict, context)

def add_category(request):
	context = RequestContext(request)
	
	if request.method =='POST':
		form = CategoryForm(request.POST)
		
		if form.is_valid():
			form.save(commit=True)
			
			return index(request)
		else:
			print form.errors
			
	else:
		form = CategoryForm()
		
	return render_to_response('rango/add_category.html', {'form': form}, context)

def add_page(request, category_name_url):
	context = RequestContext(request)
	
	category_name = decode_url(category_name_url)
	if request.method =='POST':
		form = PageForm(request.POST)
		
		if form.is_valid():
			page = form.save(commit=False)
			
			cat = Category.objects.get(name=category_name)
			page.category = cat
			
			page.views = 0
			
			page.save()
			
			return category(request, category_name_url)
		else:
			print form.errors
	else:
		form = PageForm()
		
	return render_to_response('rango/add_page.html',
			{'category_name_url': category_name_url,
			'category_name': category_name, 'form': form},
			context)

def register(request):
	context = RequestContext(request)
	
	registered = False
	
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			
			user.set_password(user.password)
			user.save()
			
			profile = profile_form.save(commit=False)
			profile.user = user
			
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
				
			profile.save()
			
			registered = True
			
		else:
			print user_form.errors, profile_form.errors
			
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
		
	return render_to_response(
		'rango/register.html',
		{'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
		context)
