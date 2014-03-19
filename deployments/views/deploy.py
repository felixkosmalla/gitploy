from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required

from deployments.models import *
from django.views.decorators.csrf import csrf_exempt


from django.contrib import messages

from django.forms import ModelForm

from django.forms.models import modelform_factory

import django.dispatch

from deployments.deployment_runner import *

from django.http import HttpResponse


DeploymentForm = modelform_factory(Deployment, fields=("name","host","username","password","shell_code"))


@login_required
def add_deployment(request, project_id):


    try:
        p = Project.objects.get(id=project_id)
    except:
        pass

    if (request.method == "POST"):

        form = DeploymentForm(request.POST)

        if form.is_valid():
            deployment = form.save(commit =False)
            deployment.creator = request.user
            deployment.project_id = project_id
            print project_id
            deployment.save()

            
            messages.add_message(request, messages.SUCCESS, "Deployment <i>"+deployment.name+"</i> created")

            
            pass

    else:
        form = DeploymentForm()

    return render(request,"add_deployment.html", {'form':form, 'project':p})



@login_required
def edit_deployment(request, deployment_id):


    try:
        d = Deployment.objects.get(id=deployment_id)
        p = d.project
    except:
        pass

    if (request.method == "POST"):

        form = DeploymentForm(request.POST, instance=d)

        if form.is_valid():
            deployment = form.save(commit =True)
            
            messages.add_message(request, messages.SUCCESS, "Deployment <i>"+deployment.name+"</i> saved")

            
            pass

    else:
        form = DeploymentForm(instance=d)

    return render(request,"edit_deployment.html", {'form':form, 'project':p})



@login_required
def run_deployment(request, deployment_id):

    (success, output) = run_deployment_by_id(deployment_id)

    deployment = Deployment.objects.get(id=deployment_id)

    deployment.save_execution(success, output, None, request.user)

    return HttpResponse("<pre>"+output+"</pre>")

@login_required
def past_deployments(request, deployment_id):

    d = Deployment.objects.get(id=deployment_id)

    return render(request, "past_deployments.html", {'deployment':d})  


@csrf_exempt
def run_hook(request, hook_id, key):

    hook = Hook.objects.get(id=hook_id, key=key)

    (s, o) = execute_hook(hook, request)

    return HttpResponse(o)



# def deployment(request, project_id):

#     try:
#         p = Project.objects.get(id=project_id)

#     except:
#         return redirect("index")


#     return render(request, "project.html",{'project':p})

