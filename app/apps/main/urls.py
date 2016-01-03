from django.conf.urls import patterns, url
from apps.main import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',
	url(r'^.well-known/acme-challenge/spJ9p3uQ_1kWNcv6IIwcMF_tcV8ki6yOxqYg_UI5jXA/$', views.cert, name='cert'),

	url(r'^test/$', views.test, name='test'),


	# FRONT MARKETING PAGES
	url(r'^$', views.landing, name='landing'),
	url(r'^contact/$', views.contact, name='contact'),
	url(r'^about/$', views.about, name='about'),
	url(r'^whyuseus/$', views.whyuseus, name='whyuseus'),
	url(r'^products/$', views.products, name='products'),
	url(r'^products/timetracker$', views.products_timetracker, name='products_timetracker'),
	url(r'^products/contractmanager$', views.products_contractmanager, name='products_contractmanager'),
	url(r'^products/analytics$', views.products_analytics, name='products_analytics'),


	url(r'^user/$', views.user, name='user'),
	url(r'^groups/$', views.groups, name='groups'),
	url(r'^groups/(?P<groupname>.+)/$', views.group, name='group'),
	
	url(r'^home/$', views.index, name='index'),
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
# alerts should show warning color based on level of alert
# make admin display better
# make addon template on form submit work (currently just adds to base template)



# new contract page
	# - forms display properly
	# - added template tags actually display
	# - current input field tags actually display
# edit contract page
	# - send to group/user makes popup and submits form
	# - actual templates load on right
	# - edit contract area - one tab for html, one tab from html_output
	# - inputs all loaded at top of page
# manage workflows page
	# - groups actually loaded on right
	# - ability to upload unknown number of inputs and create workflow object
	# - Dragging box adds data to input


### BIG
# figure out how to save in db (EAV, jsonb, etc)
# messaging that form has submitted
# get alert system and contract log up and running
# page for a physician to show all contracts
# Work on contract flow and adding/passing contracts along pipeline
	# 1. get contract submit and passing to work w/o js stuff
	# 2. all js on contract create page done
	# 3. js and submitting on current contracts done


# PLAN
# finish new and edit contract pages
# finish workflow pages
# get database setup
# get analytics up and running





# look into task runner to drop and add database

#### DROP/ADD DB Instructions
# All in terminal
# 1. dropdb cmdb
# 2. createdb cmdb
# 3. python manage.py migrate auth
# 4. python manage.py migrate
# 5. python manage.py createsuperuser --username=joe --email=joe@example.com

#### DROP/ADD DB Instructions in Heroku
# 1. heroku pg:reset DATABASE_URL
# 2. heroku run python manage.py migrate auth
# 3. heroku run python manage.py migrate
# 4. 



########## DEPLOYMENT ISSUES

# make sure app can view env varianbles -- especially for superuser creation password
# make sure no errors on fresh install (related to pythonpath and wsgipath)