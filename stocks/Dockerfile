FROM ubuntu:22.04
ADD ./utils /stocks/utils
COPY ./stock_processor.py /stocks
COPY ./requirements.txt /stocks
RUN apt update
RUN apt install -y python3-pip
RUN apt install -y python3
RUN pip install -r /stocks/requirements.txt
CMD python3 /stocks/stock_processor.py