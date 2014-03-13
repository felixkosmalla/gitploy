
from django.db import models

from django.contrib.auth.models import User

import django.dispatch

from simplecrypt import encrypt, decrypt

from django.conf import settings

from django_extensions.db.fields.encrypted import *

# Create your models here.



class Project(models.Model):

    name = models.CharField(max_length=250)
    creator = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)


    def __unicode__(self):
        return self.name


    # signals
    project_created = django.dispatch.Signal(providing_args=["project"])


class Deployment(models.Model):

    name = models.CharField(max_length=250)
    creator = models.ForeignKey(User) 
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, related_name="deployments")

    host = models.CharField(max_length = 500)
    username = models.CharField(max_length = 500)
    password = EncryptedCharField(max_length = 500)
    shell_code = models.TextField(max_length = 500)


    def _get_last_run(self):
        return DeploymentExecution.objects.filter(deployment=self).order_by('-run_at')[:1].get()    

    @property
    def last_run_successful(self):
        lr = self._get_last_run()

        if lr:
            return lr.success

        return False

    @property
    def last_run_at(self):
        lr = self._get_last_run()

        if lr:
            return lr.run_at

        return False


    def __unicode__(self):
        return self.name



class DeploymentExecution(models.Model):

    deployment = models.ForeignKey(Deployment, related_name='executions')
    run_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField()
    output = models.TextField()
    hook = models.ForeignKey("Hook", blank=True, null=True)

    @property
    def manual(self):
        return hook is None



class Hook(models.Model):

    every_push = models.BooleanField(default = False)
    commit_message_contains = models.CharField(max_length=250)

    deployments = models.ManyToManyField(Deployment)

    def __unicode__(self):
        try:
            return self.deployments.all()[0].name
        except:
            return "NO DEPLOYMENT"


