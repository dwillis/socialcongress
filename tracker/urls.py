from django.conf.urls.defaults import patterns, include, url
from django.utils.functional import curry
from django.views.defaults import server_error, page_not_found

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

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
