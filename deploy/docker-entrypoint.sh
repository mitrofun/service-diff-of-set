#!/usr/bin/env bash

set -e
set -u

cd /opt/app
[ -d media ] || mkdir media
alembic upgrade head
uvicorn src.main:app --host 0.0.0.0 --port 8000
