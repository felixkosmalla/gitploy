from deployments.models import *

def projects(request):

    return {
        'projects':Project.objects.all()
    }