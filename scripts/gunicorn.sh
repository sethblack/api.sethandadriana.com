#!/bin/bash

NAME="sethandadriana"                           # Name of the application
DJANGODIR=/home/website/site/snaapi    # Django project directory
BIND=unix:/tmp/gunicorn.sock # we will communicate using this unix socket
USER=website                             # the user to run as
GROUP=website                            # the group to run as
NUM_WORKERS=3                            # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=snaapi.settings      # which settings file should Django use
DJANGO_WSGI_MODULE=snaapi.wsgi              # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /home/atlassite/web/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $BIND)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec /home/atlassite/web/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --log-level=error \
  --timeout=60 \
  --bind=$BIND