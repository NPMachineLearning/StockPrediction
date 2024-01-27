FROM python:3.9.18-slim
WORKDIR /app
# update container system
RUN apt-get update
COPY ./stock_api/requirements.txt .
# install modules
RUN pip3 install -r requirements.txt
ADD ./libs libs
# install modules
RUN pip3 install -r ./libs/requirements.txt
COPY ./stock_api/main.py .
COPY ./stock_api/run.sh .
# run bash shell
ENTRYPOINT [ "./run.sh" ]