from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required

from deployments.models import *


from django.contrib import messages

from django.forms import ModelForm

from django.forms.models import modelform_factory

import django.dispatch


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

