#Set Environment variable for Django applications
import os
import sys

sys.path.append('./mainapp')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mainapp.settings")

#Create WSGI application request
from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware
from django.core.handlers import wsgi

application = DispatcherMiddleware(wsgi.WSGIHandler(),)

if __name__ == "__main__":
    run_simple('127.0.0.1', 5000, application, use_reloader=True, use_debugger=True)