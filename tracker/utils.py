import datetime
from tracker.models import Member, Report
from django.template.defaultfilters import slugify
import csv
import urllib
import simplejson as json
from dateutil.parser import *
import time

def update_twitter(branch='house', official=True, batch=1):
    if official:
        screen_names = [x.official_twitter_name for x in Member.objects.filter(branch=branch, official_twitter_name__isnull=False).order_by('last_name')]
    else:
        screen_names = [x.campaign_twitter_name for x in Member.objects.filter(branch=branch, campaign_twitter_name__isnull=False).order_by('last_name')]
    if batch == 1:
        screen_names = screen_names[:100]
    elif batch == 2:
        screen_names = screen_names[100:200]
    elif batch == 3:
        screen_names = screen_names[200:300]
    elif batch == 4:
        screen_names = screen_names[300:400]
    elif batch == 5:
        screen_names = screen_names[400:]
    url = "http://api.twitter.com/1/users/lookup.json?screen_name=%s" % ",".join(screen_names)
    response = urllib.urlopen(url).read()
    results = json.loads(response)
    for result in results:
        if official:
            member = Member.objects.get(official_twitter_name__iexact=result['screen_name'])
            report, created = Report.objects.get_or_create(member=member, date=datetime.date.today())
            report.official_twitter_followers=result['followers_count']
            report.official_twitter_updates=result['statuses_count']
            report.save()
        else:
            member = Member.objects.get(campaign_twitter_name__iexact=result['screen_name'])
            report, created = Report.objects.get_or_create(member=member, date=datetime.date.today())
            report.campaign_twitter_followers=result['followers_count']
            report.campaign_twitter_updates=result['statuses_count']
            report.save()
        
def update_facebook(members, token):
    for member in members:
        print member
        report, created = Report.objects.get_or_create(member=member, date=datetime.date.today())
        params = {}
        params['access_token'] = token
        batch = [{'method': 'GET', 'relative_url': str(member.official_facebook_name)}, {'method': 'GET', 'relative_url': str(member.campaign_facebook_name)}]
        params['batch'] = [x for x in batch if x['relative_url'] != '']
        encoded_params = urllib.urlencode(params)
        f = urllib.urlopen("https://graph.facebook.com", encoded_params).read()
        results = json.loads(f)
        for result in results:
            try:
                body = json.loads(result['body'])
            except:
                continue
            if body == False:
                continue
            else:
                try:
                    if str(member.official_facebook_name.lower()) == body['username'].lower():
                        report.official_facebook_likes= body['likes']
                    elif str(member.campaign_facebook_name.lower()) == body['username'].lower():
                        report.campaign_facebook_likes= body['likes']
                except:
                    try:
                        if member.official_facebook_name == body['id']:
                            report.official_facebook_likes= body['likes']
                        elif member.campaign_facebook_name == body['id']:
                            report.campaign_facebook_likes= body['likes']
                    except KeyError:
                        print "No match found for %s" % member
                        
                report.save()
        time.sleep(3)
        

def update_member(member):
    official_likes = member.facebook_likes(member.official_facebook_name, token)
    campaign_likes = member.facebook_likes(member.campaign_facebook_name, token)
    report, created = Report.objects.get_or_create(member=member, date=datetime.date.today(), official_twitter_followers=official_twitter, official_facebook_likes=official_likes, campaign_facebook_likes=campaign_likes, campaign_twitter_followers=campaign_twitter)
    report.save()

def load_chamber(chamber):
    if chamber == 'senate':
        f = open("senate.csv","r")
    elif chamber == 'house':
        f = open("house.csv","r")
    else:
        raise("Must be house or senate")
    rows = csv.DictReader(f, delimiter=',')
    for row in rows:
        member, created = Member.objects.get_or_create(last_name=row['last'], first_name=row['first'], slug=slugify(row['first']+' '+row['last']), party=row['party'], branch=chamber, state=row['state'], district=row['district'])
        if row['username'] != '':
            member.official_facebook_name = row['username']
            member.save()
        elif row['username_campaign'] != '':
            member.campaign_facebook_name = row['username_campaign']
            member.save()
        if row['twitter'] != '':
            member.official_twitter_name = row['twitter']
            member.save()

def update_from_al():
    f = open("congress_upload_9_14_11.csv","r")
    rows = csv.DictReader(f, delimiter=',')
    for row in rows:
        print row['Name']
        member, created = Member.objects.get_or_create(bioguide_id=row['bioguide'])
        member.date_of_birth = parse(str(row['dob'])).date()
        member.race = row['race']
        member.gender = row['gender']
        member.service = int(row['service'])
        member.status = row['status'][0]
        member.youtube_name = row['youtube_name']
        member.margin_2010 = float(row['margin_2010'])
        member.social_networks = int(row['social_networks'])
        if row['facebook_10'] == '':
            member.facebook_10 = None            
        else:
            member.facebook_10 = int(row['facebook_10'])    
        member.facebook_status = int(row['facebook_status'])
        if row['twitter_10'] == '':
            member.twitter_10 = None
        else:
            member.twitter_10 = int(row['twitter_10'])
        member.twitter_status = int(row['twitter_status'])
        if row['official_twitter_name'] == '':
            member.official_twitter_name = None
        else:
            member.official_twitter_name = row['official_twitter_name']
        if row['campaign_twitter_name'] == '':
            member.campaign_twitter_name = None
        else:
            member.campaign_twitter_name = row['campaign_twitter_name']
        if row['index_10'] == None:
            member.index_10 = None
        else:
            member.index_10 = int(row['index_10'])
        member.save()
        
        
