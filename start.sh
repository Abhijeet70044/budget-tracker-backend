#!/bin/bash
# Start Django app with Gunicorn on port 8000 or $PORT if set, binding to all addresses
PORT=${PORT:-8000}
exec gunicorn budget_tracker.wsgi:application --bind 0.0.0.0:$PORT --workers 3
