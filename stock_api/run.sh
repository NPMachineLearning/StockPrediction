#!/bin/bash

# !! Make sure this file is LF for end of line sequence !!

# Start uvicorn server
echo "Start uvicorn"
/usr/local/bin/uvicorn  --host=0.0.0.0 --port=8002 main:app