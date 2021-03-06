from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import Http404

from django.contrib.auth.decorators import login_required

from deployments.models import *
from django.views.decorators.csrf import csrf_exempt


from django.contrib import messages

from django.forms import ModelForm

from django.forms.models import modelform_factory

import django.dispatch

from deployments.deployment_runner import *

from django.http import HttpResponse

import deployments.ftp_synchronizer as ftp_sync
import ftputil
from fabric.api import *


DeploymentForm = modelform_factory(Deployment, fields=("name","deployment_type","host","username","password","ftp_home_dir", "shell_code"))


@login_required
def add_deployment(request, project_id):


    try:
        p = Project.objects.get(id=project_id)
    except:
        raise Http404

    if (request.method == "POST"):

        form = DeploymentForm(request.POST)

        if form.is_valid():
            deployment = form.save(commit =False)
            deployment.creator = request.user
            deployment.project_id = project_id
            
            deployment.save()

            
            messages.add_message(request, messages.SUCCESS, "Deployment <i>"+deployment.name+"</i> created")
            return redirect(reverse('project', args=[project_id])+'#deployment-'+str(deployment.id))
            
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

@csrf_exempt
def test_connection(request):

    user = request.POST['user']
    host = request.POST['host']
    password = request.POST['password']
    deployment_type = request.POST['type']
    ftp_home_dir = request.POST['ftp_home_dir']

    success = True

    if deployment_type == Deployment.SSH_SCRIPT:
        print "SSH"

        try:
            with settings(host_string=host, user=user, password=password, abort_on_prompts=True):
                
                try:
                    res = run('echo "test"')
                except:
                    success = False



        except:
            success = False

    elif deployment_type == Deployment.FTP_SYNC:

        try:
            host = ftputil.FTPHost(host, user, password)
            host.chdir(ftp_home_dir)
        except:
            success = False



    resp = "1"

    if not success:
        resp = "0"

    return HttpResponse(resp)
        



@login_required
def past_deployments(request, deployment_id):

    d = Deployment.objects.get(id=deployment_id)

    return render(request, "past_deployments.html", {'deployment':d})  


@csrf_exempt
def run_hook(request, hook_id, key):

    hook = Hook.objects.get(id=hook_id, key=key)

    (s, o) = execute_hook(hook, request)

    return HttpResponse(o)





def git_test(request, deployment_id):

    deployment = Deployment.objects.get(id=deployment_id)
    (success, res) = ftp_sync.synchronize_deployment(deployment, request)


    return HttpResponse(res)


@login_required
def delete_deployment(request, deployment_id):

    
    p= Deployment.objects.get(id=deployment_id)
    p.delete()
    
    return HttpResponse("1")    

