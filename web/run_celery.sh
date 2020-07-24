#!/bin/sh
#celery worker -A codingclash -l info
celery -A codingclash worker -B -E -l info
