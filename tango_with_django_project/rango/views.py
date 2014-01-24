# Create your views here.
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from datetime import datetime

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
	
	#CH10.5 code
	#visits = int(request.COOKIES.get('visits', '0'))
	
	#if request.COOKIES.has_key('last_visit'):
		
		#last_visit = request.COOKIES['last_visit']
		#last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
		
		#if (datetime.now() - last_visit_time).days > 0:
			#response.set_cookie('visits', visits+1)
			#response.set_cookie('last_visit', datetime.now())
		
	#else:
		#response.set_cookie('last_visit', datetime.now())
		
	#return response
	
	#CH10.6 code
	
	if request.session.get('last_visit'):
		last_visit_time = request.session.get('last_visit')
		visits = request.session.get('visits', 0)
		
		if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
			request.session['visits'] = visits + 1
			request.session['visits'] = 1
		
	else:
		request.session['last_visit'] = str(datetime.now())
		request.session['visits'] = 1
		
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

def user_login(request):
	context = RequestContext(request)
	
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		
		user = authenticate(username=username, password=password)
		
		if user is not None:
			
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/rango/')
				
			else:
				return HttpResponse("Your Rango account is disabled!")
				
		else:
			print "Invalid login details: {0}, {1}.".format(username, password)
			return HttpResponse("Invalid login details supplied.")
			
	else:
		return render_to_response('rango/login.html', {}, context)

@login_required
def restricted(request): #Ch8.6 function, not really important
	return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
	logout(request)
	
	return HttpResponseRedirect('/rango/')
