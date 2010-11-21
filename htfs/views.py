import csv
import datetime
from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
from models import *
def index(request):
   return direct_to_template(request, 'htfs/index.html')

def format_datetime(data_row):
   formatted_data_row = {}
   for key,value in data_row.items():
      if type(value) == datetime.date:
         formatted_data_row[key] = value.strftime("%Y%m%d")
      else:
         formatted_data_row[key] = value
   return formatted_data_row

def csv_response(data, data_caption):
   response = HttpResponse(mimetype='text/csv')
   response['Content-Disposition'] = 'attachment'
   header_writer = csv.writer(response)
   header_writer.writerow(data_caption)
   content_writer = csv.DictWriter(response, data_caption, extrasaction='ignore')
   for data_row in data:
      formatted_data_row = format_datetime(data_row.__dict__)
      content_writer.writerow(formatted_data_row)
   return response

def agency_txt(request):
   agencies = Agency.objects.order_by('agency_id')
   agency_fields = ['agency_id','agency_name','agency_url','agency_timezone',
                    'agency_lang','agency_phone']
   return csv_response(agencies, agency_fields)

def stops_txt(request):
   stops = Stop.objects.order_by('stop_id')
   stops_fields = ['stop_id','stop_code','stop_name','stop_desc','stop_lat',
                    'stop_lon','zone_id','stop_url','location_type',
                    'parent_station','parent_stage','stage_main_stop','stop_osm_node_id',
                    'stop_wikipedia_url','verified_stop']
   return csv_response(stops, stops_fields)

def stages_txt(request):
   stages = Stage.objects.order_by('stage_id')
   stages_fields = ['stage_id','stage_name','agency_stage_name','stage_lat','stage_lon',
                    'stage_url','stage_type','stage_rank','stage_desc']
   return csv_response(stages, stages_fields)

def routes_txt(request):
   routes = Route.objects.order_by('route_id')
   routes_fields = ['route_id','agency_id','route_short_name','route_long_name',
                    'route_desc','route_type','route_url','route_color','route_text_color',
                    'agency_route_name','agency_route_distance','agency_route_duration',
                    'route_osm_relation_id']
   return csv_response(routes, routes_fields)

def trips_txt(request):
   trips = Trip.objects.order_by('trip_id')
   trips_fields = ['route_id','service_id','trip_id','trip_headsign','trip_short_name',
                   'direction_id','block_id','shape_id','carrier_id','agency_trip_type']
   return csv_response(trips, trips_fields)

def stop_times_txt(request):
   stop_times = StopTime.objects.order_by('stop_id')
   stop_times_fields = ['trip_id','arrival_time','departure_time','stop_id','stop_sequence',
                        'stop_headsign','pickup_type','drop_off_type','shape_dist_traveled',
                        'stage_id','stage_sequence']
   return csv_response(stop_times, stop_times_fields)

def calendar_txt(request):
   calendar = Calendar.objects.order_by('service_id')
   calendar_fields = ['service_id','monday','tuesday','wednesday','thursday','friday',
                      'saturday','sunday','start_date','end_date']
   return csv_response(calendar, calendar_fields)

def calendar_dates_txt(request):
   calendar_dates = CalendarDate.objects.order_by('service_id')
   calendar_dates_fields = ['service_id','date','exception_type']
   return csv_response(calendar_dates, calendar_dates_fields)

def fare_attributes_txt(request):
   fare_attributes = FareAttribute.objects.order_by('fare_id')
   fare_attributes_fields = ['fare_id','price','currency_type','payment_method','transfers',
                             'transfer_duration','min_price','stage_price','distance_price',
                             'distance_unit','max_price']
   return csv_response(fare_attributes, fare_attributes_fields)

def fare_rules_txt(request):
   fare_rules = FareRule.objects.order_by('fare_id')
   fare_rules_fields = ['fare_id','route_id','origin_id','destination_id','contains_id']
   return csv_response(fare_rules, fare_rules_fields)

def shapes_txt(request):
   shapes = Shape.objects.order_by('shape_id')
   shapes_fields = ['shape_id','shape_pt_lat','shape_pt_lon','shape_pt_sequence',
                    'shape_dist_traveled']
   return csv_response(shapes, shapes_fields)

def frequencies_txt(request):
   frequencies = Frequency.objects.order_by('trip_id')
   frequencies_fields = ['trip_id','start_time','end_time','headway_secs']
   return csv_response(frequencies, frequencies_fields)

def transfers_txt(request):
   transfers = Transfer.objects.order_by('from_stop_id')
   transfers_fields = ['from_stop_id','to_stop_id','transfer_type','min_transfer_time',
                       'from_stage_id','to_stage_id','transfer_desc']
   return csv_response(transfers, transfers_fields)

def carriers_txt(request):
   carriers = Carrier.objects.order_by('carrier_id')
   carriers_fields = ['carrier_id','carrier_name','carrier_chassis','carrier_model',
                      'carrier_desc','carrier_type','low_floor','air_conditioned',
                      'seating_capacity','standing_capacity','seat_comfort']
   return csv_response(carriers, carriers_fields)

