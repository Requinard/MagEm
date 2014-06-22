from django.views.generic import View
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

# Create your views here.
class LoginView(View):
	def get(self, *args, **kwargs):
		return redirect("magazine:index")

	def post(self, request, *args, **kwargs):
		user = authenticate(username=request.POST['user'], password=request.POST['password'])

		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect("magazine:index")
			else:
				return HttpResponseForbidden()
		else:
			return HttpResponseNotAllowed()