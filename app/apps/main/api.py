from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication
from tastypie import fields

from django.contrib.auth.models import User
from apps.main.models import Physician, PhysicianTimeLog, Alert, PhysicianTimeLogCategory



# 1. only let user post to their own user account				CHECKED
# 2. only let user get data from own account    				CHECKED
# 3. user must login with every request / send auth token   	CHECKED




# AUTHORIZATION
class PhysicianTimeLogAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(timelog_category__physician__user=bundle.request.user)

class UserAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user)

class PhysicianAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(physician__user=bundle.request.user)





# MODEL RESOURCES
class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name = 'user'
		excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
		allowed_methods = ['get']
		filtering = {
			'username': ALL,
		}

class PhysicianResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user')

	class Meta:
		queryset = Physician.objects.all()
		allowed_methods = ['get']
		filtering = {
			'user': ALL_WITH_RELATIONS,
		}

class PhysicianTimeLogResource(ModelResource):
	timelog_category = fields.ForeignKey(PhysicianResource, 'timelog_category')

	class Meta:
		queryset = PhysicianTimeLog.objects.all()
		filtering = {
			'timelog_category': ALL_WITH_RELATIONS,
		}
		authentication = BasicAuthentication()
		authorization = PhysicianTimeLogAuthorization()

	def hydrate(self, bundle):
		# print bundle.obj
		# this would be the spot to create mins_worked from start and end time if we do it serverside
		return bundle

	def obj_create(self, bundle, **kwargs):
		'''creates the object from the data passed in'''
		physician = Physician.objects.get(user=bundle.request.user) 
		return super(PhysicianTimeLogResource, self).obj_create(bundle, timelog_category__physician = physician)



class PhysicianAlertResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user')

	class Meta:
		queryset = Alert.objects.all()
		allowed_methods = ['get']
		filtering = {
			'user': ALL_WITH_RELATIONS,
		}

		authentication = BasicAuthentication()
		authorization = UserAuthorization()


class PhysicianTimeLogCategoryResource(ModelResource):
	physician = fields.ForeignKey(PhysicianResource, 'physician')

	class Meta:
		queryset = PhysicianTimeLogCategory.objects.all()
		excludes = ['first_elevation_users', 'second_elevation_users', 'final_elevation_users', 'approving_users', 'workflow_default']
		allowed_methods = ['get']
		filtering = {
			'physician': ALL_WITH_RELATIONS,
		}

		authentication = BasicAuthentication()
		authorization = PhysicianAuthorization()