from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
import models




def test(request):
	context= {}
	return render(request, 'main/test.html', context)

@login_required
def index(request):
	context= {}
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
	context= {}
	return render(request, 'main/group.html', context)

@login_required
def newcontract(request):
	all_templates = models.Template.objects.filter(system=request.user.userprofile.system)
	addon_templates = all_templates.filter(add_on=True)
	base_templates = all_templates.filter(add_on=False)

	context= {'addon_templates':addon_templates, 'base_templates':base_templates}
	return render(request, 'main/newcontract.html', context)

@login_required
def allcontracts(request):
	context= {}
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
	context= {}
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
	context= {'alerts':alerts}
	return render(request, 'main/alerts.html', context)

@login_required
def alerthistory(request):
	alerts = models.Alert.objects.filter(user=request.user, active=False)
	context= {'alerts':alerts}
	return render(request, 'main/alerts.html', context)

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

	context= {'form':form, 'sites':sites}
	return render(request, 'main/addsite.html', context)

@login_required
def settings(request):
	context= {}
	return render(request, 'main/settings.html', context)