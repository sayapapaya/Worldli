from django.template.context import RequestContext
from django.shortcuts import render, render_to_response
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponse
from .forms import UploadImageForm
from app.models import *
import requests


def index(request):
	social = None
	if request.user and hasattr(request.user, "social_auth"):
		social = request.user.social_auth.get(provider="facebook")
	problems = Problem.objects.all()
	context = RequestContext(request, {"user": request.user, "request": request, "social": social, "problems": problems})
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
		return HttpResponse("data saved successfully")

def create_post(request):
	social = None
	if request.user and hasattr(request.user, "social_auth"):
		social = request.user.social_auth.get(provider="facebook")
	context = RequestContext(request, {"social":social})
	return render_to_response("app/create_post.html", context_instance=context)

def my_post(request):
	social = None
	if request.user and hasattr(request.user, "social_auth"):
		social = request.user.social_auth.get(provider="facebook")
	problem = Problem.objects.get(user=request.user)
	context = RequestContext(request, {"social":social, "problem": problem})
	return render_to_response("app/my_post.html", context_instance=context)


def view_post(request, problem_id):
	social = None
	if request.user and hasattr(request.user, "social_auth"):
		social = request.user.social_auth.get(provider="facebook")
	problem = Problem.objects.get(id=problem_id)
	images = ProblemImage.objects.filter(problem=problem)
	context = RequestContext(request, {"social":social, "problem": problem, "images":images})
	return render_to_response("app/view_post.html", context_instance=context)

def create_problem(request):
	social = None
	problem = None
	if request.user and hasattr(request.user, "social_auth"):
		social = request.user.social_auth.get(provider="facebook")
	if request.method == "POST":
		title = request.POST.get('title')
		description = request.POST.get('description')
		location = request.POST.get('location')
		latitude = request.POST.get('latitude')
		longitude = request.POST.get('longitude')
		problem = Problem.objects.filter(user=request.user, title=title)
		if len(problem) == 0:
			problem = Problem(user=request.user, title=title, description=description, location=location, latitude=latitude, longitude=longitude)
			try:
				problem.save()
			except Exception, e:
				context = RequestContext(request, {"social":social, "error_msg": str(e)})
				return render_to_response("app/create_post.html", context_instance=context)
		else:
			problem[0].title = title
			problem[0].description = description
			problem[0].location = location
			problem[0].latitude = latitude
			problem[0].longitude = longitude
			try:
				problem[0].save()
				problem = problem[0]
			except Exception, e:
				context = RequestContext(request, {"social":social, "error_msg": str(e)})
				return render_to_response("app/create_post.html", context_instance=context)
	if problem == None:
		context = RequestContext(request, {"social":social})
		return render_to_response("app/create_post.html", context_instance=context)
	images = ProblemImage.objects.filter(problem=problem)
	context = RequestContext(request, {"social":social, "problem":problem, "images": images})
	return render_to_response("app/upload_images.html", context_instance=context)

def upload_images(request, problem_id):
	if request.method == "POST":
		form = UploadImageForm(request.POST, request.FILES)
		if form.is_valid():
			problemimage = ProblemImage(image=request.FILES["image"], problem=Problem.objects.get(id=problem_id))
			try:
				problemimage.save()
			except Exception, e:
				print str(e)
	social = None
	if request.user and hasattr(request.user, "social_auth"):
		social = request.user.social_auth.get(provider="facebook")
	problem = Problem.objects.get(id=problem_id)
	images = ProblemImage.objects.filter(problem=problem)
	context = RequestContext(request, {"social":social, "problem": problem, "images": images})
	return render_to_response("app/upload_images.html", context_instance=context)

def delete_image(request, image_id):
	social = None
	if request.user and hasattr(request.user, "social_auth"):
		social = request.user.social_auth.get(provider="facebook")
	problemimage = ProblemImage.objects.get(id=image_id)
	problemimage.delete()
	problem = Problem.objects.filter(user=request.user, title=request.GET.get('problem'))[0]
	images = ProblemImage.objects.filter(problem=problem)
	context = RequestContext(request, {"social":social, "problem": problem, "images": images})
	return render_to_response("app/upload_images.html", context_instance=context)

def place_autocomplete(request):
	if request.method == "POST":
		API_KEY = "AIzaSyD-oVtT-NbHwFJDJkjKbbe-I4llMFBbXtg"
		text = request.POST.get("search")
		url = "https://maps.googleapis.com/maps/api/place/autocomplete/json?types=(regions)&input=%s&key=%s" % (text, API_KEY)
		r = requests.get(url)
		return HttpResponse(r.text)

