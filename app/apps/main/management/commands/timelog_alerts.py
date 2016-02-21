from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.main.models import PhysicianTimeLogCategory, PhysicianTimeLogPeriod, Alert, Contract

import datetime
from dateutil.relativedelta import relativedelta

from os import environ


class Command(BaseCommand):

	def handle(self, *args, **options):
		now = datetime.datetime.now()

		if now.day in [8,12,14,16,20]: # days of the week to run do alerts for
			pass
		else:
			return




		last_month = now + relativedelta(months=-1)  # month that needs to be submitted -- aka last month
		period = datetime.date(last_month.year,last_month.month,1)

		# physicians who *should submit
		tlcategories = PhysicianTimeLogCategory.objects.all()
		# physicians who *did submit
		periods = PhysicianTimeLogPeriod.objects.filter(period=period) 

		# area for table - this makes dict of all tsperiods and if they have been submitted/created or not
		should =  list(tlcategories.values('category__name','physician','physician__user__first_name','physician__user__last_name'))
		did = list(periods.values('timelog_category__physician','timelog_category__physician__user__first_name', \
			'timelog_category__physician__user__last_name', 'timelog_category__category__name','active','approved_at'))

		for d in did:
			d['physician-category'] = '{} - {}'.format(d['timelog_category__category__name'],d['timelog_category__physician'])
			d['submitted'] = True
			if not d['approved_at'] and d['active']:
				d['pending'] = True
			else:
				d['pending'] = False

		uniquephyscats = set([d['physician-category'] for d in did])

		for i in should:
			i['physician-category'] = '{} - {}'.format(i['category__name'],i['physician'])
			if i['physician-category'] not in uniquephyscats:
				add = {'timelog_category__category__name':i['category__name'] , 'submitted': False, 'timelog_category__physician':i['physician'],\
					'timelog_category__physician__user__first_name':i['physician__user__first_name'], \
					'timelog_category__physician__user__last_name':i['physician__user__last_name'], \
					'active':False, 'approved_at':None, 'pending':False}
				did.append(add)

		physician_categories = did


		for doc in physician_categories:
			if not doc["submitted"]:
				days_left = 15-now.day

				if days_left>0:
					message =  'You have {} days to submit your timesheets - {}!'.format(days_left, doc['timelog_category__physician'])
				
				else:
					days_left = -days_left
					message =  'You are {} days overdue in submitting your timesheets - {}!'.format(days_left, doc['timelog_category__physician'])
				

				physician = User.objects.get(id=doc['timelog_category__physician'])

				c = Contract.objects.get(id=1)
				Alert.objects.create(user=physician, name=message, contract=c)

