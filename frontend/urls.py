from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'frontend.views.default.index', name='index'),

    url(r'^login$', 'frontend.views.default.login', name='login'),
    # url(r'^', 'frontend.views.home.home',name='home'),
    
    url(r'^logout$', 'frontend.views.default.logout', name='logout'),

	url(r'^profile$', 'frontend.views.profile.profile', name='profile'),
	url(r'^profile/validate_token$', 'frontend.views.profile.validate_token', name='validate_token'),
    

    
    
    # url(r'^admin/', include(admin.site.urls)),
)
