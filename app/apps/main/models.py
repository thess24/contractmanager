from django.db import models
from django.forms import ModelForm, Textarea
from django import forms
from django.contrib.auth.models import User
import os
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm


 
class HealthSystem(models.Model):
	name = models.CharField(max_length=100)
	street = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=30)
	zipcode = models.CharField(max_length=5)
	created_at = models.DateTimeField(auto_now_add=True)
	logo = models.ImageField(upload_to='logos', blank=True, null=True)
	shorthand = models.CharField(max_length=6)

	def __unicode__(self):
		return self.name

class HealthSite(models.Model):
	name = models.CharField(max_length=100)
	system = models.ForeignKey(HealthSystem)
	street = models.CharField(max_length=100, blank=True, null=True)
	city = models.CharField(max_length=100, blank=True, null=True)
	state = models.CharField(max_length=30, blank=True, null=True)
	zipcode = models.CharField(max_length=5)  # blank and null = True
	created_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name



class Team(models.Model):
	''' a department/group/team within a healthsystem '''
	system = models.ForeignKey(HealthSystem)
	name = models.CharField(max_length=100)
	description = models.TextField()
	admin = models.ForeignKey(User)

	def __unicode__(self):
		return self.name


class UserProfile(models.Model):
	''' info about a user '''
	user = models.OneToOneField(User)
	system = models.ForeignKey(HealthSystem)
	team = models.ForeignKey(Team)
	# belong to group here? or another way? --- add here and then do groups also - this is main group

	def __unicode__(self):
		return '{} {}'.format(self.user.first_name, self.user.last_name)


class PhysicianGroup(models.Model):
	name = models.CharField(max_length=100)
	system = models.ForeignKey(HealthSystem)

	def __unicode__(self):
		return self.name


class Physician(models.Model):
	user = models.OneToOneField(User)
	npi = models.CharField(max_length=100)
	payroll_num = models.CharField(max_length=100, blank=True, null=True)
	med_license_num = models.CharField(max_length=100)
	med_license_state = models.CharField(max_length=100)
	med_degree = models.CharField(max_length=255)
	system = models.ForeignKey(HealthSystem)
	physiciangroup = models.ForeignKey(PhysicianGroup, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.user.username

class PhysicianTimeLog(models.Model):
	physician = models.ForeignKey(Physician)
	date = models.DateTimeField(blank=True, null=True)
	start_time = models.DateTimeField(blank=True, null=True)
	end_time = models.DateTimeField(blank=True, null=True)
	mins_worked = models.IntegerField(blank=True, null=True)
	category = models.CharField(max_length=100)
	notes = models.TextField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '{} - {} - {}'.format(self.physician, self.category, self.date)

class Template(models.Model):
	''' a template for creating contracts '''
	system = models.ForeignKey(HealthSystem)
	name = models.CharField(max_length=100)
	short_desc = models.CharField(max_length=100, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	add_on = models.BooleanField(default=False)
	html = models.TextField()

	def __unicode__(self):
		return self.name


class Workflow(models.Model):
	''' done I think'''
	system = models.ForeignKey(HealthSystem)
	name = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name


class WorkflowItem(models.Model):
	''' done I think'''
	workflow = models.ForeignKey(Workflow)
	user = models.ForeignKey(User, blank=True, null=True)
	team = models.ForeignKey(Team, blank=True, null=True)
	position = models.IntegerField()

	def __unicode__(self):
		return self.workflow.name

class ContractType(models.Model):
	''' the types of contracts that a health system has '''
	system = models.ForeignKey(HealthSystem)
	name = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name

class ContractSubType(models.Model):
	contract_type = models.ForeignKey(ContractType)
	name = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name

class Contract(models.Model):
	''' contract info that does not change / isn't verisioned '''
	system = models.ForeignKey(HealthSystem)
	name = models.CharField(max_length=100)
	workflow = models.ForeignKey(Workflow, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User)
	physician = models.ForeignKey(Physician, blank=True, null=True)
	physician_group = models.ForeignKey(PhysicianGroup, blank=True, null=True)
	contract_type = models.ForeignKey(ContractType, blank=True, null=True)
	contract_subtype = models.ForeignKey(ContractSubType, blank=True, null=True)
	contract_file = models.FileField(upload_to='contracts', blank=True, null=True)
	status = models.CharField(max_length=50, default='In Progress')
	signed = models.BooleanField(default=False)
	# signed_at = models.DateTimeField(blank=True, null=True)

	def __unicode__(self):
		return self.name

class ContractInfo(models.Model):
	''' information about a contract that would be changed in new versions '''
	# CONTRACT_TYPES = (
	# 	('Professional Services / Employment', 'Professional Services / Employment'),
	# 	('Physician Coverage / Stipends', 'Physician Coverage / Stipends'),
	# 	('Administrative / Medical Directorships', 'Administrative / Medical Directorships'),
	# 	('Teaching / Residency', 'Teaching / Residency'),
	# 	('Call Pay', 'Call Pay'),
	# 	('Income Guarantee', 'Income Guarantee'),
	# 	('Real Estate / Lease Agreements', 'Real Estate / Lease Agreements'),
	# )

	contract = models.ForeignKey(Contract)
	version = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	html = models.TextField(blank=True, null=True)
	html_output = models.TextField(blank=True, null=True)
	change_made = models.CharField(max_length=255)


	grabbed_at = models.DateTimeField(blank=True, null=True)
	next_user = models.ForeignKey(User, blank=True, null=True, related_name='contract_next_user')
	next_team= models.ForeignKey(Team, blank=True, null=True, related_name='contract_next_team')
	sent_at = models.DateTimeField(blank=True, null=True)
	current_user = models.ForeignKey(User, blank=True, null=True, related_name='contract_current_user')
	current_team = models.ForeignKey(Team, blank=True, null=True, related_name='contract_current_team')
	prev_user = models.ForeignKey(User, blank=True, null=True, related_name='contract_past_user')
	prev_team = models.ForeignKey(Team, blank=True, null=True, related_name='contract_past_team')


	site = models.ForeignKey(HealthSite, blank=True, null=True)
	region = models.CharField(max_length=100, blank=True, null=True)
	specialty = models.CharField(max_length=100, blank=True, null=True)
	contracting_entity = models.CharField(max_length=100, blank=True, null=True)
	start_date = models.DateTimeField(blank=True, null=True)
	end_date = models.DateTimeField(blank=True, null=True)
	type_of_services = models.CharField(max_length=255, blank=True, null=True)
	type_of_admin_services = models.TextField(blank=True, null=True)
	admin_services_title = models.CharField(max_length=255, blank=True, null=True)
	num_physicians = models.IntegerField(blank=True, null=True)
	max_monthly_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
	amount = models.IntegerField(blank=True, null=True)
	performance_linked = models.NullBooleanField(default=None, blank=True, null=True)
	performance_criteria = models.TextField(blank=True, null=True)
	responsible_party = models.CharField(max_length=100, blank=True, null=True)
	responsible_party_secondary = models.CharField(max_length=100, blank=True, null=True)
	termination_days_notice = models.IntegerField(blank=True, null=True)
	malpractice_coverage_party = models.CharField(max_length=100, blank=True, null=True)
	malpractice_limits= models.IntegerField(blank=True, null=True)
	type_of_malpractice_coverage = models.CharField(max_length=100, blank=True, null=True)
	physician_tail_responsibility = models.NullBooleanField(default=None, blank=True, null=True)
	right_to_bill = models.CharField(max_length=100, blank=True, null=True)
	non_compete = models.NullBooleanField(default=None, blank=True, null=True)
	non_solicitation = models.NullBooleanField(default=None, blank=True, null=True)
	auto_renew = models.NullBooleanField(default=None, blank=True, null=True)
	renewal_date = models.DateTimeField(blank=True, null=True)


	# address of lease agreement - maybe make another column

	def __unicode__(self):
		return '{} (version {})'.format(self.contract.name, self.version)

class ContractAttachment(models.Model):
	'''attachements to the contract, not the actual contract file'''
	contract = models.ForeignKey(Contract)
	name = models.CharField(max_length=100, blank=True, null=True)
	attachment = models.FileField(upload_to='attachments')

	def __unicode__(self):
		return self.contract.name	

class ContractApproval(models.Model):
	contract = models.ForeignKey(Contract)
	user = models.ForeignKey(User)
	team = models.ForeignKey(Team)
	created_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name


class Alert(models.Model):
	''' alert to user that something happened that concerns them '''
	user = models.ForeignKey(User)
	contract = models.ForeignKey(Contract)
	name = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)
	level = models.IntegerField(default=2) # higher is more serious

	def __unicode__(self):
		return self.name


# class Action(models.Model):
# 	''' log of all actions taken

# 	ex.
# 		- create template
# 		- edit contract / create contract
# 		- check out / check in contract
# 		- create user / Physician / workflow
# 		- create site / group

# 	 '''
# 	user = models.ForeignKey(User)
# 	action_taken = models.CharField(max_length=255)
# 	contract = models.ForeignKey(ContractInfo, blank=True, null=True)
# 	template = models.ForeignKey(Template, blank=True, null=True)
# 	created_at = models.DateTimeField(auto_now_add=True)

# 	def __unicode__(self):
# 		return self.action_taken



#### Permissions
# can add a site / physician
# can add users
# can do analysis (see all data)
# only can edit contracts





class ContactRequest(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.EmailField()
	phone_number = models.CharField(max_length=10, blank=True, null=True)
	organization = models.CharField(max_length=255, blank=True, null=True)
	city = models.CharField(max_length=255, blank=True, null=True)
	state = models.CharField(max_length=100, blank=True, null=True)
	zipcode = models.CharField(max_length=5, blank=True, null=True)
	job_title = models.CharField(max_length=255, blank=True, null=True)
	message = models.TextField()

	date = models.DateTimeField(auto_now_add=True)
	responded = models.BooleanField(default=False)
	notes = models.TextField()

	def __unicode__(self):
		return self.email

##################################
##########    FORMS   ############
##################################





class HealthSiteForm(ModelForm):
	class Meta:
		model = HealthSite
		exclude = ('system',)
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control'}),
			'street': forms.TextInput(attrs={'class': 'form-control'}),
			'city': forms.TextInput(attrs={'class': 'form-control'}),
			'state': forms.TextInput(attrs={'class': 'form-control', 'style':'width:200px'}),
			'zipcode': forms.TextInput(attrs={'class': 'form-control', 'style':'width:200px'}),
		}

class TemplateForm(ModelForm):
	class Meta:
		model = Template
		exclude = ('system',)
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control'}),
			'short_desc': forms.TextInput(attrs={'class': 'form-control'}),
			'description': forms.Textarea(attrs={'class': 'form-control'}),
			'add_on': forms.RadioSelect(attrs={'style': 'display:none'}),
			'html': forms.Textarea(attrs={'style': 'display:none'}),
		}


class ContractForm(ModelForm):
	class Meta:
		model = Contract
		exclude = ('system','created_by')

	def __init__(self, *args, **kwargs):
		super(ContractForm, self).__init__(*args, **kwargs)
		for i in self.fields:
			self.fields[i].widget.attrs['class'] = 'form-control'

class ContractInfoForm(ModelForm):
	class Meta:
		model = ContractInfo
		exclude = ('contract', 'html', 'html_output', 'version', 'created_by', 'prev_team', 'prev_user', 'grabbed_at', 'sent_at', 'current_user', 'current_team')


	def __init__(self, *args, **kwargs):
		super(ContractInfoForm, self).__init__(*args, **kwargs)
		for i in self.fields:
			self.fields[i].widget.attrs['class'] = 'form-control'

class TeamForm(ModelForm):
	class Meta:
		model = Team
		exclude = ('system',)
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control'}),
			'description': forms.Textarea(attrs={'class': 'form-control'}),
			'admin': forms.Select(attrs={'class': 'form-control'}),
		}

	# def __init__(self, user=None, **kwargs):
	# 	super(TeamForm, self).__init__(**kwargs)
	# 	if user:
	# 		self.fields['admin'].queryset = UserProfile.objects.filter(system=user.userprofile.system)

	def __init__(self, **kwargs):
		super(TeamForm, self).__init__(**kwargs)

		# need to filter system 
		# need to enforce that name doesnt match another name
		# need to make look better, while still loading dropdowns (crispy?)


class NamesForm(forms.Form):
	first_name = forms.CharField(max_length=30, required=True)
	last_name = forms.CharField(max_length=30, required=True)
	email = forms.EmailField() # emails not required with this setup - they need to be

class ExtendedUserCreateForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(max_length=30, required=True)
	last_name = forms.CharField(max_length=30, required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2", "first_name", "last_name")
		# for some reason, widgets do not work when inheriting from usercreationform, need to user init
		# to set attributes

	def __init__(self, *args, **kwargs):
		super(ExtendedUserCreateForm, self).__init__(*args, **kwargs)
		for i in self.fields:
			self.fields[i].widget.attrs['class'] = 'form-control'


	def save(self, commit=True):
		user = super(ExtendedUserCreateForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		user.first_name = self.cleaned_data["first_name"]
		user.last_name = self.cleaned_data["last_name"]
		if commit:
			user.save()
		return user

class UserProfileForm(ModelForm):
	class Meta:
		model = UserProfile
		exclude = ('system','user')

class PhysicianForm(ModelForm):
	class Meta:
		model = Physician
		exclude = ('system','user')
		widgets = {
			'physiciangroup': forms.Select(attrs={'class': 'form-control'}),
		}

class PhysicianGroupForm(ModelForm):
	class Meta:
		model = PhysicianGroup
		exclude = ('system',)
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control'}),
		}


class ContactUsForm(ModelForm):
	class Meta:
		model = ContactRequest
		exclude = ('phone_number','city','state','zipcode','job_title','responded','notes','date')

	def __init__(self, *args, **kwargs):
		super(ContactUsForm, self).__init__(*args, **kwargs)
		for i in self.fields:
			self.fields[i].widget.attrs['class'] = 'form-control'

