from django.conf.urls.defaults import patterns, include, url
from django.utils.functional import curry
from django.views.defaults import server_error, page_not_found
from tracker.api import MemberResource, ReportResource
from tastypie.api import Api

v1_api = Api(api_name='v1')
v1_api.register(MemberResource())
v1_api.register(ReportResource())

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

handler500 = curry(server_error, template_name='admin/500.html')
handler404 = curry(page_not_found, template_name='admin/404.html')

urlpatterns = patterns('tracker.views',
    # Examples:
    # url(r'^$', 'socialcongress.views.home', name='home'),
    url(r'^admin/_update$', 'update', name="update"),
    url(r'^admin/chamber/(?P<chamber>[-a-z]+)/$', 'chamber_csv', name='admin_chamber_csv'),
    url(r'^admin/weekly/chamber/(?P<chamber>[-a-z]+)/$', 'weekly_csv', name='admin_weekly_csv'),
    #url(r'^reports/weeks/$', 'week_index', name='week_index'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # API urls
    url(r'^api/', include(v1_api.urls)),
)
