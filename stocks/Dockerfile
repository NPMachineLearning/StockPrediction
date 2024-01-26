FROM python:3.9.18-slim
WORKDIR /stocks
# update container system
RUN apt-get update
# install cron
RUN apt-get install -y cron
ADD ./utils utils
# install modules
RUN pip3 install -r ./utils/requirements.txt
COPY ./stocks/stock_processor.py .
COPY ./stocks/run.sh .
COPY ./stocks/stock_cronjob .
# make sure cronjob can be runned
RUN chmod 0644 stock_cronjob
# run bash shell
ENTRYPOINT [ "./run.sh" ]
