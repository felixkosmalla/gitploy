from deployments.models import *
import urllib, hashlib
from django.conf import settings

def user_settings(request):

	settings = False

	if request.user.is_active:
		# check if the user has settings
		try:
			settings = request.user.settings
		except:
			settings = UserSettings()
			settings.user = request.user
			settings.save()



	print settings
	return {
		'user_settings':settings
	}


def projects(request):

    return {
        'projects':Project.objects.all()
    }

def project_settings(request):
	print settings.GITLAB_URL
	return{
		'project_settings':{
			'GITLAB_URL':settings.GITLAB_URL
		}
	}
