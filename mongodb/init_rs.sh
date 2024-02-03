#!/bin/bash

# $MONGO_INITDB_ROOT_USERNAME vairable is from docker environment variable
# $MONGO_INITDB_ROOT_PASSWORD vairable is from docker environment variable
mongosh -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD --eval "
rs.initiate({
    _id:'rs0',
    members:[
        {_id:0, host:'host.docker.internal:27017', priority:1}]
});
rs.status();
"
mongosh -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD --eval "db.adminCommand('ping')"
