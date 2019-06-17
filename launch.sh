#!/bin/bash

gunicorn run:app -p compose.pid -b ${FLASK_HOST:-127.0.0.1}:${FLASK_PORT:-9991} 