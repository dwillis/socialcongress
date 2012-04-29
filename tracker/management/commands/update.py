from django.core.management.base import BaseCommand, CommandError
from tracker.utils import update_twitter, update_facebook
from tracker.facebook import fetch_facebook_token
from tracker.models import Member, Report

class Command(BaseCommand):
    
    def handle(self, branch, **options):
        if branch == 'house':
            for batch in range(1,6):
                update_twitter(branch, official=True, batch=batch)
                update_twitter(branch, official=False, batch=batch)
        else:
            update_twitter(branch, official=True, batch=1)
            update_twitter(branch, official=False, batch=1)
        token = fetch_facebook_token()
        members = Member.objects.filter(branch=branch).order_by('last_name')
        update_facebook(members, token)
        self.stdout.write("Loaded %s" % branch)
 

