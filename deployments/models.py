
from django.db import models

from django.contrib.auth.models import User

# Create your models here.



class Project(models.Model):

    name = models.CharField(max_length=250)
    creator = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)


    def __unicode__(self):
        return self.name


class Deployment(models.Model):

    name = models.CharField(max_length=250)
    creator = models.ForeignKey(User) 
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return self.name


class DeploymentEvent(models.Model):

    tag = models.CharField(max_length = 100)
    message = models.CharField(max_length = 500)

    created_at = models.DateTimeField(auto_now_add=True)
    deployment = models.ForeignKey(Deployment)




class Hook(models.Model):

    every_push = models.BooleanField(default = False)
    commit_message_contains = models.CharField(max_length=250)

    deployments = models.ManyToManyField(Deployment)

    def __unicode__(self):
        try:
            return self.deployments.all()[0].name
        except:
            return "NO DEPLOYMENT"


