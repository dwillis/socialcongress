from tracker.models import Member, Report
import csv
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from tracker.tasks import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required

@csrf_protect
def update(request):
    if request.method == 'POST':
        if request.POST.has_key('twitter'):
            twitter_task.delay()
        elif request.POST.has_key('facebook'):
            facebook_task.delay()
    return render_to_response('admin/update.html', context_instance=RequestContext(request))

def chamber_csv(request, chamber):
    members = Member.objects.filter(branch=chamber).order_by('last_name')
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = "attachment; filename=%s.csv" % chamber

    writer = csv.writer(response)
    writer.writerow(['Bioguide','Member', 'State', 'District', 'Party', 'Official Twitter', 'Official Twitter Statuses', 'Official Facebook', 'Campaign Twitter', 'Campaign Twitter Statuses', 'Campaign Facebook', 'Date'])
    for member in members:
        report = member.latest_report()
        if report:
            writer.writerow([member.bioguide_id, member, member.state, member.district, member.party, report.official_twitter_followers, report.official_twitter_updates, report.official_facebook_likes, report.campaign_twitter_followers, report.campaign_twitter_updates, report.campaign_facebook_likes, report.date])
    return response
    
def weekly_csv(request, chamber):
    members = Member.objects.filter(branch=chamber).order_by('last_name')
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = "attachment; filename=%s.csv" % chamber

    writer = csv.writer(response)
    writer.writerow(['Bioguide', 'Member', 'State', 'District', 'Party', 'Official Twitter', 'Official Twitter Statuses', 'Official Twitter Change', 'Official Facebook', 'Official Facebook Change', 'Campaign Twitter', 'Campaign Twitter Statuses', 'Campaign Twitter Change', 'Campaign Facebook', 'Campaign Facebook Change', 'Date'])
    for member in members:
        report = member.latest_report()
        if report:
            writer.writerow([member.bioguide_id, member, member.state, member.district, member.party, report.official_twitter_followers, report.official_twitter_updates, member.change_from_previous('official_twitter'), report.official_facebook_likes, member.change_from_previous('official_facebook'), report.campaign_twitter_followers, report.campaign_twitter_updates, member.change_from_previous('campaign_twitter'), report.campaign_facebook_likes, member.change_from_previous('campaign_facebook'), report.date])
    return response
