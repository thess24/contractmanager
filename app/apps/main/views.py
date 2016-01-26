from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Count, Sum
import models
import datetime




def test(request):
	context= {}
	return render(request, 'main/test.html', context)

def landing(request):
	context= {}
	return render(request, 'main/landing.html', context)

def contact(request):
	form = models.ContactUsForm()

	if request.method=='POST':
		form = models.ContactUsForm(request.POST)
		if form.is_valid():
			form.save()

			print 'FAKE SEND EMAIL'

			return HttpResponseRedirect(reverse('contact'))

	context= {'form':form}
	return render(request, 'main/contact.html', context)

def about(request):
	context= {}
	return render(request, 'main/about.html', context)

def products(request):
	context= {}
	return render(request, 'main/products.html', context)

def whyuseus(request):
	context= {}
	return render(request, 'main/whyuseus.html', context)


def products_analytics(request):
	context= {}
	return render(request, 'main/products_analytics.html', context)

def products_timetracker(request):
	context= {}
	return render(request, 'main/products_timetracker.html', context)

def products_contractmanager(request):
	context= {}
	return render(request, 'main/products_contractmanager.html', context)














@login_required
def index(request):
	checked_out_contracts = models.ContractInfo.objects.filter(current_user=request.user)
	contract_history = models.ContractInfo.objects.filter(current_user=request.user)

	if request.method=='POST':
		print request.POST
		if 'checkin_contract' in request.POST:
			cid = request.POST.get('contractid')
			checked_in_contract = models.ContractInfo.objects.get(id=cid)
			checked_in_contract.current_user = None
			checked_in_contract.grabbed_at = None
			checked_in_contract.save()

			return HttpResponseRedirect(reverse('index'))

	context= {'checked_out_contracts':checked_out_contracts,'contract_history':contract_history}
	return render(request, 'main/index.html', context)

@login_required
def user(request):
	context= {}
	return render(request, 'main/user.html', context)

@login_required
def groups(request):
	teams = models.UserProfile.objects.filter(system=request.user.userprofile.system).values('team__name', 'team__description').annotate(user_count=Count('user'))

	# query count of all contracts in each team currently 

	context= {'teams':teams}
	return render(request, 'main/groups.html', context)

@login_required
def group(request, groupname):
	team = get_object_or_404(models.Team, system=request.user.userprofile.system, name=groupname)
	contracts = models.ContractInfo.objects.filter(current_team=team)
	team_members = models.UserProfile.objects.filter(team=team)

	if request.method=='POST':
		print request.POST
		if 'grab_contract' in request.POST:
			for cid in  request.POST.getlist('grabbed_contract'):
				grabbed_contract = models.ContractInfo.objects.get(id=cid)
				grabbed_contract.current_user = request.user
				grabbed_contract.grabbed_at = datetime.datetime.now()
				grabbed_contract.save()
				print grabbed_contract

			return HttpResponseRedirect(reverse('group', args=(groupname,)))

	context= {'contracts':contracts, 'team':team, 'team_members':team_members}
	return render(request, 'main/group.html', context)

@login_required
def newcontract(request):
	all_templates = models.Template.objects.filter(system=request.user.userprofile.system)
	addon_templates = all_templates.filter(add_on=True)
	base_templates = all_templates.filter(add_on=False)

	contractform = models.ContractForm()
	contractinfoform = models.ContractInfoForm()

	if request.method=='POST':
		# print request.POST
		if 'add_contract' in request.POST:
			contractform = models.ContractForm(request.POST)
			contractinfoform = models.ContractInfoForm(request.POST)
			if all([contractform.is_valid(), contractinfoform.is_valid()]):
				contract = contractform.save(commit=False)
				contract.system = request.user.userprofile.system
				contract.created_by = request.user
				contract.save()



				contractinfo = contractinfoform.save(commit=False)
				# if not contractinfo.next_team:
					# raise some error here and send back to form


				contractinfo.contract = contract
				contractinfo.version = 1
				contractinfo.sent_at = datetime.datetime.now()

				contractinfo.current_team = contractinfo.next_team
				contractinfo.current_user = contractinfo.next_user
				contractinfo.prev_team = request.user.userprofile.team
				contractinfo.prev_user = request.user

				contractinfo.save()



				alert_string = 'You have a new contract ready for review!'
				alert_user = contractinfo.current_user
				alert = models.Alert.objects.create(user=alert_user, contract=contract, name=alert_string)


				return HttpResponseRedirect(reverse('newcontract'))


	context= {'addon_templates':addon_templates, 'base_templates':base_templates, 'contractform':contractform, 'contractinfoform': contractinfoform}
	return render(request, 'main/newcontract.html', context)




##### ANALYTICS AREA #####

@login_required
def allcontracts(request):
	contracts = models.ContractInfo.objects.filter(contract__system=request.user.userprofile.system)

	context= {'contracts':contracts}
	return render(request, 'main/allcontracts.html', context)

@login_required
def analytics_dollar_value(request):
	context= {}
	return render(request, 'main/analytics_dollar_value.html', context)

@login_required
def analytics_expiration(request):
	context= {}
	return render(request, 'main/analytics_expiration.html', context)

@login_required
def analytics_physician_compare(request):
	context= {}
	return render(request, 'main/analytics_physician_compare.html', context)

@login_required
def analytics_physician_view(request):
	context= {}
	return render(request, 'main/analytics_physician_view.html', context)

@login_required
def analytics_service_lines(request):
	context= {}
	return render(request, 'main/analytics_service_lines.html', context)

@login_required
def analytics_sites(request):
	context= {}
	return render(request, 'main/analytics_sites.html', context)

@login_required
def analytics_snapshot(request):
	context= {}
	return render(request, 'main/analytics_snapshot.html', context)

@login_required
def contractsprogress(request):
	context= {}
	return render(request, 'main/contractsprogress.html', context)


@login_required
def analyzecontracts(request):
	context= {}
	return render(request, 'main/analyzecontracts.html', context)


######################## END ANALYTICS AREA  #######################




@login_required
def diffcontracts(request, contractid1, contractid2):
	context= {'contractid1':contractid1, 'contractid2': contractid2}
	return render(request, 'main/diffcontracts.html', context)

@login_required
def editcontract(request, contractid):
	contract = get_object_or_404(models.Contract, id=contractid)
	contract_versions = models.ContractInfo.objects.filter(contract=contract).order_by('-created_at')
	latest_contract = contract_versions.latest('created_at')
	contractinfoform = models.ContractInfoForm(instance=latest_contract)


	context= {'latest_contract':latest_contract, 'contract_versions':contract_versions, 'contractinfoform':contractinfoform}
	return render(request, 'main/editcontract.html', context)

@login_required
def contract(request, contractid):
	contract = get_object_or_404(models.Contract, id=contractid)
	contract_versions = models.ContractInfo.objects.filter(contract=contract).order_by('-created_at')
	latest_contract = contract_versions.latest('created_at')

	context= {'latest_contract':latest_contract, 'contract_versions':contract_versions}
	return render(request, 'main/contract.html', context)

@login_required
def workflows(request):
	context= {}
	return render(request, 'main/workflows.html', context)

@login_required
def addworkflow(request):
	context= {}
	return render(request, 'main/addworkflow.html', context)

@login_required
def alerts(request):
	alerts = models.Alert.objects.filter(user=request.user, active=True)

	if request.method=='POST':
		if 'mark_handled' in request.POST:
			alert_id = request.POST.get('alert_id')
			alert = models.Alert.objects.get(id=alert_id)
			alert.active = False
			alert.save()

			return HttpResponseRedirect(reverse('alerts'))

	context= {'alerts':alerts}
	return render(request, 'main/alerts.html', context)

@login_required
def alerthistory(request):
	alerts = models.Alert.objects.filter(user=request.user, active=False)
	context= {'alerts':alerts}
	return render(request, 'main/alertshistory.html', context)

@login_required
def alertmanage(request):
	alerts = models.Alert.objects.filter(user=request.user, active=False)
	context= {'alerts':alerts}
	return render(request, 'main/alertmanage.html', context)

@login_required
def addtemplate(request):
	templates = models.Template.objects.filter(system=request.user.userprofile.system)
	form = models.TemplateForm()

	if request.method=='POST':
		if 'add_template' in request.POST:
			form = models.TemplateForm(request.POST)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.system = request.user.userprofile.system
				instance.save()

				return HttpResponseRedirect(reverse('addtemplate'))

	context= {'form':form, 'templates':templates}	
	return render(request, 'main/addtemplate.html', context)

@login_required
def viewtemplates(request):
	context= {}
	return render(request, 'main/viewtemplates.html', context)

@login_required
def addteam(request):
	teams = models.Team.objects.filter(system=request.user.userprofile.system)
	form = models.TeamForm()

	if request.method=='POST':
		if 'addteam' in request.POST:
			form = models.TeamForm(request.POST)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.system = request.user.userprofile.system
				instance.save()	

				return HttpResponseRedirect(reverse('addteam'))

	context= {'form':form, 'teams':teams}
	return render(request, 'main/addteam.html', context)

@login_required
def adduser(request):
	users = models.UserProfile.objects.filter(system=request.user.userprofile.system)
	extuserform = models.ExtendedUserCreateForm()
	userprofileform = models.UserProfileForm()

	if request.method=='POST':
		if 'add_user' in request.POST:
			extuserform = models.ExtendedUserCreateForm(request.POST)
			userprofileform = models.UserProfileForm(request.POST)

			if all([userprofileform.is_valid(), extuserform.is_valid()]):
				user = extuserform.save()

				instance = userprofileform.save(commit=False)
				instance.user = user
				instance.system = request.user.userprofile.system
				instance.save()
				
				return HttpResponseRedirect(reverse('adduser'))

	context= {'users':users, 'userprofileform':userprofileform, 'extuserform':extuserform}
	return render(request, 'main/adduser.html', context)

@login_required
def addphysician(request):
	doctors = models.Physician.objects.filter(system=request.user.userprofile.system)
	extuserform = models.ExtendedUserCreateForm()
	physicianform = models.PhysicianForm()

	if request.method=='POST':
		if 'addphysician' in request.POST:
			extuserform = models.ExtendedUserCreateForm(request.POST)
			physicianform = models.PhysicianForm(request.POST)

			if all([physicianform.is_valid(), extuserform.is_valid()]):
				user = extuserform.save()

				instance = physicianform.save(commit=False)
				instance.system = request.user.userprofile.system
				instance.user = user
				instance.save()

				return HttpResponseRedirect(reverse('addphysician'))

	context = {'doctors':doctors, 'physicianform':physicianform, 'extuserform':extuserform}
	return render(request, 'main/addphysician.html', context)

@login_required
def addphysiciangroup(request):
	physician_groups = models.PhysicianGroup.objects.filter(system = request.user.userprofile.system)
	form = models.PhysicianGroupForm()

	if request.method=='POST':
		if 'add_physician_group' in request.POST:
			form = models.PhysicianGroupForm(request.POST)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.system = request.user.userprofile.system
				instance.save()
				
				return HttpResponseRedirect(reverse('addphysiciangroup'))

	context= {'physician_groups':physician_groups, 'form':form}				
	return render(request, 'main/addphysiciangroup.html', context)

@login_required
def addsite(request):
	sites = models.HealthSite.objects.filter(system = request.user.userprofile.system)
	form = models.HealthSiteForm()

	if request.method=='POST':
		if 'addsite' in request.POST:
			form = models.HealthSiteForm(request.POST)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.system = request.user.userprofile.system
				instance.save()

				return HttpResponseRedirect(reverse('addsite'))

	context = {'form':form, 'sites':sites}
	return render(request, 'main/addsite.html', context)

@login_required
def settings(request):
	context = {}
	return render(request, 'main/settings.html', context)



@login_required
def allphysicians(request):
	physicians = models.Physician.objects.filter(system=request.user.userprofile.system)

	context= {'physicians':physicians}		
	return render(request, 'main/allphysicians.html', context)

@login_required
def viewphysician(request,npi):
	physician = get_object_or_404(models.Physician, system=request.user.userprofile.system, npi=npi)

	context= {'physician':physician}		
	return render(request, 'main/physician.html', context)

@login_required
def timesheets_view(request):
	timesheets = models.PhysicianTimeLog.objects\
		.extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)"})\
		.values('category','month','year','physician__user__first_name','physician__user__last_name','physician__npi', 'created_at')\
		.annotate(time_sum=Sum('mins_worked'))


	context= {'timesheets':timesheets}		
	return render(request, 'main/timesheets_view.html', context)

@login_required
def timesheets_approve_view(request):
	timesheets = models.PhysicianTimeLogPeriod.objects.filter(current_user=request.user, active=True, approved_at__isnull=True)

	if request.method=='POST':
		if 'approvetimesheet' in request.POST:

			timesheetperiod_id = request.POST.get('timesheetperiod_id')
			ts = timesheets.get(id=timesheetperiod_id)
			ts.approval_num += 1

			wf_id = ts.workflow.id
			wf_items = models.WorkflowItem.objects.filter(workflow__id=wf_id)

			# should move the .count to the database level to speed things up
			if wf_items.count() == ts.approval_num: 
				# if this item has been approved the same number of times as the number of steps in the workflow,
				# then this is the final step of approval
				ts.approved_by = request.user
				ts.approved_at = datetime.datetime.now()
				ts.save()

			else:
				next_user = wf_items.get(position=ts.approval_num).user
				ts.current_user = next_user
				ts.save()


			ptla = models.PhysicianTimeLogApproval(user=request.user, physiciantimelogperiod=ts)
			ptla.save()


			return HttpResponseRedirect(reverse('timesheets_approve_view'))


	context= {'timesheets':timesheets}		
	return render(request, 'main/timesheets_approve_view.html', context)

@login_required
def timesheets_by_physician(request):
	timesheets = models.PhysicianTimeLog.objects\
		.extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)"})\
		.values('category','month','year','physician__user__first_name','physician__user__last_name','physician__npi', 'created_at')\
		.annotate(time_sum=Sum('mins_worked'))

	physicians = models.Physician.objects.all()


	context= {'timesheets':timesheets, 'physicians':physicians}		
	return render(request, 'main/timesheets_by_physician.html', context)

@login_required
def timesheets_physician_add(request):
	physician = get_object_or_404(models.Physician, user=request.user)
	form = models.PhysicianTimeLogForm()
	tsperiods = models.PhysicianTimeLogPeriod.objects.filter(physician=physician, active=True)

	if request.method=='POST':
		if 'addtimesheet' in request.POST:
			form = models.PhysicianTimeLogForm(request.POST)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.physician = physician

				# send error to form if physlog is locked (because its submitted for approval)
				period = datetime.date(instance.date.year,instance.date.month,1)
				tsperiod = tsperiods.filter(period=period)

				if tsperiod:
					form.add_error(None,'Cannot submit a time for this date -- you have already submitted your time sheet for this time period')
					context= {'form':form, 'physician':physician}		
					return render(request, 'main/timesheets_physician_add.html', context)

				instance.save()

				return HttpResponseRedirect(reverse('timesheets_view'))


	context= {'form':form, 'physician':physician}		
	return render(request, 'main/timesheets_physician_add.html', context)

@login_required
def timesheets_physician_edit(request,timesheetid):
	physician = get_object_or_404(models.Physician, user=request.user)
	timesheet_to_edit = get_object_or_404(models.PhysicianTimeLog, id=timesheetid, physician=physician, active=True)
	# import ipdb;ipdb.set_trace()
	ts_date = datetime.date(timesheet_to_edit.date.year,timesheet_to_edit.date.month,1)
	tsperiod = models.PhysicianTimeLogPeriod.objects.filter(physician=physician,period=ts_date)

	form = models.PhysicianTimeLogForm(instance=timesheet_to_edit)

	if request.method=='POST':
		if 'edittimesheet' in request.POST:
			form = models.PhysicianTimeLogForm(request.POST, instance=timesheet_to_edit)
			if form.is_valid():
				if tsperiod.filter(active=False) and not tsperiod.filter(active=True):
					# timesheets have been denied before for this time period - and no new sheets have been submitted
					# 'editing' is done by making original inactive and copying data to new one
					timesheet_to_edit.active = False
					timesheet_to_edit.save()

					timesheet_to_edit.pk = None
					timesheet_to_edit.active = True
					timesheet_to_edit.save()

					# need to created new phystimelog model here with same attributes as form


					
				elif tsperiod.filter(active=True):
					# timesheets have been submitted, but not denied -- cant edit, raise error
					form.add_error(None,'Cannot edit this -- you have already submitted a time sheet.')
					context= {'form':form, 'physician':physician}		
					return render(request, 'main/timesheets_physician_edit.html', context)

				else:
					# there is no timesheet awaiting approval, you can actually edit it
					instance = form.save(commit=False)
					instance.save()

				return HttpResponseRedirect(reverse('timesheets_view'))

		if 'deletetimesheet' in request.POST:
			if tsperiod.filter(active=False) and not tsperiod.filter(active=True):
				# timesheets have been denied before for this time period - and no new sheets have been submitted
				timesheet_to_edit.active=False
				timesheet_to_edit.save()
				
			elif tsperiod.filter(active=True):
				# timesheets have been submitted, but not denied -- cant delete, raise error
				form.add_error(None,'Cannot delete this -- you have already submitted a time sheet.')
				context= {'form':form, 'physician':physician}		
				return render(request, 'main/timesheets_physician_edit.html', context)

			else:
				# there is no timesheet awaiting approval, you can actually delete it
				timesheet_to_edit.delete()

			return HttpResponseRedirect(reverse('timesheets_view'))


	context= {'form':form, 'physician':physician}		
	return render(request, 'main/timesheets_physician_edit.html', context)

@login_required
def timesheets_physician_view_periods(request):
	physician = get_object_or_404(models.Physician, user=request.user)
	tsperiods = models.PhysicianTimeLogPeriod.objects.filter(physician=physician, active=True)

	timesheets = models.PhysicianTimeLog.objects\
		.filter(physician=physician)\
		.extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)"})\
		.values('month','year')\
		.annotate(time_sum=Sum('mins_worked'))

	context= {'physician':physician, 'timesheets':timesheets, 'tsperiods':tsperiods}		
	return render(request, 'main/timesheets_physician_view_periods.html', context)

@login_required
def timesheets_physician_one_period(request, month, year):
	monthyearperiod = '{}-{}'.format(month,year)
	try:
		period = datetime.datetime.strptime(monthyearperiod,'%m-%Y')
	except ValueError:
		raise Http404

	physician = get_object_or_404(models.Physician, user=request.user)
	tsperiod = models.PhysicianTimeLogPeriod.objects.filter(period=period, physician=physician, active=True)
	timesheets = models.PhysicianTimeLog.objects.filter(physician=physician, date__year=period.year, date__month=period.month, active=True)

	timesheet_agg = models.PhysicianTimeLog.objects\
		.filter(physician=physician, date__year=period.year, date__month=period.month,active=True)\
		.values('category')\
		.annotate(time_sum=Sum('mins_worked'), sheet_count=Count('mins_worked'))

	if request.method=='POST':
		if 'submittimesheet' in request.POST:
			if tsperiod: 
				# probably should handle this better-this would be if there is a timelogperiod that alerady exists
				# client side will make it hard to submit if this exists, so this is just in case
				raise Http404  

			for ts in timesheet_agg:
				try:
					# import ipdb;ipdb.set_trace()
					category = models.ContractType.objects.get(name=ts['category'])
					instance = models.PhysicianTimeLogPeriod(physician=physician, mins_worked=ts['time_sum'], period=period.date(), category=category)
					instance.save()
				except:
					# this needs to be handled -- this should never happen if the category is correct
					print 'error'
					pass

			return HttpResponseRedirect(reverse('timesheets_physician_one_period', args=(month,year)))

	context= {'physician':physician, 'timesheets':timesheets, 'period':period, 'timesheet_agg':timesheet_agg, 'tsperiod':tsperiod}		
	return render(request, 'main/timesheets_physician_one_period.html', context)
	