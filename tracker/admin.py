from django.contrib import admin
from tracker.models import Member, Report, Error

class MemberAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("first_name","last_name")}
    search_fields = ['last_name']
    list_display = ('bioguide_id', '__unicode__', 'state', 'party', 'district', 'date_of_birth')
    list_filter = ('party', 'branch', 'state')
    
class ReportAdmin(admin.ModelAdmin):
    search_fields = ['member__last_name']
    list_display = ('member', 'official_facebook_likes', 'official_twitter_followers', 'official_twitter_updates', 'campaign_facebook_likes', 'campaign_twitter_followers', 'campaign_twitter_updates', 'date')

class ErrorAdmin(admin.ModelAdmin):
    list_display = ('member', 'date', 'message')
    
admin.site.register(Member, MemberAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Error, ErrorAdmin)