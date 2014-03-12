from django.contrib import admin

from deployments.models import *

# Register your models here.
# 
# 
admin.site.register(Project)
admin.site.register(Deployment)
admin.site.register(Hook)
admin.site.register(DeploymentEvent)
