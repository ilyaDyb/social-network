#!/bin/bash

python manage.py migrate

if [ "$LOAD_FIXTURES" = "1" ]; then
  echo "Loading fixtures..."
  for fixture in fixtures/*.json; do
    python manage.py loaddata "$fixture"
  done
else
  echo "Skipping fixture loading."
fi

python manage.py collectstatic --noinput
uvicorn application.asgi:application --host 0.0.0.0 --port 8000
exec "$@"