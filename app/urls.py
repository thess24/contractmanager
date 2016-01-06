from django.contrib import admin
from django.conf.urls import patterns, include, url
from apps.main.api import PhysicianResource, PhysicianTimeLogResource, UserResource
from tastypie.api import Api
from django.views.generic import TemplateView

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(PhysicianResource())
v1_api.register(PhysicianTimeLogResource())
v1_api.register(UserResource())


urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('allauth.urls')),
    (r'^sitemap.xml$',TemplateView.as_view(template_name='sitemap.xml', content_type='text/xml')),
    url(r'^api/', include(v1_api.urls)),
    url(r'', include('apps.main.urls')),
)
 