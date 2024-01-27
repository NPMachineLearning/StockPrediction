FROM python:3.9.18-slim
WORKDIR /app
# update container system
RUN apt-get update
# install cron
RUN apt-get install -y cron
ADD ./libs libs
# install modules
RUN pip3 install -r ./libs/requirements.txt
COPY ./stock_manager/stock_processor.py .
COPY ./stock_manager/run.sh .
COPY ./stock_manager/stock_cronjob.cron .
# make sure cronjob can be runned
RUN chmod 0644 stock_cronjob.cron
# run bash shell
ENTRYPOINT [ "./run.sh" ]
