from django.template.context import RequestContext
from django.shortcuts import render, render_to_response


def index(request):
	social = None
	if request.user and hasattr(request.user, "social_auth"):
		social = request.user.social_auth.get(provider="facebook")
	context = RequestContext(request, {"user": request.user, "request": request, "social": social})
	return render_to_response("app/index.html", context_instance=context)

def login(request):
	return render(request, "app/index.html")

def logout(request):
	return render(request, "app/index.html")
