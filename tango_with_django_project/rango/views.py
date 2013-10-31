# Create your views here.
from django.http import HttpResponse

def index(request):
	return HttpResponse("Rango says hello world!")
	
def about_page(request):
	return HttpResponse("Rango says this is the about page")
