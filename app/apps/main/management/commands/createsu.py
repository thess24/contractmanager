from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from os import environ


class Command(BaseCommand):

	def handle(self, *args, **options):
		if not User.objects.filter(username="admin").exists():
			User.objects.create_superuser("admin", environ["SUPERUSER_EMAIL"], environ["SUPERUSER_PASSWORD"])