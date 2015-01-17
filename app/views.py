from django.template.context import RequestContext
from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponse
from app.models import *


def index(request):
	social = None
	if request.user and hasattr(request.user, "social_auth"):
		social = request.user.social_auth.get(provider="facebook")
	context = RequestContext(request, {"user": request.user, "request": request, "social": social})
	return render_to_response("app/index.html", context_instance=context)

def profile(request):
	social = None
	if request.user and hasattr(request.user, "social_auth"):
		social = request.user.social_auth.get(provider="facebook")
	else:
		raise Http404("Profile does not exist.")
	person = Person.objects.filter(user=request.user)
	context = RequestContext(request, {"user": request.user, "request": request,"social": social, "person":person})
	return render_to_response("app/profile.html", context_instance=context)

def create_user(request):
	if request.method == 'POST':
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		email = request.POST.get('email')
		education = request.POST.get('education')
		linkedin = request.POST.get('linkedin')
		# save to database
		person = Person.objects.filter(user=request.user)
		if len(person) == 0:
			person = Person(user=request.user, first_name=first_name, last_name=last_name, email=email, education=education, linkedin=linkedin)
			person.save()
		else:
			person[0].first_name = first_name
			person[0].last_name = last_name
			person[0].email = email
			person[0].education = education
			person[0].linkedin = linkedin
			person[0].save()
		return HttpResponse("data saved succesfully")
