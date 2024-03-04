FROM mongo
RUN apt-get update
RUN apt-get install -y python3
COPY ./mongodb/init_stock_config.js /docker-entrypoint-initdb.d
COPY ./mongodb/init_rs.sh /
COPY ./libs/convert_crlf_to_lf.py /
# ! important convert init_rs.sh bash shell script from CRLF to LF for linux
RUN python3 ./convert_crlf_to_lf.py /init_rs.sh

COPY ./mongodb/mongodbkey /
# change owner right
RUN chown 999:999 /mongodbkey
RUN chmod 400 /mongodbkey
RUN chmod +x /init_rs.sh


