from django.template.context import RequestContext
from django.shortcuts import render, render_to_response
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponse
from .forms import UploadImageForm
from app.models import *
import requests
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q

def index(request):
	social = None
	if request.user and hasattr(request.user, "social_auth"):
		social = request.user.social_auth.get(provider="facebook")
	problems = Problem.objects.all()
	image_dict = {}
	for problem in problems:
		images = ProblemImage.objects.filter(problem=problem)
		image_dict[problem] = images
	context = RequestContext(request, {"user": request.user, "request": request, "social": social, "problems": problems, "image_dict": image_dict})
	return render_to_response("app/index.html", context_instance=context)

def profile(request):
	social = None
	if request.user and hasattr(request.user, "social_auth"):
		social = request.user.social_auth.get(provider="facebook")
	else:
		raise Http404("Profile does not exist.")
	person = Person.objects.filter(user=request.user)
	skills = Skill.objects.filter(person=person)
	context = RequestContext(request, {"user": request.user, "request": request,"social": social, "person":person, "skills":skills})
	return render_to_response("app/profile.html", context_instance=context)

def create_user(request):
	if request.method == 'POST':
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		email = request.POST.get('email')
		education = request.POST.get('education')
		location = request.POST.get('location')
		skills = request.POST.getlist('skills[]')
		latitude = request.POST.get('latitude')
		longitude = request.POST.get('longitude')
		# save to database
		person = Person.objects.filter(user=request.user)
		if len(person) == 0:
			person = Person(user=request.user, first_name=first_name, last_name=last_name, email=email, education=education, location=location, latitude=latitude, longitude=longitude)
			person.save()
			for i in range(len(skills)-1):
				s = Skill(text=skills[i], person=person[0])
				s.save()
		else:
			old_skills = Skill.objects.filter(person=person[0])
			for i in range(len(old_skills)):
				if (old_skills[i] not in skills):
					s = Skill.objects.get(text=old_skills[i], person=person[0])
					s.delete()
			for i in range(len(skills)-1):
				if (skills[i] not in old_skills):
					s = Skill(text=skills[i], person=person[0])
					s.save()
			person[0].first_name = first_name
			person[0].last_name = last_name
			person[0].email = email
			person[0].education = education
			person[0].location = location
			person[0].latitude = latitude
			person[0].longitude = longitude
			person[0].save()
		return HttpResponse("data saved successfully")

def create_post(request):
	social = None
	if request.user and hasattr(request.user, "social_auth"):
		social = request.user.social_auth.get(provider="facebook")
	context = RequestContext(request, {"social":social})
	return render_to_response("app/create_post.html", context_instance=context)

def edit_post(request, problem_id):
	social = None
	if request.user and hasattr(request.user, "social_auth"):
		social = request.user.social_auth.get(provider="facebook")
	problem = Problem.objects.get(id=problem_id)
	if problem.user != request.user:
		context = RequestContext(request, {"social":social})
		return render_to_response("app/index.html", context_instance=context)
	context = RequestContext(request, {"social":social, "problem":problem})
	return render_to_response("app/edit_post.html", context_instance=context)

def my_post(request):
	social = None
	if request.user and hasattr(request.user, "social_auth"):
		social = request.user.social_auth.get(provider="facebook")
	problems = Problem.objects.filter(user=request.user)
	image_dict = {}
	for problem in problems:
		images = ProblemImage.objects.filter(problem=problem)
		image_dict[problem.id] = images
	context = RequestContext(request, {"social":social, "problems": problems, "image_dict":image_dict})
	return render_to_response("app/my_post.html", context_instance=context)


def view_post(request, problem_id):
	social = None
	if request.user and hasattr(request.user, "social_auth"):
		social = request.user.social_auth.get(provider="facebook")
	problem = Problem.objects.get(id=problem_id)
	images = ProblemImage.objects.filter(problem=problem)
	comments = Comment.objects.filter(problem=problem)
	comment_users = {}
	for comment in comments:
		comment_users[comment] = comment.user.social_auth.get(provider="facebook")
	context = RequestContext(request, {"user": request.user, "social":social, "problem": problem, "images":images, "comments":comments, "comment_users":comment_users})
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

def edit_problem(request, problem_id):
	if request.method == "POST":
		problem = Problem.objects.get(id=problem_id)
		problem.title = request.POST.get('title')
		problem.description = request.POST.get('description')
		problem.location = request.POST.get('location')
		problem.latitude = request.POST.get('latitude')
		problem.longitude = request.POST.get('longitude')
		problem.save()
	if problem.user != request.user:
		context = RequestContext(request, {"social":social})
		return render_to_response("app/index.html", context_instance=context)
	social = None
	if request.user and hasattr(request.user, "social_auth"):
		social = request.user.social_auth.get(provider="facebook")
	images = ProblemImage.objects.filter(problem=problem)
	context = RequestContext(request, {"social":social, "problem":problem, "images": images})
	return render_to_response("app/upload_images.html", context_instance=context)

def delete_problem(request, problem_id):
	problem = Problem.objects.get(id=problem_id)
	problem.delete()
	return my_post(request)

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

def search_autocomplete(request):
	if request.method == "POST":
		search_text = request.POST["search_text"]
	else:
		search_text = ""
	problems = Problem.objects.filter(title__contains=search_text)
	results = [{}]
	for problem in problems:
		results[0][problem.id] = {"title": problem.title} 
	data = json.dumps(results)
	return HttpResponse(data, "application/json")

def search(request):
	if request.method == "POST":
		search_text = request.POST["search_text"]
		try:
			problem = Problem.objects.get(title=search_text)
			results = {"id": problem.id, "latitude":problem.latitude, "longitude":problem.longitude}
			data = json.dumps(results)
			return HttpResponse(data, "application/json")
		except:
			return HttpResponse("Doesn't exist")

def search_people_name(request):
	if request.method == "POST":
		search_text = request.POST["search_text"]
		try:
			people = Person.objects.filter(Q(first_name__contains=search_text) | Q(last_name__contains=search_text))
			results = {}
			print people
			for i in range(len(people)):
				results[i] = {"id": people[i].id, "latitude": people[i].latitude, "longitude":people[i].longitude}
			return HttpResponse(json.dumps(results), "application/json")
		except:
			return HttpResponse("Doesn't exist")

def search_skills(request):
	if request.method == "POST":
		search_text = request.POST["search_text"]
		try:
			skills = Skill.objects.filter(text=search_text)
			print skills
			people = []
			for skill in skills:
				people.append(skill.person)
			people = list(set(people))
			results = {}
			for i in range(len(people)):
				results[i] = {"id": people[i].id, "latitude": people[i].latitude, "longitude": people[i].longitude}
			return HttpResponse(json.dumps(results), "application/json")
		except Exception, e:
			print e
			return HttpResponse("Doesn't exist")

def create_comment(request, problem_id):
	if request.method == "POST":
		text = request.POST.get('text')
		try: 
			followup_id = request.POST.get('comment_id');
			followup = Comment.objects.get(id=followup_id)
			comment = Comment(user=request.user, problem=Problem.objects.get(id=problem_id), upvotes=0, followup=followup, text=text)
			comment.save()
		except:
			comment = Comment(user=request.user, problem=Problem.objects.get(id=problem_id), upvotes=0, text=text)
			comment.save()
		return view_post(request, problem_id)

def delete_comment(request, comment_id):
	comment = Comment.objects.get(id=comment_id)
	comment.delete()
	problem_id = request.GET['problem_id']
	return view_post(request, problem_id)

def filterProblems(request):
	tags = request.POST.getlist("tags[]")
	filteredProblems = []
	for tag in tags:
		filteredProblems += Problem.objects.filter(tags=tag)
	results={}
	for i in range(len(filteredProblems)):
		problem = filteredProblems[i]
		images = ProblemImage.objects.filter(problem=problem)
		if len(images)==0:
			url = 'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcSeorgZD9j5kKDFuH5bBk-jbUp9hJbyNTPG-mUPxD59jZrG0UsuxjITva_k'
		else:
			url =images[0].image.url
		results[filteredProblems[i].id] = {"title": filteredProblems[i].title, "latitude": filteredProblems[i].latitude, "longitude": filteredProblems[i].longitude,"picture":url}
		print results
	data = json.dumps(results)
	return HttpResponse(data, "application/json")
