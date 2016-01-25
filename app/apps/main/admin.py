from django.contrib import admin
from apps.main.models import *


class PhysicianTimeLogAdmin(admin.ModelAdmin):
    list_display = ('physician', 'date', 'mins_worked', 'category','created_at', 'active')


admin.site.register(HealthSystem)
admin.site.register(HealthSite)
admin.site.register(Team) 
admin.site.register(UserProfile)
admin.site.register(PhysicianGroup)
admin.site.register(Physician)
admin.site.register(Template)
admin.site.register(Workflow)
admin.site.register(WorkflowItem)
admin.site.register(Contract)
admin.site.register(ContractType)
admin.site.register(ContractInfo)
admin.site.register(ContractApproval)
admin.site.register(Alert)
admin.site.register(PhysicianTimeLog, PhysicianTimeLogAdmin)
admin.site.register(PhysicianTimeLogPeriod)
admin.site.register(ContactRequest)


# admin.site.register(CallIn, CallInAdmin)
