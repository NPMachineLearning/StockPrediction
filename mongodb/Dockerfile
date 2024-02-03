FROM mongo
COPY ./init_stock_config.js /docker-entrypoint-initdb.d
COPY ./init_rs.sh /
# ! important convert run bash shell script from CRLF to LF for linux
RUN python ./libs/convert_crlf_to_lf.py /run.sh
COPY ./mongodbkey /
RUN chown 999:999 /mongodbkey
RUN chmod 400 /mongodbkey
RUN chmod +x /init_rs.sh


