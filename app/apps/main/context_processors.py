from apps.main.models import Alert

def alerts(request):
	if request.user.is_authenticated():
		num_alerts = Alert.objects.filter(user=request.user, active=True).count()
	else: 
		num_alerts = 0

	return {"num_alerts":num_alerts}

def system_name(request):
	if request.user.is_authenticated():
		try:
			system_name = request.user.userprofile.system
			return {"system_name":system_name}
		except:
			pass

		try:
			system_name = request.user.physician.system
			return {"system_name":system_name}
		except:
			pass
			
	return {"system_name":[]}


