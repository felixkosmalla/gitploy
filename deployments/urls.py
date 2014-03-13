from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    

    url(r'^add-project$', 'deployments.views.projects.add_project', name='add-project'),
    
    # url(r'^', 'frontend.views.home.home',name='home'),
    
    url(r'^project/(?P<project_id>\d*)$','deployments.views.projects.project', name="project"),
    
    url(r'^project/(?P<project_id>\d*)/add-deployment$', 'deployments.views.deploy.add_deployment', name='add-deployment'),
    url(r'^deployment/(?P<deployment_id>\d*)/edit$', 'deployments.views.deploy.edit_deployment', name='edit-deployment'),
    url(r'^deployment/(?P<deployment_id>\d*)/run$', 'deployments.views.deploy.run_deployment', name='run-deployment'),

    

    
    
    # url(r'^admin/', include(admin.site.urls)),
)
