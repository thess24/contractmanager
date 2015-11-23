from apps.main.models import Alert

def alerts(request):
	if request.user.is_authenticated():
		num_alerts = Alert.objects.filter(user=request.user, active=True).count()
	else: 
		num_alerts = 0

	return {"num_alerts":num_alerts}
