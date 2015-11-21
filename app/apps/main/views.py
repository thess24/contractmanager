from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
import models





def test(request):
	context= {}
	return render(request, 'main/test.html', context)

def index(request):
	context= {}
	return render(request, 'main/index.html', context)

def user(request):
	context= {}
	return render(request, 'main/user.html', context)

def groups(request):
	teams = models.Team.objects.filter(system=request.user.userprofile.system)

	context= {'teams':teams}
	return render(request, 'main/groups.html', context)

def group(request, groupname):
	context= {}
	return render(request, 'main/group.html', context)

def newcontract(request):
	all_templates = models.Template.objects.filter(system=request.user.userprofile.system)
	addon_templates = all_templates.filter(add_on=True)
	base_templates = all_templates.filter(add_on=False)

	context= {'addon_templates':addon_templates, 'base_templates':base_templates}
	return render(request, 'main/newcontract.html', context)

def allcontracts(request):
	context= {}
	return render(request, 'main/allcontracts.html', context)

def analyzecontracts(request):
	context= {}
	return render(request, 'main/analyzecontracts.html', context)

def contractsexpiration(request):
	context= {}
	return render(request, 'main/contractsexpiration.html', context)

def contractsprogress(request):
	context= {}
	return render(request, 'main/contractsprogress.html', context)

def compensationcompare(request):
	context= {}
	return render(request, 'main/compensationcompare.html', context)

def diffcontracts(request, contractid1, contractid2):
	context= {'contractid1':contractid1, 'contractid2': contractid2}
	return render(request, 'main/diffcontracts.html', context)

def editcontract(request, contractid):
	context= {}
	return render(request, 'main/editcontract.html', context)

def contract(request, contractid):
	context= {}
	return render(request, 'main/contract.html', context)

def workflows(request):
	context= {}
	return render(request, 'main/workflows.html', context)

def addworkflow(request):
	context= {}
	return render(request, 'main/addworkflow.html', context)

def alerts(request):
	alerts = models.Alert.objects.filter(user=request.user, active=True)
	context= {'alerts':alerts}
	return render(request, 'main/alerts.html', context)

def alerthistory(request):
	alerts = models.Alert.objects.filter(user=request.user, active=False)
	context= {'alerts':alerts}
	return render(request, 'main/alerts.html', context)

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

def viewtemplates(request):
	context= {}
	return render(request, 'main/viewtemplates.html', context)

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

# def addphysician(request):
# 	doctors = models.Physician.objects.filter(system=request.user.userprofile.system)
# 	userform = UserCreationForm()
# 	namesform = models.NamesForm()
# 	physicianform = models.PhysicianForm()

# 	if request.method=='POST':
# 		if 'addphysician' in request.POST:
# 			userform = UserCreationForm(request.POST)
# 			namesform = models.NamesForm(request.POST)
# 			physicianform = models.PhysicianForm(request.POST)

# 			if all([physicianform.is_valid(), userform.is_valid(), namesform.is_valid()]):
# 				user = userform.save(commit=False)
# 				user.first_name = namesform.cleaned_data['first_name']
# 				user.last_name = namesform.cleaned_data['last_name']
# 				user.email = namesform.cleaned_data['email']
# 				user.save()

# 				instance = physicianform.save(commit=False)
# 				instance.system = request.user.userprofile.system
# 				instance.user = user
# 				instance.save()

# 	context = {'doctors':doctors, 'physicianform':physicianform, 'namesform':namesform, 'userform':userform}
# 	return render(request, 'main/addphysician.html', context)

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

def settings(request):
	context= {}
	return render(request, 'main/settings.html', context)