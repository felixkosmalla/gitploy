from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gitlab_deployment.views.home', name='home'),
    url(r'^', include('frontend.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^jsreverse/$', 'django_js_reverse.views.urls_js', name='js_reverse'),

)
