from django.db import models
from django.forms import ModelForm, Textarea
from django import forms
from django.contrib.auth.models import User
import os
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings



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

	def __unicode__(self):
		return self.user.email


class PhysicianGroup(models.Model):
	name = models.CharField(max_length=100)
	system = models.ForeignKey(HealthSystem)

	def __unicode__(self):
		return self.name


class Physician(models.Model):
	user = models.OneToOneField(User)
	system = models.ForeignKey(HealthSystem)
	physiciangroup = models.ForeignKey(PhysicianGroup, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.user.username


class Template(models.Model):
	''' done I think'''
	system = models.ForeignKey(HealthSystem)
	name = models.CharField(max_length=100)
	short_desc = models.CharField(max_length=100, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
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

	CATEGORIES = (
		('Asset Allocation', 'Asset Allocation'),
		('Equities', 'Equities'),
		('Fixed Income', 'Fixed Income'),
		('Sector Investing', 'Sector Investing'),
		('Alternative Investing', 'Alternative Investing'),
		('Geopolitics', 'Geopolitics'),
		('Financial Planning', 'Financial Planning'),
	)

	contract = models.ForeignKey(Contract)
	version = models.IntegerField()
	contract_type = models.CharField(max_length=100, choices=CATEGORIES)
	html = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User)	
	# contract_file = 

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
















##########    FORMS   ############
class HealthSiteForm(ModelForm):
	class Meta:
		model = HealthSite
		exclude = ('system',)


class TeamForm(ModelForm):
	class Meta:
		model = Team
		exclude = ('system',)

	# def __init__(self, user=None, **kwargs):
	# 	super(TeamForm, self).__init__(**kwargs)
	# 	if user:
	# 		self.fields['admin'].queryset = UserProfile.objects.filter(system=user.userprofile.system)

	def __init__(self, **kwargs):
		super(TeamForm, self).__init__(**kwargs)

		# need to filter system 
		# need to enforce that name doesnt match another name
		# need to make look better, while still loading dropdowns (crispy?)



class UserForm(ModelForm):
	class Meta:
		model = UserProfile
		exclude = ('system',)


class PhysicianForm(ModelForm):
	class Meta:
		model = Physician
		exclude = ('system',)

class PhysicianGroupForm(ModelForm):
	class Meta:
		model = PhysicianGroup
		exclude = ('system',)