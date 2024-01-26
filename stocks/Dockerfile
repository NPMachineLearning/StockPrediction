FROM python:3.9.18-slim
WORKDIR /stocks
ADD ./utils utils
COPY ./stocks/stock_processor.py .
COPY ./stocks/requirements.txt .
COPY ./stocks/run.sh .
COPY ./stocks/stock_cronjob .
# update container system
RUN apt-get update
# install cron
RUN apt-get install -y cron
# install modules
RUN pip3 install -r requirements.txt
# make sure cronjob can be runned
RUN chmod 0644 stock_cronjob
# run bash shell
ENTRYPOINT [ "./run.sh" ]
