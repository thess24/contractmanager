from django.contrib import admin
from django.conf.urls import patterns, include, url
from apps.main.api import PhysicianResource, PhysicianTimeLogResource, UserResource, PhysicianAlertResource, PhysicianTimeLogCategoryResource
from tastypie.api import Api
from django.views.generic import TemplateView
from axes.decorators import watch_login
from allauth.account.views import login 


admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(PhysicianResource())
v1_api.register(PhysicianTimeLogResource())
v1_api.register(UserResource())
v1_api.register(PhysicianAlertResource())
v1_api.register(PhysicianTimeLogCategoryResource())





urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', watch_login(login)),
    (r'^accounts/', include('allauth.urls')),
    url(r'session_security/', include('session_security.urls')),
    (r'^sitemap.xml$',TemplateView.as_view(template_name='sitemap.xml', content_type='text/xml')),
    url(r'^api/', include(v1_api.urls)),
    url(r'', include('apps.main.urls')),
)
