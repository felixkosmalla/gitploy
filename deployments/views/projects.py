from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required

from deployments.models import *


from django.contrib import messages

from django.forms import ModelForm

from django.forms.models import modelform_factory

import django.dispatch


ProjectForm = modelform_factory(Project, fields=("name",))

@login_required
def add_project(request):


    if (request.method == "POST"):

        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit =False)
            project.creator = request.user
            project.save()

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