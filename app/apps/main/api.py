from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
from tastypie import fields

from django.contrib.auth.models import User
from apps.main.models import Physician, PhysicianTimeLog



class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name = 'user'
		excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
		filtering = {
			'username': ALL,
		}

class PhysicianResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user')

	class Meta:
		queryset = Physician.objects.all()
		filtering = {
			'user': ALL_WITH_RELATIONS,
		}

class PhysicianTimeLogResource(ModelResource):
	physician = fields.ForeignKey(PhysicianResource, 'doctor')

	class Meta:
		queryset = PhysicianTimeLog.objects.all()
		filtering = {
			'physician': ALL_WITH_RELATIONS,
		}
		authorization = Authorization()

