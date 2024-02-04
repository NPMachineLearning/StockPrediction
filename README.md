# Stock Prediction

The purpose of this project is to grab Yahoo's financial stocks' data and then use meachine learning to make prediction for stocks. Store stock data and prediction in database.

The project is docker based and each services are containerized.

# Run on local machine

1. Make sure [docker](https://www.docker.com/products/docker-desktop/#) is installed.
2. Download env files template [here](https://drive.google.com/drive/folders/12vQ9ApwkVmEPrRtOjkXxueJ9vpUiXzQ6?usp=sharing).
3. Move or copy **.env** file `docker_env/.env` to project's root directory and change value if needed.
4. Move or copy **.env** file `libs_env/.env` to project's `libs` folder and change value if needed.
5. Install [openssl](https://www.openssl.org/source/) if not installed.
6. Generate a security key for mongodb.
   `openssl rand -base64 741 > [path_to_project]/mongodb/mongodbkey`. Key file name must be **mongodbkey**.
7. Open terminal and go to project root directory.
8. Run command `docker-compose up -d --build` for detach mode or `docker-compose up --build` for none detach mode.
9. To shutdown services `docker-compose down`.

# Run development on local machine

This will only start database related services. Therefore we can debug or test code in local machine.

1. Go through steps 1 ~ 7 for **Run on local machine**.
2. Run command `docker-compose -f docker-compose-dev.yml up -d --build` for detach mode or `docker-compose -f docker-compose-dev.yml up --build` for none detach mode.
3. 11. To shutdown services `docker-compose -f docker-compose-dev.yml down`.

# Docker containers/services

Number of containers/services will start when docker-compose is up.

- [**mysql database**](https://hub.docker.com/_/mysql): For storing stock and prediction data.
- [**admine**](https://hub.docker.com/_/adminer): User interface for mysql database.
- [**mongo database**](https://hub.docker.com/_/mongo): NoSQL database for storing configuration values.
- [**mongo-express**](https://hub.docker.com/_/mongo-express): User interface for monogo database.
- **stock_api**: Backend Restful endpoint api.
- **stock_manager**: Processing stock data and listen for configuration file updated.

# Architecture

![image](https://images.unsplash.com/photo-1706947329131-1aa452641f74?q=80&w=2017&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D)

# Database

Two database is used for the project [MySQL](https://www.mysql.com/) and [MongoDB](https://www.mongodb.com/). MySQL(table like) database is used for storing stock and prediction data. In contrast MongoDB(JSON like) is used for storing configuration data which will be used during stock's data processing.

# Backend API

The API provide stock and configuration data.
The backend api service running at port 8002 by default.

To consume api `http://localhost:8002`.
To see how to use api or what api is avaliable `http://locahost:8002/docs`.

# Libraries

The following python libraries are used in the project.

Make sure they are installed in development environment when doing local machine development.

- mysql_connector_python==8.3.0
- numpy==1.24.4
- pandas==2.0.3
- pymongo==4.6.1
- python-dotenv==1.0.1
- scikit_learn==1.3.2
- SQLAlchemy==2.0.25
- yfinance==0.2.35
- fastapi==0.109.0
- labelImg==1.8.6
- pydantic==2.6.0
- uvicorn==0.27.0

# Project structure

## Root directory

- [libs/](./libs)
- [mongodb/](./mongodb)
- [stock_api/](./stock_api)
- [stock_manager/](./stock_manager)
- [.gitignore](./.gitignore)
- [docker-compose-dev.yml](./docker-compose-dev.yml)
- [docker-compose.yml](./docker-compose.yml)
- [README.md](./README.md)

---

- **libs**: Common libraries
- **mongodb**: Mongo database for docker.
- **stock_api**: Backend Restful endpoint api.
- **stock_manager**: Processing stock data.
- **docker-compose-dev.yml**: YAML file for docker compose only for development purpose.
- **docker-compose.yml**: YAML file for docker compose only for production purpose.
- **README.md**: Documentation.

## mongodb directory

This database is only for store configurations such as size of window to be used for machine learning to learn to make stock prediction. Store symbol of which stock will be processed.

- [Dockerfile](./mongodb/Dockerfile)
- [init_rs.sh](./mongodb/init_rs.sh)
- [init_stock_config.js](./mongodb/init_stock_config.js)

---

- **Dockerfile**: To build mongodb docker service on top of [mongo docker image](https://hub.docker.com/_/mongo). Doing so is because we want to create a collection with configuration files in database when container started.
  In addition we need to setup [replica set](https://www.mongodb.com/docs/manual/replication/).
- **init_rs.sh**: Bash shell for configure mongodb [replica set](https://www.mongodb.com/docs/manual/replication/).
- **init_stock_config.js**: This javascript file will be used and called when mongodb started. And is where we write script to create a collection with files. [How is this work?](https://hub.docker.com/_/mongo) look at section **Initializing a fresh instance**.

## stock_api directory

This is source code of backend Restful API, which act as interface between frontend and backend database. The framework for backend Restful API is [FastAPI](https://fastapi.tiangolo.com/). Furthermore the server is running on [Uvicorn](https://www.uvicorn.org/).

- [Dockerfile](.\stock_api\Dockerfile)
- [main.py](.\stock_api\main.py)
- [requirements.txt](.\stock_api\requirements.txt)
- [run.sh](.\stock_api\run.sh)

---

- **Dockerfile**: Dockerfile that is base on [Python image](https://hub.docker.com/_/python).
- **main.py**: Restful API.
- **requirements.txt**: Python pip requirement.txt.
- **run.sh**: Bash shell for starting backend Restful API.

## stock_manager directory

The heart of project and source code of stock's data processing. It download stock data from Yahoo financial the processing those data and make prediction for 1 day in future for the stock.

- [Dockerfile](.\stock_manager\Dockerfile)
- [run.sh](.\stock_manager\run.sh)
- [stock_config_listener.py](.\stock_manager\stock_config_listener.py)
- [stock_cronjob.cron](.\stock_manager\stock_cronjob.cron)
- [stock_processor.py](.\stock_manager\stock_processor.py)

---

- **Dockerfile**: Dockerfile that is base on [Python image](https://hub.docker.com/_/python).
- **run.sh**: Bash shell to schedule and run cronjob.
- **stock_config_listener.py**: A listener who listen to mongo database changed event then run **stock_processor.py**. This file listen to confiuration file changed in mongo database constantly.
- **stock_cronjob**: A file define the cronjob to be scheduled for linux.
- **stock_processor.py**: Main script to process downloaded stock data and use machine learning to learn and make prediction. Finally to write stock and prediction data into database.
