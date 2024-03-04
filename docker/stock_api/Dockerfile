FROM python:3.9.18-slim

WORKDIR /app

# update container system packages
RUN apt-get update

# copy requirements file for main program
COPY ./stock_api/requirements.txt .

# install main program's modules
RUN pip3 install -r requirements.txt

# copy libraries folder
ADD ./libs libs

# install libraries' module
RUN pip3 install -r ./libs/requirements.txt

# copy main script
COPY ./stock_api/main.py .

# copy run bash shell script
COPY ./stock_api/run.sh .

# ! important convert run bash shell script from CRLF to LF for linux
RUN python ./libs/convert_crlf_to_lf.py ./run.sh

# run bash shell
ENTRYPOINT [ "./run.sh" ]