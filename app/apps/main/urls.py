from django.conf.urls import patterns, url
from apps.main import views
from django.conf import settings
from django.conf.urls.static import static


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
	# phys
	# physgroup
	# users
# filter people you can add based on system they are in
# make forms look good
# ability for admin to reset user password
# finish addtemplate html file- modal popup from ajax, copy data on load, render on pageup
# fix footer
# authentication/security on api
# page for a physician to show all contracts
# page to add contracts
# redirect all pages to proper areas
# alerts should show warning color based on level of alert
# password reset html


# dont allow creating accounts at signin page
