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
		image_dict[problem.id] = images
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
	#print filteredProblems[0]
	#image_dict = {};
	#for problem in filteredProblems:
	#	image = images.objects.filter(problem=problem)
	#	image_dict[image[0].url]={"id": problem.id, "latitude":problem.latitude, "longitude":problem.longitude}
	#print len(filteredProblems)
	#print filteredProblems
	results={}
	for i in range(len(filteredProblems)):
		problem = filteredProblems[i]
		images = ProblemImage.objects.filter(problem=problem)
		if len(images)<=1:
			results[i] = {"id": filteredProblems[i].id, "latitude": filteredProblems[i].latitude, "longitude": filteredProblems[i].longitude,"image":"data:image/jpeg;base64,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"}
		else:
			image = images[0].url
			#print image
			results[i] = {"id": filteredProblems[i].id, "latitude": filteredProblems[i].latitude, "longitude": filteredProblems[i].longitude,"image":image}
	#print results
	data = json.dumps(results)
	return HttpResponse(data, "application/json")
