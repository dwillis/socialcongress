from django.db import models
from django.contrib.localflavor.us.models import USStateField
import simplejson as json
import urllib
import datetime

RACE_CHOICES = (
    (u'W', u'White'),
    (u'B', u'Black'),
    (u'A', u'Asian'),
    (u'H', u'Hispanic'),
)

GENDER_CHOICES = (
    (u'M', u'Male'),
    (u'F', u'Female'),
)

STATUS_CHOICES = (
    (u'O', u'Old'),
    (u'N', u'New'),
)

class Member(models.Model):
    bioguide_id = models.CharField(max_length=12, null=True)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=75)
    party = models.CharField(max_length=75)
    branch = models.CharField(max_length=20)
    state = USStateField()
    district = models.PositiveSmallIntegerField(null=True, blank=True)
    official_twitter_name = models.CharField(max_length=255, null=True, blank=True)
    campaign_twitter_name = models.CharField(max_length=255, null=True, blank=True)
    official_facebook_name = models.CharField(max_length=255, null=True, blank=True)
    campaign_facebook_name = models.CharField(max_length=255, null=True, blank=True)
    race = models.CharField(max_length=1, choices=RACE_CHOICES, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    service = models.PositiveSmallIntegerField(null=True, blank=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, null=True, blank=True)
    youtube_name = models.CharField(max_length=255, null=True, blank=True)
    margin_2010 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    social_networks = models.PositiveSmallIntegerField(null=True, blank=True)
    facebook_10 = models.PositiveIntegerField(null=True, blank=True)
    facebook_status = models.PositiveSmallIntegerField(null=True, blank=True)
    twitter_10 = models.PositiveIntegerField(null=True, blank=True)
    twitter_status = models.PositiveSmallIntegerField(null=True, blank=True)
    index_10 = models.PositiveIntegerField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name
    
    def latest_report(self):
        try:
            return self.report_set.order_by('-date')[0]
        except IndexError:
            return None
    
    def previous_report(self):
        try:
            return self.report_set.order_by('-date')[6]
        except IndexError:
            return None
            
    def change_from_previous(self, account):
        try:
            if self.previous_report():
                if account == 'official_twitter':
                    return self.latest_report().official_twitter_followers - self.previous_report().official_twitter_followers
                elif account == 'official_facebook':
                    return self.latest_report().official_facebook_likes - self.previous_report().official_facebook_likes
                elif account == 'campaign_twitter':
                    return self.latest_report().campaign_twitter_followers - self.previous_report().campaign_twitter_followers
                elif account == 'campaign_facebook':
                    return self.latest_report().campaign_facebook_likes - self.previous_report().campaign_facebook_likes
        except:
            return None

    def twitter_followers(self, account):
        if account:
            url = "http://api.twitter.com/1/users/show.json?screen_name=%s" % account
            response = urllib.urlopen(url).read()
            try:
                result = json.loads(response)
                return result['followers_count']
            except:
                Error(member=self, date=datetime.date.today(), message="Can't load %s on Twitter" % account)
                return None
        else:
            return None
    
    def facebook_likes(self, account, token):
        if account:
            url = "https://graph.facebook.com/%s?access_token=%s" % (account, token)
            response = urllib.urlopen(url).read()
            if response == 'false':
                Error.objects.create(member=self, date=datetime.date.today(), message="Can't find %s on Facebook" % account)
                return None
            result = json.loads(response)
            if 'likes' not in result.keys():
                return None
            else:
                return result['likes']
        else:
            return None

    
class Report(models.Model):
    member = models.ForeignKey(Member)
    date = models.DateField(auto_now=False, auto_now_add=True)
    official_facebook_likes = models.PositiveIntegerField(null=True, blank=True)
    official_twitter_followers = models.PositiveIntegerField(null=True, blank=True)
    official_twitter_updates = models.PositiveIntegerField(null=True, blank=True)
    campaign_facebook_likes = models.PositiveIntegerField(null=True, blank=True)
    campaign_twitter_followers = models.PositiveIntegerField(null=True, blank=True)
    campaign_twitter_updates = models.PositiveIntegerField(null=True, blank=True)
    
    def __unicode__(self):
        return self.member.slug
    
class Error(models.Model):
    member = models.ForeignKey(Member)
    date = models.DateField(auto_now=False, auto_now_add=True)
    message = models.TextField()
    
    def __unicode__(self):
        return member
    

