from django.conf.urls import patterns, url
from apps.main import views
from django.conf import settings
from django.conf.urls.static import static
from settings.common import MEDIA_ROOT 


urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^test/$', views.test, name='test'),

	url(r'^user/$', views.user, name='user'),
	url(r'^groups/$', views.groups, name='groups'),
	url(r'^groups/(?P<groupname>.+)/$', views.group, name='group'),
	
	url(r'^contracts/new/$', views.newcontract, name='newcontract'),
	url(r'^contracts/all/$', views.allcontracts, name='allcontracts'),

	url(r'^contracts/analyze/$', views.analyzecontracts, name='analyzecontracts'),
	url(r'^contracts/analyze/expiration/$', views.contractsexpiration, name='contractsexpiration'),
	url(r'^contracts/analyze/progress/$', views.contractsprogress, name='contractsprogress'),
	url(r'^contracts/analyze/compensation/$', views.compensationcompare, name='compensationcompare'),

	url(r'^contracts/diff/(?P<contractid1>.+)/(?P<contractid2>.+)/$', views.diffcontracts, name='diffcontracts'),
	url(r'^contracts/(?P<contractid>.+)/edit$', views.editcontract, name='editcontract'),
	url(r'^contracts/(?P<contractid>.+)/$', views.contract, name='contract'),

	url(r'^workflows/$', views.workflows, name='workflows'),
	url(r'^workflows/add/$', views.addworkflow, name='addworkflow'),

	url(r'^alerts/$', views.alerts, name='alerts'),
	url(r'^alerts/history$', views.alerthistory, name='alerthistory'),

	url(r'^addtemplate/$', views.addtemplate, name='addtemplate'),
	url(r'^viewtemplates/$', views.viewtemplates, name='viewtemplates'),

	

	url(r'^addteam/$', views.addteam, name='addteam'),
	url(r'^adduser/$', views.adduser, name='adduser'),
	url(r'^addphysician/$', views.addphysician, name='addphysician'),
	url(r'^addphysiciangroup/$', views.addphysiciangroup, name='addphysiciangroup'),
	url(r'^addsite/$', views.addsite, name='addsite'),


	url(r'^settings/$', views.settings, name='settings'),

)





################## TODO #################

# edit / delete of...
	# sites
	# teams
# filter people you can add based on system they are in
# make forms look good
# physician form is takes two forms and adds them together
