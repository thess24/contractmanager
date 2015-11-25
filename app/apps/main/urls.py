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
# page to add contracts
# alerts should show warning color based on level of alert

### BIG
# redirect all pages to proper areas
# figure out how to save in db
# get alert system and contract log up and running
# page for a physician to show all contracts
# Work on contract flow and adding/passing contracts along pipeline
	# 1. get contract submit and passing to work w/o js stuff
	# 2. all js on contract create page done
	# 3. js and submitting on current contracts done


# look into task runner to drop and add database

#### DROP/ADD DB Instructions
# All in terminal
# 1. dropdb cmdb
# 2. createdb cmdb
# 3. python manage.py migrate auth
# 4. python manage.py migrate
# 5. python manage.py createsuperuser --username=joe --email=joe@example.com