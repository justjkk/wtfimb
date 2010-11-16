from django.conf.urls.defaults import *

urlpatterns = patterns('htfs.views',
   url(r'^$', 'index'),
   url(r'^agency.txt$', 'agency_txt', name='agency_txt'),
   url(r'^stops.txt$', 'stops_txt', name='stops_txt'),
   url(r'^stages.txt$', 'stages_txt', name='stages_txt'),
   url(r'^routes.txt$', 'routes_txt', name='routes_txt'),
   url(r'^trips.txt$', 'trips_txt', name='trips_txt'),
   url(r'^stop_times.txt$', 'stop_times_txt', name='stop_times_txt'),
   url(r'^calendar.txt$', 'calendar_txt', name='calendar_txt'),
   url(r'^calendar_dates.txt$', 'calendar_dates_txt', name='calendar_dates_txt'),
   url(r'^fare_attributes.txt$', 'fare_attributes_txt', name='fare_attributes_txt'),
   url(r'^fare_rules.txt$', 'fare_rules_txt', name='fare_rules_txt'),
   url(r'^shapes.txt$', 'shapes_txt', name='shapes_txt'),
   url(r'^frequencies.txt$', 'frequencies_txt', name='frequencies_txt'),
   url(r'^transfers.txt$', 'transfers_txt', name='transfers_txt'),
   url(r'^carriers.txt$', 'carriers_txt', name='carriers_txt'),
)
