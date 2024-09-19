# website/management/commands/create_profiles.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from website.models import Profile

class Command(BaseCommand):
    help = 'Create profiles for all users who don\'t have one'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)
        self.stdout.write(self.style.SUCCESS('Successfully created profiles for all users'))
