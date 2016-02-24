from django.db import models
from django.forms import ModelForm, Textarea
from django import forms
from django.contrib.auth.models import User
import os
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
import datetime

 
class HealthSystem(models.Model):
	name = models.CharField(max_length=100)
	street = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=30)
	zipcode = models.CharField(max_length=5)
	created_at = models.DateTimeField(auto_now_add=True)
	logo = models.ImageField(upload_to='logos', blank=True, null=True)
	shorthand = models.CharField(max_length=6)

	# add settings for the system here
	# master_user = 


	def __unicode__(self):
		return self.name

class HealthSite(models.Model):
	name = models.CharField(max_length=100)
	system = models.ForeignKey(HealthSystem)
	street = models.CharField(max_length=100, blank=True, null=True)
	city = models.CharField(max_length=100, blank=True, null=True)
	state = models.CharField(max_length=30, blank=True, null=True)
	zipcode = models.CharField(max_length=5, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name



class Team(models.Model):
	''' a department/group/team within a healthsystem '''
	system = models.ForeignKey(HealthSystem)
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True, null=True)
	admin = models.ForeignKey(User)

	def __unicode__(self):
		return self.name


class UserProfile(models.Model):
	''' info about a user '''
	user = models.OneToOneField(User)
	system = models.ForeignKey(HealthSystem)
	team = models.ForeignKey(Team)
	sites = models.ManyToManyField(HealthSite)

	superuser = models.BooleanField(default=False)  # can do anything and edit users? / change site settings
	master = models.BooleanField(default=False)  # can do anything for sites listed
	analyst = models.BooleanField(default=False)  # allowed to access all data



	# by default make it so you can only access contracts from sites youre subbed to--
	# also have ability to blacklist? or blacklist and whitelist?
	# contract_blacklist = 

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
		return '{} {}'.format(self.user.first_name, self.user.last_name)


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
	name = models.CharField(max_length=100)  # make required
	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User)
	is_all_users = models.BooleanField(default=True)

	def __unicode__(self):
		return self.name


# make system-name unique

class WorkflowItem(models.Model):
	'''An individual chain in the workflow
	postion:	index of workflowitem - starts at 0
	'''
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
	signed_at = models.DateTimeField(blank=True, null=True)

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
	''' alert to user that something happened that concerns them (specific contract) '''
	user = models.ForeignKey(User)
	contract = models.ForeignKey(Contract, blank=True, null=True)
	name = models.CharField(max_length=255)
	active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	level = models.IntegerField(default=2) # higher is more serious

	def __unicode__(self):
		return self.name

# class GenericAlert(models.Model):
# 	''' alert to user that something happened that concerns them (generic version) '''
# 	user = models.ForeignKey(User)
# 	name = models.CharField(max_length=255)
# 	active = models.BooleanField(default=True)
# 	created_at = models.DateTimeField(auto_now_add=True)
# 	level = models.IntegerField(default=2) # higher is more serious

# 	def __unicode__(self):
# 		return self.name

class PhysicianTimeLogCategory(models.Model):
	'''
	The category that each physician has to submit times for.

	approving_users:: 
	first_elevation_users::
	second_elevation_users::
	final_elevation_users::

	'''
	

	TIME_PERIODS = (
		('Weekly', 'Weekly'),
		('Monthly', 'Monthly'),
	)

	physician = models.ForeignKey(Physician)
	category = models.ForeignKey(ContractType)
	workflow_default = models.ForeignKey(Workflow)
	hours_needed = models.DecimalField(blank=True,null=True,decimal_places=2, max_digits=8)
	time_period = models.CharField(max_length = 30, choices=TIME_PERIODS, default='Monthly')
	approving_users = models.ManyToManyField(User, related_name='approving')
	created_at = models.DateTimeField(auto_now_add=True)

	first_elevation_users = models.ManyToManyField(User, blank=True, related_name='first_elevation')
	second_elevation_users = models.ManyToManyField(User, blank=True, related_name='second_elevation')
	final_elevation_users = models.ManyToManyField(User, blank=True, related_name='final_elevation')

	# add unique constraint for physician - category?

	def __unicode__(self):
		return '{} - {}'.format(self.category, self.physician)


class PhysicianTimeLog(models.Model):
	'''the individual time submitted by a physician for a days work in each category'''
	timelog_category = models.ForeignKey(PhysicianTimeLogCategory) 
	date = models.DateField(blank=True, null=True)
	start_time = models.DateTimeField(blank=True, null=True)
	end_time = models.DateTimeField(blank=True, null=True)
	mins_worked = models.IntegerField(blank=True, null=True)
	notes = models.TextField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return '{} - {}'.format(self.timelog_category, self.date)


class PhysicianTimeLogPeriod(models.Model):
	'''
	This is the snapshot of a period that will tell if a time period has been approved.

	approved_at: 	the time it was fully approved at
	active: 		whether the timelogperiod is the active record.  This should be false only if this timelogperiod was denied
	current_user: 	the user who has to currently approve the record
	approval_num:	the number of approvals so far -- in order to track position in workflowitems for passing purposes
					zero based indexing, so when the first person 'has' the object, this should be 0


	active and not approved - pending approval
	approved - approved
	not active - denied
	'''

	timelog_category = models.ForeignKey(PhysicianTimeLogCategory) 
	period = models.DateField()
	mins_worked = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	approved_at = models.DateTimeField(blank=True,null=True)
	approved_by = models.ForeignKey(User, blank=True, null=True, related_name='approver')  
	active = models.BooleanField(default=True)
	current_user = models.ForeignKey(User, blank=True, null=True, related_name='current')
	workflow = models.ForeignKey(Workflow, blank=True, null=True)
	approval_num = models.IntegerField(default=0)
	paid_at = models.DateTimeField(blank=True,null=True)
	paid_by = models.ForeignKey(User, blank=True, null=True, related_name='paying') 
	note = models.TextField(blank=True, null=True)

	def is_pending(self):
		if self.active and not self.approved_at:
			return True
		else:
			return False

	def is_approved(self):
		if self.approved_at:
			return True
		else:
			return False

	def is_denied(self):
		if not self.active:
			return True
		else:
			return False


	def __unicode__(self):
		return '{} - {} - {}'.format(self.timelog_category.physician, self.timelog_category.category, self.period)


class PhysicianTimeLogApproval(models.Model):
	''''''
	user = models.ForeignKey(User)
	physiciantimelogperiod = models.ForeignKey(PhysicianTimeLogPeriod)
	created_at = models.DateTimeField(auto_now_add=True)
	approved = models.BooleanField(default=True)  # true=approved, false=denied
	note = models.TextField(blank=True,null=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return '{} - {}'.format(self.physiciantimelogperiod, self.approved)


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
# can add a site / physician / physiciangroup
# can add users
# can do analysis (see all data)
# only can edit contracts / can't create
# 






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


class ContractTypeForm(ModelForm):
	class Meta:
		model = ContractType
		exclude = ('system',)

	def __init__(self, *args, **kwargs):
		super(ContractTypeForm, self).__init__(*args, **kwargs)
		for i in self.fields:
			self.fields[i].widget.attrs['class'] = 'form-control'


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

class WorkflowForm(ModelForm):
	class Meta:
		model = Workflow
		exclude = ('system','created_by')

	def __init__(self, *args, **kwargs):
		super(WorkflowForm, self).__init__(*args, **kwargs)
		for i in self.fields:
			self.fields[i].widget.attrs['class'] = 'form-control'

class WorkflowItemForm(ModelForm):
	class Meta:
		model = WorkflowItem
		exclude = ('workflow','position')

	def __init__(self, *args, **kwargs):
		super(WorkflowItemForm, self).__init__(*args, **kwargs)
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
		widgets = {
			'team': forms.Select(attrs={'class': 'form-control'}),
			'sites': forms.Select(attrs={'class': 'form-control'}),
		}

class PhysicianForm(ModelForm):
	class Meta:
		model = Physician
		exclude = ('system','user')
		widgets = {
			'physiciangroup': forms.Select(attrs={'class': 'form-control'}),
		}

	def __init__(self, *args, **kwargs):
		super(PhysicianForm, self).__init__(*args, **kwargs)
		for i in self.fields:
			self.fields[i].widget.attrs['class'] = 'form-control'
			
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


class PhysicianTimeLogForm(ModelForm):

	class Meta:
		model = PhysicianTimeLog
		exclude = ('active',)

	def clean(self):
		''' Make sure:
			xx 1. end time later than start time
			xx 2. mins worked is filled in and correct
			xx 3. date is filled in
		'''
		cleaned_data = super(PhysicianTimeLogForm, self).clean()


		start_time = cleaned_data.get('start_time',False)
		end_time = cleaned_data.get('end_time',False)

		if start_time and end_time:

			# check that start_time is before end time
			if end_time < start_time:
				raise ValidationError("The start time cannot be before the end time")

			# fill in date from start_time
			date_to_add = datetime.datetime(start_time.year,start_time.month,start_time.day)
			cleaned_data['date'] = date_to_add

			# set mins_worked based on times
			time_delta = end_time - start_time
			time_delta_mins = int(time_delta.total_seconds()/60)
			cleaned_data['mins_worked'] = time_delta_mins


		return cleaned_data

	def __init__(self, *args, **kwargs):
		super(PhysicianTimeLogForm, self).__init__(*args, **kwargs)
		for i in self.fields:
			self.fields[i].widget.attrs['class'] = 'form-control'




class PhysicianTimeLogCategoryForm(ModelForm):
	class Meta:
		model = PhysicianTimeLogCategory
		exclude = ('time_period','approving_users')

	def __init__(self, user, *args, **kwargs):
		super(PhysicianTimeLogCategoryForm, self).__init__(*args, **kwargs)
		for i in self.fields:
			self.fields[i].widget.attrs['class'] = 'form-control'

		self.fields['category'].queryset = ContractType.objects.filter(system=user.userprofile.system)
		self.fields['physician'].queryset = Physician.objects.filter(system=user.userprofile.system)

		# we can only pass from user to user for timesheets
		self.fields['workflow_default'].queryset = Workflow.objects.filter(is_all_users=True, system=user.userprofile.system)

		# users should be from the system, and be managers (ie have userprofiles)
		self.fields['first_elevation_users'].queryset = User.objects.filter(userprofile__system=user.userprofile.system)
		self.fields['second_elevation_users'].queryset = User.objects.filter(userprofile__system=user.userprofile.system)
		self.fields['final_elevation_users'].queryset = User.objects.filter(userprofile__system=user.userprofile.system)

