from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    

    url(r'^add-project$', 'deployments.views.projects.add_project', name='add-project'),
    
    # url(r'^', 'frontend.views.home.home',name='home'),
    
    url(r'^project/(?P<project_id>\d*)$','deployments.views.projects.project', name="project"),
    url(r'^project/(?P<project_id>\d*)/add-hook$','deployments.views.hooks.add_hook', name="add-hook"),
    url(r'^project/edit-hook/(?P<hook_id>\d*)$','deployments.views.hooks.edit_hook', name="edit-hook"),
    
    url(r'^project/(?P<project_id>\d*)/add-deployment$', 'deployments.views.deploy.add_deployment', name='add-deployment'),
    url(r'^project/(?P<project_id>\d*)/delete$', 'deployments.views.projects.delete_project', name='delete_project'),
    url(r'^deployment/(?P<deployment_id>\d*)/edit$', 'deployments.views.deploy.edit_deployment', name='edit-deployment'),
    url(r'^deployment/(?P<deployment_id>\d*)/delete$', 'deployments.views.deploy.delete_deployment', name='delete_deployment'),
    url(r'^deployment/(?P<deployment_id>\d*)/run$', 'deployments.views.deploy.run_deployment', name='run-deployment'),
    url(r'^deployment/(?P<deployment_id>\d*)/past-deployments$', 'deployments.views.deploy.past_deployments', name='show-past-deployments'),


    #url(r'^deployment/(?P<deployment_id>\d*)/git_test$', 'deployments.views.deploy.git_test', name='git-test-deployment'),

    url(r'^test-connection$','deployments.views.deploy.test_connection', name="test_connection"),

    
    url(r'^hook/(?P<hook_id>\d*)/run/(?P<key>\w*)$', 'deployments.views.deploy.run_hook', name="run-hook"),
    url(r'^hook/(?P<hook_id>\d*)/delete$', 'deployments.views.hooks.delete_hook', name="delete_hook"),
    
    
    # url(r'^admin/', include(admin.site.urls)),
)
