from django_cron import CronJobBase, Schedule
from django.db.models import Count
from django.core.mail import EmailMessage
from serializers import *
from datetime import timedelta
import logging
import json
import datetime
import requests

from models import *

from rest_framework.renderers import JSONRenderer
import os

if os.environ.has_key('OPENSHIFT_REPO_DIR'):
    logFile_Sent = os.path.join(os.environ['OPENSHIFT_DATA_DIR'], "NotificationSent.log")
else:
    logFile_Sent = "NotificationSent.log"

logging.basicConfig(filename = logFile_Sent, filemode = 'a', level = logging.DEBUG,
                    format = '%(asctime)s - %(levelname)s: %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p')       

UBER_SERVER_TOKEN = "BPehDhjfmMaomcn2ZbnWuyaqRzrZoTS1ezAMlZs1"

UBERGO_PRODUCT_ID = 'db6779d6-d8da-479f-8ac7-8068f4dade6f'
UBER_TIME_URI = 'https://api.uber.com/v1/estimates/time'

GOOGLE_MAP_KEY = "AIzaSyB6ky0s6kmaxH15hsxsNHKuZeI6n_OG2eA"
GOOGLE_MAP_TIME_ESTIMATE_URI = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric"

def get_uber_arrival_time(src_lat, src_long):
    parameters = {
        'server_token': UBER_SERVER_TOKEN,
        'start_latitude': src_lat,
        'start_longitude': src_long,
        'product_id' : UBERGO_PRODUCT_ID,
    }

    response = requests.get(UBER_TIME_URI, params=parameters)
    data = response.json()  
    return  data['times'][0]['estimate']

def get_google_estimate_time(src_latitude, src_longitude, dest_latitude, dest_longitude):
    """ returns google estimate time in mins or None in case of error"""
    request_uri =  GOOGLE_MAP_TIME_ESTIMATE_URI + "&origins=%s,%s&destinations=%s,%s&key=%s" % (src_latitude, src_longitude, dest_latitude, dest_longitude, GOOGLE_MAP_KEY)
    response = requests.get(request_uri)
    if response.status_code != 200:
        return None
    data = response.json()
    # returning the first element to keep things simple
    return (data['rows'][0]['elements'][0]['duration']['value'])

class GenerateNotificationCronJob(CronJobBase):
    '''
    Generates notication for users
    '''
    RUN_EVERY_MINS = 2 # run every 2 mins

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'apiapp.GenerateNotificationCronJob'    # a unique code

    def __init__(self):
        super(GenerateNotificationCronJob, self).__init__()

    def send_remainder(self, entity):
        body = "Gentle remainder: Time to book Uber from (%s, %s) to (%s, %s)" % (entity.srclat, entity.srclong, entity.destlat, entity.destlong)
        email = EmailMessage('Remainder: Time to book Uber', body, to=[entity.emailid])
        email.send()
        entity.remaindersent = True
        entity.save()

    def populate_tentativegooglemaptime(self):
        items = Remainders.objects.filter(tentativegooglemaptime=None)

        for item in items:

            # updating tuple's tentativegooglemaptime
            get = get_google_estimate_time(item.srclat, item.srclong, item.destlat, item.destlong)
            d = timedelta(seconds = get)
            item.tentativegooglemaptime = item.travel_date_time - d
            item.save()

    def do(self):
        # write your logic for generating notifications
        logging.info("notification generation started.")

        # query for rows in which tentative time is not provided and update the tentaitve time
        self.populate_tentativegooglemaptime()

        # query for rows in where { (sch time - google tentative time - 60 -30 (max time assumed for uberGO to arrive)) <= current time } for sending the notification
        curr = datetime.datetime.now()
        d = timedelta(seconds = 1800 + 3600)

        items = Remainders.objects.filter(tentativegooglemaptime__lte = (curr + d), remaindersent=False)

        # getting uber arrival time
        for item in items:
            uat = get_uber_arrival_time(item.srclat, item.srclong)

            # send notification if time for uber to arrive is > 15 mins or if the tentative time - curr time <= 15 mins
            if uat >= 900:
                self.send_remainder(item)
            else:
                if item.tentativegooglemaptime <= (curr + timedelta(seconds = 3600 + uat)):
                    self.send_remainder(item)

        logging.info("notification generation completed")
