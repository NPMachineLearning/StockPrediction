#!/bin/bash

# !! Make sure this file is LF for end of line sequence !!

# schedule cronjob
echo "Schedule cronjob"
crontab stock_cronjob.cron

# run stock processor once
echo "Process stocks"
/usr/local/bin/python3 stock_processor.py

# run cron at foreground
echo "Run cron"
cron

echo "Run config listener"
/usr/local/bin/python3 stock_config_listener.py