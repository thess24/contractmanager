from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication
from tastypie import fields

from django.contrib.auth.models import User
from apps.main.models import Physician, PhysicianTimeLog


# 1. only let user post to their own user account				CHECKED
# 2. only let user get data from own account    				CHECKED
# 3. user must login with every request / send auth token   	CHECKED




# AUTHORIZATION
class PhysicianAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(physician__user=bundle.request.user)




# MODEL RESOURCES
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
	physician = fields.ForeignKey(PhysicianResource, 'physician')

	class Meta:
		queryset = PhysicianTimeLog.objects.all()
		filtering = {
			'physician': ALL_WITH_RELATIONS,
		}
		authentication = BasicAuthentication()
		authorization = PhysicianAuthorization()

	def hydrate(self, bundle):
		# print bundle.obj
		# this would be the spot to create mins_worked from start and end time if we do it serverside
		return bundle

	def obj_create(self, bundle, **kwargs):
		'''creates the object from the data passed in'''
		physician = Physician.objects.get(user=bundle.request.user)
		return super(PhysicianTimeLogResource, self).obj_create(bundle, physician = physician)
