from django.conf.urls import patterns, url
from apps.main import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',
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


	# INTERNAL APPLICATION PAGES
	url(r'^user/$', views.user, name='user'),
	url(r'^groups/$', views.groups, name='groups'),
	url(r'^groups/(?P<groupname>.+)/$', views.group, name='group'),
	
	url(r'^home/$', views.index, name='index'),
	url(r'^contracts/new/$', views.newcontract, name='newcontract'),
	url(r'^contracts/all/$', views.allcontracts, name='allcontracts'),

	url(r'^physician/new$', views.addphysician, name='addphysician'),
	url(r'^physician/all/$', views.allphysicians, name='allphysicians'),
	url(r'^physician/group/new/$', views.addphysiciangroup, name='addphysiciangroup'),
	url(r'^physician/(?P<npi>.+)/$', views.viewphysician, name='viewphysician'),

	url(r'^analyze/$', views.analyzecontracts, name='analyzecontracts'),
	url(r'^analyze/progress/$', views.contractsprogress, name='contractsprogress'),
	url(r'^analyze/physiciancompare/$', views.analytics_physician_compare, name='analytics_physician_compare'),
	url(r'^analyze/expiration/$', views.analytics_expiration, name='analytics_expiration'),
	url(r'^analyze/dollarvalue/$', views.analytics_dollar_value, name='analytics_dollar_value'),
	url(r'^analyze/physician/$', views.analytics_physician_view, name='analytics_physician_view'),
	url(r'^analyze/servicelines/$', views.analytics_service_lines, name='analytics_service_lines'),
	url(r'^analyze/sites/$', views.analytics_sites, name='analytics_sites'),
	url(r'^analyze/snapshot/$', views.analytics_snapshot, name='analytics_snapshot'),


	url(r'^contracts/diff/(?P<contractid1>.+)/(?P<contractid2>.+)/$', views.diffcontracts, name='diffcontracts'),
	url(r'^contracts/(?P<contractid>.+)/edit$', views.editcontract, name='editcontract'),
	url(r'^contracts/(?P<contractid>.+)/$', views.contract, name='contract'),


	url(r'^workflows/$', views.workflows, name='workflows'),
	url(r'^workflows/add/$', views.addworkflow, name='addworkflow'),


	url(r'^alerts/$', views.alerts, name='alerts'),
	url(r'^alerts/history$', views.alerthistory, name='alerthistory'),
	url(r'^alerts/manage$', views.alertmanage, name='alertmanage'),


	url(r'^addtemplate/$', views.addtemplate, name='addtemplate'),
	url(r'^viewtemplates/$', views.viewtemplates, name='viewtemplates'),


	url(r'^addteam/$', views.addteam, name='addteam'),
	url(r'^adduser/$', views.adduser, name='adduser'),
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




########## DEPLOYMENT ISSUES

# make sure app can view env varianbles -- especially for superuser creation password
# make sure no errors on fresh install (related to pythonpath and wsgipath)
# make sure copying of http config apache stuff works
# make https://baldurhealthcare.com work
# add hsts header in /etc/httpd/wsgi.conf



# RewriteEngine On
# RewriteCond %{HTTP:X-Forwarded-Proto} !https
# RewriteRule / https://%{SERVER_NAME}%{REQUEST_URI} [L,R=301]

# Header always set Strict-Transport-Security "max-age=3000; includeSubDomains"
