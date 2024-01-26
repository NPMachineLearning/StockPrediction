FROM python:3.9.18-slim
WORKDIR /stock_service
ADD ./utils utils
COPY ./stock_service/main.py .
COPY ./stock_service/requirements.txt .
COPY ./stock_service/run.sh .
# update container system
RUN apt-get update
# install modules
RUN pip3 install -r requirements.txt
# run bash shell
ENTRYPOINT [ "./run.sh" ]