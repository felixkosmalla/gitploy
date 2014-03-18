
from django.db import models

from django.contrib.auth.models import User

import django.dispatch


from django.conf import settings

from django_extensions.db.fields.encrypted import *

import random
from django.core.urlresolvers import reverse

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


    def get_last_run(self):
        return DeploymentExecution.objects.filter(deployment=self).order_by('-run_at')[:1].get()    

    @property
    def last_run_successful(self):
        lr = self.get_last_run()

        if lr:
            return lr.success

        return False

    @property
    def last_run_at(self):
        lr = self.get_last_run()

        if lr:
            return lr.run_at

        return False


    def __unicode__(self):
        return self.name

    def save_execution(self, success, output, hook = None, invoked_by = None):

        exe = DeploymentExecution()
        exe.deployment = self
        exe.invoked_by = invoked_by
        exe.success = success
        exe.output = output
        exe.hook = hook
        exe.save()

        print "saved"



class DeploymentExecution(models.Model):

    class Meta:
        ordering = ['-run_at']

    deployment = models.ForeignKey(Deployment, related_name='executions')
    run_at = models.DateTimeField(auto_now_add=True)
    invoked_by = models.ForeignKey(User, null=True, blank=True)
    success = models.BooleanField()
    output = models.TextField()
    hook = models.ForeignKey("Hook", blank=True, null=True)

    @property
    def manual(self):
        return hook is None


KEY_LENGTH = 30

def gen_key(length=KEY_LENGTH):
    legal_chars = ['1', '2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','J','K','M','N','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    key = ''
    for i in range(length):
        key+= random.choice(legal_chars)
    return key




class Hook(models.Model):

    def save(self, *args, **kwargs):
        key = self.key
        while key == u"":
            try:
                key = gen_key()
                print key
                Hook.objects.get(key=key)
                key = u""
            except Hook.DoesNotExist:
                pass #expected
        self.key = key
        super(Hook, self).save(*args, **kwargs)  

    name = models.CharField(max_length=200)
    every_push = models.BooleanField(default = False)
    commit_message_regex = models.CharField(max_length=250, null=True, blank=True)
    project = models.ForeignKey(Project, related_name='hooks', null=True, blank=True)
    deployments = models.ManyToManyField(Deployment, related_name='hooks')

    creator = models.ForeignKey(User, null=True) 
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    key = models.CharField(max_length=200, unique = True)

    def get_absolute_url(self):
        return reverse('run-hook',args=[self.id, self.key])


    def __unicode__(self):
        try:
            return self.deployments.all()[0].name
        except:
            return "NO DEPLOYMENT"


