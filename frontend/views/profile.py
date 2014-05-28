from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login as ulogin, logout as ulogout
from django.contrib import messages

from deployments.models import *
from django.http import HttpResponse
from django.conf import settings
import gitlab

from django.views.decorators.csrf import csrf_exempt

from django import forms


class ProfileForm(forms.Form):

	token = forms.CharField(max_length = 200)
	


@login_required
def profile(request):
	user_settings = request.user.settings

	if (request.method == 'POST'):
		# return HttpResponse("post")
		form = ProfileForm(request.POST)
		if form.is_valid():
			user_settings.gitlab_token = form.cleaned_data['token']
			user_settings.save()
			messages.success(request, 'New access token set.')
			pass
		else:
			messages.error(request, 'New access token set.')
	else:
		form = ProfileForm({'token':user_settings.gitlab_token}) 



	return render(request, "profile.html",{
		'form':form,
		'public_key':settings.DEPLOY_KEY
		})

@csrf_exempt
def validate_token(request):

    token = request.POST['token']

    git = gitlab.Gitlab(settings.GITLAB_URL, token)

    sample_request = git.getprojects()

    if sample_request == False:
        return HttpResponse("0")
    else:
        return HttpResponse("1")