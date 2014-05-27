from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required

from deployments.models import *


from django.contrib import messages

from django.forms import ModelForm

from django.forms.models import modelform_factory

import django.dispatch
import gitlab
from django.conf import settings
from django.http import HttpResponse


# HookForm = modelform_factory(Hook, fields=("every_push","commit_message_regex","deployments"))

class HookForm(ModelForm):

    class Meta:
        model = Hook
        fields = ("name","every_push","commit_message_regex","deployments")

    def __init__(self, *args, **kwargs):
        
        current_project_id = kwargs.pop('current_project_id')
        print current_project_id
        super(HookForm, self).__init__(*args, **kwargs)

        self.fields['deployments'].queryset = Deployment.objects.filter(project_id=int(current_project_id))
    

@login_required
def add_hook(request, project_id):


    if (request.method == "POST"):

        form = HookForm(request.POST, current_project_id= project_id)

        if form.is_valid():
            hook = form.save(commit =True)
            hook.creator = request.user
            hook.project_id = project_id
            hook.save()

            register_hook = False

            try:
                tmp = request.POST['id_register_hook']
                register_hook = True
            except:
                pass

            if register_hook:
                git = gitlab.Gitlab(settings.GITLAB_URL, request.user.settings.gitlab_token)
                url_hook = request.build_absolute_uri(hook.get_absolute_url())

                if git.addprojecthook(hook.project.gitlab_id, url_hook):
                    messages.add_message(request, messages.SUCCESS, "Hook registered in GitLab")
                else:
                    messages.add_message(request, messages.ERROR, "Hook could not be registered")
                


            
            #project.project_created.send(sender=project, project = project)
            messages.add_message(request, messages.SUCCESS, "Hook for project <i>"+hook.project.name+"</i> created")
            return redirect(reverse("project",args=[project_id]))

            pass

    else:
        form = HookForm(current_project_id=project_id)

    return render(request,"add_hook.html", {'form':form})


@login_required
def edit_hook(request, hook_id):
    
    d = Hook.objects.get(id=hook_id)

    url = request.build_absolute_uri(d.get_absolute_url())

    if (request.method == "POST"):

        form = HookForm(request.POST, instance=d, current_project_id=d.project_id)

        if form.is_valid():
            hook = form.save(commit =True)
            
            messages.add_message(request, messages.SUCCESS, "Hook for project <i>"+hook.project.name+"</i> saved")
            
            pass

    else:
        form = HookForm(instance=d, current_project_id=d.project_id)

    return render(request,"edit_hook.html", {'form':form, 'hook':d, 'project':d.project, 'url':url})

@login_required
def delete_hook(request, hook_id):

    
    p= Hook.objects.get(id=hook_id)
    p.delete()
    
    return HttpResponse("1")    

