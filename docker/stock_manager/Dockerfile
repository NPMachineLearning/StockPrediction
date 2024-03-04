FROM python:3.9.18-slim

WORKDIR /app

# update container system packages
RUN apt-get update

# install cron
RUN apt-get install -y cron

# copy libraries folder
ADD ./libs libs

# install libraries' module
RUN pip3 install -r ./libs/requirements.txt

# copy main script
COPY ./stock_manager/stock_processor.py .

# copy config listener script
COPY ./stock_manager/stock_config_listener.py .

# copy run bash shell script
COPY ./stock_manager/run.sh .

# ! important convert run bash shell script from CRLF to LF for linux
RUN python ./libs/convert_crlf_to_lf.py ./run.sh

# copy cron job file
COPY ./stock_manager/stock_cronjob.cron .

# ! important convert cron job file from CRLF to LF for linux
RUN python ./libs/convert_crlf_to_lf.py ./stock_cronjob.cron

# make sure cronjob can be runned
RUN chmod 0644 stock_cronjob.cron

# run bash shell
ENTRYPOINT [ "./run.sh" ]
