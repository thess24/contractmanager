from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
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
	teams = models.Team.objects.filter(system=request.user.userprofile.system)

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
	print contractform
	print contractinfoform

	if request.method=='POST':
		print request.POST
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

@login_required
def allcontracts(request):
	contracts = models.ContractInfo.objects.filter(contract__system=request.user.userprofile.system)


	context= {'contracts':contracts}
	return render(request, 'main/allcontracts.html', context)

@login_required
def analyzecontracts(request):
	context= {}
	return render(request, 'main/analyzecontracts.html', context)

@login_required
def contractsexpiration(request):
	context= {}
	return render(request, 'main/contractsexpiration.html', context)

@login_required
def contractsprogress(request):
	context= {}
	return render(request, 'main/contractsprogress.html', context)

@login_required
def compensationcompare(request):
	context= {}
	return render(request, 'main/compensationcompare.html', context)

@login_required
def diffcontracts(request, contractid1, contractid2):
	context= {'contractid1':contractid1, 'contractid2': contractid2}
	return render(request, 'main/diffcontracts.html', context)

@login_required
def editcontract(request, contractid):
	context= {}
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