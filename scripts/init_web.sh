#!/bin/bash

set -euo pipefail

poetry run python manage.py collectstatic --noinput
uvicorn benny.asgi:application --host 0.0.0.0 --port 8000
