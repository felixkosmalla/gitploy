from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required

from deployments.models import *


from django.contrib import messages

from django.forms import ModelForm
from django import forms

from django.forms.models import modelform_factory

import django.dispatch
import gitlab
from django.conf import settings
from django.http import HttpResponse



@login_required
def add_project(request):

    git = gitlab.Gitlab(settings.GITLAB_URL, request.user.settings.gitlab_token)

    projects = git.getprojects()

    choices = []

    
    project_in_db = Project.objects.all()
    project_ids = []
    for project in project_in_db:
        project_ids.append(project.gitlab_id)


    project_names = []

    if(projects == False):
        return redirect(reverse("profile"))
    else:
        for project in projects:
            if not project['id'] in project_ids:
                choices.append((project['id'], project['name_with_namespace']))

        


    class ProjectForm(forms.Form):
        name = forms.CharField(max_length=200, widget = forms.HiddenInput(attrs={'id':'project_name'}), required=True)
        gitlab_id = forms.IntegerField( widget = forms.HiddenInput(attrs={'id':'project_id'}), required=True)
        projects = forms.CharField(max_length = 250, widget = forms.Select(choices = choices, attrs={'id':'project_select'}), required=True)



    if (request.method == "POST"):

        form = ProjectForm(request.POST)

        if form.is_valid():
            project = Project()
            project.name = form.cleaned_data['name']
            project.gitlab_id = int(form.cleaned_data['gitlab_id'])
            project.creator = request.user
            project.save()
            
            git.adddeploykey(project.gitlab_id, 'Deployment Tool', settings.DEPLOY_KEY)
            messages.add_message(request, messages.SUCCESS, "Added Deploy Key to <i>"+project.name+"</i>")

            project.project_created.send(sender=project, project = project)
            messages.add_message(request, messages.SUCCESS, "Project <i>"+project.name+"</i> created")
            return redirect(reverse("project",args=[project.id]))

            pass

    else:
        form = ProjectForm()

    return render(request,"add_project.html", {'form':form})

@login_required
def project(request, project_id):

    try:
        p = Project.objects.get(id=project_id)

    except:
        return redirect("index")


    return render(request, "project.html",{'project':p})

@login_required
def delete_project(request, project_id):

    try:
        p= Project.objects.get(id=project_id)
        p.delete()
    except:
        return HttpResponse("0")

    return HttpResponse("1")