#!/bin/bash
exec gunicorn dus.wsgi:application  --bind 0.0.0.0:8000 --workers 6 --limit-request-line 65535 -t 300