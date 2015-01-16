from django.template.context import RequestContext
from django.shortcuts import render, render_to_response



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
	context = RequestContext(request, {"user": request.user, "social": social})
	return render_to_response("app/profile.html", context_instance=context)
