#!/bin/bash

# schedule cronjob
crontab stock_cronjob

# run stock processor once
/usr/local/bin/python3 stock_processor.py

# run cron at foreground
cron -f