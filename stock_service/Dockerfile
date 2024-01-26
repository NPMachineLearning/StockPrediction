FROM python:3.9.18-slim
WORKDIR /stock_service
# update container system
RUN apt-get update
COPY ./stock_service/requirements.txt .
ADD ./utils utils
# install modules
RUN pip3 install -r requirements.txt
# install modules
RUN pip3 install -r ./utils/requirements.txt
COPY ./stock_service/main.py .
COPY ./stock_service/run.sh .
# run bash shell
ENTRYPOINT [ "./run.sh" ]