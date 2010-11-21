from django.contrib.gis.db import models

STOP_LOCATION_TYPE_CHOICES = (
   ('0', 'Normal Stop'),
   ('1', 'Bus Station'),
)

STOP_STAGE_MAIN_STOP_CHOICES = (
   ('0', 'Normal Stop'),
   ('1', 'Main Stop'),
)

STAGE_TYPE_CHOICES = (
   ('0', 'Through Stage'),
   ('1', 'Terminal Stage'),
)

ROUTE_TYPE_CHOICES = (
   ('1', 'Metro'),
   ('2', 'Rail'),
   ('3', 'Bus'),
   ('4', 'Ferry'),
   ('10', 'Share Taxi(unlicensed)'),
   ('11', 'Share Autorickshaw'),
)

TRIP_DIRECTION_ID_CHOICES = (
   ('0', 'From Operating Depot'),
   ('1', 'Towards Operating Depot'),
)

STOP_TIME_PICKUP_TYPE_CHOICES = (
   ('0', 'Regular Scheduled Stop'),
   ('1', 'No Stop, Express Service'),
)

CALENDAR_WEEKDAY_CHOICES = (
   ('0', 'Service doesn\'t run'),
   ('1', 'Service runs as scheduled'),
)

CALENDAR_DATE_EXCEPTION_TYPE_CHOICES = (
   ('1', 'Service Added'),
   ('2', 'Service Removed'),
)

STOP_TIME_DROP_OFF_TYPE_CHOICES = STOP_TIME_PICKUP_TYPE_CHOICES

FARE_ATTRIBUTE_PAYMENT_METHOD_CHOICES = (
   ('0', 'On board'),
   ('1', 'Before boarding'),
)

FARE_ATTRIBUTE_TRANSFERS_CHOICES = (
   ('0', 'No transfers'),
   ('1', '1 transfer'),
   ('2', '2 transfers'),
   ('', 'Unlimited transfers'),
)

TRANSFER_TYPE_CHOICES = (
   ('0', 'Recommended Transfer point'),
   ('2', 'Requires minimum amt of time'),
)

CARRIER_TYPE_CHOICES = ROUTE_TYPE_CHOICES

CARRIER_SEAT_COMFORT_CHOICES = (
   ('0', 'Bench Type'),
   ('1', 'Fixed Seat'),
   ('2', 'Reclining/Semi-sleeper'),
   ('3', 'Full Sleeper'),
)

''' XTimeField is a CharField that stores Time Instances
''  TimeField cannot be used because GTFS defines Time values to exceed 24 hours.
'''
class XTimeField(models.CharField): #TODO: Implement Validation
   def __init__(self, *args, **kwargs):
      kwargs['max_length'] = 8
      kwargs['help_text'] = "Format time as HH:MM:SS"
      super(XTimeField, self).__init__(*args, **kwargs)

class Agency(models.Model):
   agency_id = models.AutoField(primary_key=True)
   agency_name = models.CharField(max_length=100)
   agency_url = models.URLField()
   agency_timezone = models.CharField(max_length=50)
   agency_lang = models.CharField(max_length=2, blank=True)
   agency_phone = models.CharField(max_length=18, blank=True)

class Stop(models.Model):
   stop_id = models.AutoField(primary_key=True)
   stop_code = models.CharField(max_length=30, blank=True)
   stop_name = models.CharField(max_length=100)
   stop_desc = models.TextField(blank=True)
   stop_lat = models.FloatField(editable=False)
   stop_lon = models.FloatField(editable=False)
   zone_id = models.IntegerField(null=True, blank=True)
   stop_url = models.URLField(null=True, blank=True)
   location_type = models.CharField(max_length=2, choices=STOP_LOCATION_TYPE_CHOICES, blank=True)
   parent_station = models.ForeignKey('Stop', null=True, blank=True)
   parent_stage = models.ForeignKey('Stage')
   stage_main_stop = models.CharField(max_length=2, choices=STOP_STAGE_MAIN_STOP_CHOICES)
   stop_osm_node_id = models.IntegerField(max_length=15, null=True, blank=True)
   stop_wikipedia_url = models.URLField(null=True, blank=True)
   verified_stop = models.IntegerField(default=0)

   location = models.PointField()
   objects = models.GeoManager()

   def save(self, *args,**kwargs):
      self.stop_lat = self.location.y
      self.stop_lon = self.location.x
      super(Stop, self).save(*args, **kwargs)

class Stage(models.Model):
   stage_id = models.AutoField(primary_key=True)
   stage_name = models.CharField(max_length=100)
   agency_stage_name = models.CharField(max_length=100, blank=True)
   stage_lat = models.FloatField(editable=False)
   stage_lon = models.FloatField(editable=False)
   stage_url = models.URLField(null=True, blank=True)
   stage_type = models.CharField(max_length=2, choices=STAGE_TYPE_CHOICES)
   stage_rank = models.IntegerField(default=0)
   stage_desc = models.TextField(blank=True)

   location = models.PointField()
   objects = models.GeoManager()

   def save(self, *args,**kwargs):
      self.stage_lat = self.location.y
      self.stage_lon = self.location.x
      super(Stage, self).save(*args, **kwargs)

class Route(models.Model):
   route_id = models.AutoField(primary_key=True)
   agency_id = models.ForeignKey('Agency')
   route_short_name = models.CharField(max_length=100)
   route_long_name = models.CharField(max_length=100)
   route_desc = models.TextField(blank=True)
   route_type = models.CharField(max_length=2, choices=ROUTE_TYPE_CHOICES)
   route_url = models.URLField(null=True, blank=True)
   route_color = models.CharField(max_length=6, default='FFFFFF', blank=True)
   route_text_color = models.CharField(max_length=6, default='000000', blank=True)
   agency_route_name = models.CharField(max_length=100, blank=True)
   agency_route_distance = models.FloatField(null=True, blank=True)
   agency_route_duration = models.IntegerField(null=True, blank=True, help_text='Travel time in minutes')
   route_osm_relation_id = models.IntegerField(max_length=10, null=True, blank=True)

class Trip(models.Model):
   route_id = models.ForeignKey('Route')
   service_id = models.ForeignKey('Calendar')
   trip_id = models.AutoField(primary_key=True)
   trip_headsign = models.CharField(max_length=100, blank=True)
   trip_short_name = models.CharField(max_length=30, blank=True)
   direction_id = models.CharField(max_length=2, choices=TRIP_DIRECTION_ID_CHOICES, blank=True)
   block_id = models.IntegerField(null=True, blank=True)
   shape_id = models.ForeignKey('Shape', null=True, blank=True)
   carrier_id = models.ForeignKey('Carrier', null=True, blank=True)
   agency_trip_type = models.CharField(max_length=15, blank=True) #FIXME: What should be entered?

class StopTime(models.Model):
   trip_id = models.ForeignKey('Trip')
   arrival_time = XTimeField()
   departure_time = XTimeField()
   stop_id = models.ForeignKey('Stop')
   stop_sequence = models.IntegerField()
   stop_headsign = models.CharField(max_length=100, blank=True)
   pickup_type = models.CharField(max_length=2, choices=STOP_TIME_PICKUP_TYPE_CHOICES, blank=True)
   drop_off_type = models.CharField(max_length=2, choices=STOP_TIME_DROP_OFF_TYPE_CHOICES, blank=True)
   shape_dist_traveled = models.FloatField(null=True, blank=True)
   stage_id = models.ForeignKey('Stage')
   stage_sequence = models.IntegerField()

class Calendar(models.Model):
   service_id = models.AutoField(primary_key=True)
   monday = models.CharField(max_length=2, choices=CALENDAR_WEEKDAY_CHOICES)
   tuesday = models.CharField(max_length=2, choices=CALENDAR_WEEKDAY_CHOICES)
   wednesday = models.CharField(max_length=2, choices=CALENDAR_WEEKDAY_CHOICES)
   thursday = models.CharField(max_length=2, choices=CALENDAR_WEEKDAY_CHOICES)
   friday = models.CharField(max_length=2, choices=CALENDAR_WEEKDAY_CHOICES)
   saturday = models.CharField(max_length=2, choices=CALENDAR_WEEKDAY_CHOICES)
   sunday = models.CharField(max_length=2, choices=CALENDAR_WEEKDAY_CHOICES)
   start_date = models.DateField()
   end_date = models.DateField()

class CalendarDate(models.Model):
   service_id = models.AutoField(primary_key=True)
   date = models.DateField()
   exception_type = models.CharField(max_length=2, choices=CALENDAR_DATE_EXCEPTION_TYPE_CHOICES)

class FareAttribute(models.Model):
   fare_id = models.AutoField(primary_key=True)
   price = models.FloatField()
   currency_type = models.CharField(max_length=3)
   payment_method = models.CharField(max_length=2, choices=FARE_ATTRIBUTE_PAYMENT_METHOD_CHOICES)
   transfers = models.CharField(max_length=2, choices=FARE_ATTRIBUTE_TRANSFERS_CHOICES, blank=True)
   transfer_duration = models.IntegerField(null=True, blank=True)
   min_price = models.FloatField()
   stage_price = models.FloatField()
   distance_price = models.FloatField()
   distance_unit = models.FloatField(default=1)
   max_price = models.FloatField()

class FareRule(models.Model):
   fare_id = models.AutoField(primary_key=True)
   route_id = models.ForeignKey('Route', null=True, blank=True)
   origin_id = models.IntegerField(null=True, blank=True)
   destination_id = models.IntegerField(null=True, blank=True)
   contains_id = models.IntegerField(null=True, blank=True)

class Shape(models.Model):
   shape_id = models.AutoField(primary_key=True)
   shape_pt_lat = models.FloatField(editable=False)
   shape_pt_lon = models.FloatField(editable=False)
   shape_pt_sequence = models.IntegerField()
   shape_dist_traveled = models.FloatField(null=True, blank=True)

   location = models.PointField()
   objects = models.GeoManager()

   def save(self, *args,**kwargs):
      self.shape_pt_lat = self.location.y
      self.shape_pt_lon = self.location.x
      super(Shape, self).save(*args, **kwargs)

class Frequency(models.Model):
   trip_id = models.ForeignKey('Trip')
   start_time = XTimeField()
   end_time = XTimeField()
   headway_secs = models.IntegerField()

class Transfer(models.Model):
   from_stop_id = models.ForeignKey('Stop', related_name='transfers_from')
   to_stop_id = models.ForeignKey('Stop', related_name='transfers_to')
   transfer_type = models.CharField(max_length=2, choices=TRANSFER_TYPE_CHOICES)
   min_transfer_time = models.IntegerField(null=True, blank=True)
   from_stage_id = models.ForeignKey('Stage', related_name='transfers_from')
   to_stage_id = models.ForeignKey('Stage', related_name='transfers_to')
   transfer_desc = models.CharField(max_length=200, blank=True)

class Carrier(models.Model):
   carrier_id = models.AutoField(primary_key=True)
   carrier_name = models.CharField(max_length=30)
   carrier_chassis = models.CharField(max_length=30, blank=True)
   carrier_model = models.CharField(max_length=50, blank=True)
   carrier_desc = models.TextField(blank=True)
   carrier_type = models.CharField(max_length=2, choices=CARRIER_TYPE_CHOICES, blank=True)
   low_floor = models.NullBooleanField(null=True, blank=True)
   air_conditioned = models.NullBooleanField(null=True, blank=True)
   seating_capacity = models.IntegerField(null=True, blank=True)
   standing_capacity = models.IntegerField(null=True, blank=True)
   seat_comfort = models.CharField(max_length=2, choices=CARRIER_SEAT_COMFORT_CHOICES)
   
