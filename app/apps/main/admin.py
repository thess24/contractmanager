from django.contrib import admin
from apps.main.models import *


# class TalkAdmin(admin.ModelAdmin):
#     list_display = ('user', 'expert', 'time', 'accepted','cancelled','requested','call_length')


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
admin.site.register(ContractInfo)
admin.site.register(ContractApproval)
admin.site.register(Alert)
# admin.site.register(CallIn, CallInAdmin)
