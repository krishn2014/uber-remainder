
The Django app resides in 'wsgi' folder. Application logic is in folder apiapp.

SETUP
======

Replace the variables EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in mainapp/settings.py with valid email and password.

One can directly deploy the project in Openshift or can run locally using the following steps:

1. cd into folder 'wsgi/mainapp'
2. Initialize databse 'almabase' using "python manage.py syncdb"
3. To run the application go to 'wsgi/mainapp' and execute "python manage.py runserver"
4. One also need to set a cron job to send email remainders. setup cronjob to execute the following cmd 'python manage.py runcrons'
5. For can be viewed @ URI "http://localhost:8000/form/"


NOTES
======

Replace the variables EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in mainapp/settings.py with valid email and password before starting.
Travel date and time should be given in format MM/DD/YYYY HH:MM example: 07/24/2016 17:00
Logic to send remainder is in file 'wsgi/mainapp/apiapp/cronjob.py'.

Reference for django crons: https://github.com/Tivix/django-cron


