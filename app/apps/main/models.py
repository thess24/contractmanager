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

	def __unicode__(self):
		return self.name


class HealthSite(models.Model):
	name = models.CharField(max_length=100)
	system = models.ForeignKey(HealthSystem)
	street = models.CharField(max_length=100, blank=True, null=True)
	city = models.CharField(max_length=100, blank=True, null=True)
	state = models.CharField(max_length=30, blank=True, null=True)
	zipcode = models.CharField(max_length=5)
	created_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name





class Team(models.Model):
	'''done I think'''
	system = models.ForeignKey(HealthSystem)
	name = models.CharField(max_length=100)
	description = models.TextField()
	admin = models.ForeignKey(User)

	def __unicode__(self):
		return self.name


class UserProfile(models.Model):
	user = models.OneToOneField(User)
	system = models.ForeignKey(HealthSystem)
	# belong to group here? or another way?

	def __unicode__(self):
		return '{} {}'.format(self.user.first_name, self.user.last_name)


class PhysicianGroup(models.Model):
	name = models.CharField(max_length=100)
	system = models.ForeignKey(HealthSystem)

	def __unicode__(self):
		return self.name


class Physician(models.Model):
	user = models.OneToOneField(User)
	# npi = models.CharField(max_length=100)
	# payroll_num = models.CharField(max_length=100)
	# med_liscence_num = models.CharField(max_length=100)
	# med_liscence_state = models.CharField(max_length=100)
	# med_degree = models.CharField(max_length=255)
	system = models.ForeignKey(HealthSystem)
	physiciangroup = models.ForeignKey(PhysicianGroup, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.user.username

class PhysicianTimeLog(models.Model):
	doctor = models.ForeignKey(Physician)
	date = models.DateTimeField()
	mins_worked = models.IntegerField()
	category = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '{} - {} - {}'.format(doctor, category, date)

class Template(models.Model):
	''' done I think'''
	system = models.ForeignKey(HealthSystem)
	name = models.CharField(max_length=100)
	short_desc = models.CharField(max_length=100, blank=True, null=True)
	description = models.TextField(blank=True, null=True)  # remove
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


class Contract(models.Model):
	system = models.ForeignKey(HealthSystem)
	name = models.CharField(max_length=100)
	workflow = models.ForeignKey(Workflow, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	physician = models.ForeignKey(Physician, blank=True, null=True)
	physician_group = models.ForeignKey(PhysicianGroup, blank=True, null=True, )
	next_user = models.ForeignKey(User, blank=True, null=True, related_name='contract_next_user')
	next_group = models.ForeignKey(User, blank=True, null=True, related_name='contract_next_group')
	current_user = models.ForeignKey(User, blank=True, null=True, related_name='contract_current_user')
	current_group = models.ForeignKey(User, blank=True, null=True, related_name='contract_current_group')

	def __unicode__(self):
		return self.name


class ContractInfo(models.Model):

	CONTRACT_TYPES = (
		('Professional Services / Employment', 'Professional Services / Employment'),
		('Physician Coverage / Stipends', 'Physician Coverage / Stipends'),
		('Administrative / Medical Directorships', 'Administrative / Medical Directorships'),
		('Teaching / Residency', 'Teaching / Residency'),
		('Call Pay', 'Call Pay'),
		('Income Guarantee', 'Income Guarantee'),
		('Real Estate / Lease Agreements', 'Real Estate / Lease Agreements'),
	)

	contract = models.ForeignKey(Contract)
	version = models.IntegerField()  # change maybe
	contract_type = models.CharField(max_length=100, choices=CONTRACT_TYPES)
	html = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	services_lines = models.CharField(max_length=255, blank=True, null=True)
	num_physicians = models.IntegerField(blank=True, null=True)
	max_monthly_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
	performance_linked = models.BooleanField(default=False)
	performance_metrics = models.TextField(blank=True, null=True)
	# contract_file = 
	# address of lease agreement - maybe make another column

	def __unicode__(self):
		return self.name


class ContractApproval(models.Model):
	contract = models.ForeignKey(Contract)
	user = models.ForeignKey(User)
	team = models.ForeignKey(Team)
	created_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name


class Alert(models.Model):
	''' done I think'''
	user = models.ForeignKey(User)
	contract = models.ForeignKey(Contract)
	name = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)
	level = models.IntegerField()

	def __unicode__(self):
		return self.name









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
	email = forms.EmailField() # emails not required with this setup

	# consider doing this instead
	# http://jessenoller.com/blog/2011/12/19/quick-example-of-extending-usercreationform-in-django

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
		print self.fields
		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['email'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['first_name'].widget.attrs['class'] = 'form-control'
		self.fields['last_name'].widget.attrs['class'] = 'form-control'

		# probably cleaner to look through fields and set to form-control. Could be used on all forms


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