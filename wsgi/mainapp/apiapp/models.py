# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Remainders(models.Model):
    id = models.AutoField(primary_key=True)
    travel_date_time = models.DateTimeField(db_column='travelDateTime', blank=False, null=False) # Field name made lowercase.
    emailid = models.EmailField(db_column='emailID', max_length=200, blank=False, null=False) # Field name made lowercase.
    srclat = models.FloatField(db_column='srcLat', blank=False, null=False) # Field name made lowercase.
    srclong = models.FloatField(db_column='srcLong', blank=False, null=False) # Field name made lowercase.
    destlat = models.FloatField(db_column='destLat', blank=False, null=False) # Field name made lowercase.
    destlong = models.FloatField(db_column='destLong', blank=False, null=False) # Field name made lowercase.
    # tentativegooglemaptime in min approx
    tentativegooglemaptime = models.DateTimeField(db_column='tentativeGoogleMapTime', null=True) # Field name made lowercase.
    remaindersent = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'remainders'
        