from django.contrib import admin
from apps.main.models import *


class PhysicianTimeLogApprovalAdmin(admin.ModelAdmin):
    list_display = ('user', 'physiciantimelogperiod', 'approved', 'active', 'created_at') 

class PhysicianTimeLogAdmin(admin.ModelAdmin):
    list_display = ('timelog_category', 'date', 'mins_worked','created_at', 'active') 

class PhysicianTimeLogPeriodAdmin(admin.ModelAdmin):
    list_display = ('timelog_category', 'period', 'mins_worked','active', 'current_user', 'id')

class WorkflowItemAdmin(admin.ModelAdmin):
    list_display = ('workflow', 'user', 'position', 'team')

class WorkflowAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_all_users')

class PhysicianTimeLogCategoryAdmin(admin.ModelAdmin):
    list_display = ('physician', 'category', 'hours_needed')


admin.site.register(HealthSystem)
admin.site.register(HealthSite)
admin.site.register(Team) 
admin.site.register(UserProfile)
admin.site.register(PhysicianGroup)
admin.site.register(Physician)

admin.site.register(Alert)

admin.site.register(Workflow, WorkflowAdmin)
admin.site.register(WorkflowItem, WorkflowItemAdmin)

admin.site.register(Contract)
admin.site.register(ContractType)
admin.site.register(ContractInfo)
admin.site.register(ContractApproval)
admin.site.register(Template)

admin.site.register(PhysicianTimeLog, PhysicianTimeLogAdmin)
admin.site.register(PhysicianTimeLogPeriod, PhysicianTimeLogPeriodAdmin)
admin.site.register(PhysicianTimeLogApproval, PhysicianTimeLogApprovalAdmin)
admin.site.register(PhysicianTimeLogCategory, PhysicianTimeLogCategoryAdmin)

admin.site.register(ContactRequest)


