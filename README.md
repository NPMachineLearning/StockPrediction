[TOC]

# Stock Prediction

The purpose of this project is to grab Yahoo's financial stocks' data and then use meachine learning to make prediction for stocks. Store stock data and prediction in database.

The project is docker based and each services are containerized.

# Note

**Instruction are using forward slash(\/). However in window command line need to be replaced with backward slash(\\)**

# Run on local machine

## Setup environment

1. Make your have python installed.
2. Install [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).
3. Create an environment [see here](https://virtualenv.pypa.io/en/latest/user_guide.html). For example `virtualenv .venv`.
4. Activate environment [see here](https://virtualenv.pypa.io/en/latest/user_guide.html). For example in Powershell `./.venv/scripts/activate`.
5. Install packages with command `pip install -r ./app/requirements.txt`

## Run docker services

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

## Run web app

The project provide a web app for end user as a demo.

To run demo:

1. Run command `streamlit run ./app/app.py`.
2. Go to `http://http://localhost:8501`.

## Note

### To change mysql password

Go to `.env` file at `./.env`

- Change password for **MYSQL_DB_PASSWORD**

### To change mongodb user and password

Go to `.env` file at `./.env`

#### mongodb

- Change user for **MONGO_DB_USER**
- Change password for **MONGO_DB_PASSWORD**

#### mongo-express(UI)

- Change user for **MONGO_EXPRESS_USER**
- Change password for **MONGO_EXPRESS_PASSWORD**

### For local development

Docker container might use libraries from `./docker/libs` and libraries use defined setting for connecting database. Values in setting are defined in `.env` file located at `./docker/libs/.env`

# Development on local machine

This will **only** start database related services. Therefore we can write, debug or test code in local machine.

**Note**: Make sure to change value to **localhost** for **_MYSQL_HOST_** and **_MONGO_HOST_** in `.env` file located in `./docker/libs/.env`

1. Install packages from **_requirements.txt_**
   - `pip install -r ./app/requirements.txt`
   - `pip install -r ./docker/libs/requirements.txt`
   - `pip install -r ./docker/stock_api/requirements.txt`
2. Go through steps 1 ~ 7 for **Run on local machine**.
3. Run command `docker-compose -f docker-compose-dev.yml up -d --build` for detach mode or `docker-compose -f docker-compose-dev.yml up --build` for none detach mode.
4. At this point your are able to write code, debug, test and connect to database.
5. To shutdown services `docker-compose -f docker-compose-dev.yml down`.

# Architecture

![image](https://images.unsplash.com/photo-1706947329131-1aa452641f74?q=80&w=2017&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D)

## All docker containers/services

Number of containers/services will start when docker-compose is up.

- [**mysql database**](https://hub.docker.com/_/mysql): For storing stock and prediction data.
- [**admine**](https://hub.docker.com/_/adminer): User interface for mysql database.
- [**mongo database**](https://hub.docker.com/_/mongo): NoSQL database for storing configuration values.
- [**mongo-express**](https://hub.docker.com/_/mongo-express): User interface for monogo database.
- **stock_api**: Backend Restful endpoint api.
- **stock_manager**: Processing stock data and listen for configuration file updated.

## Database (Docker container)

Two database is used for the project [MySQL](https://www.mysql.com/) and [MongoDB](https://www.mongodb.com/). MySQL(table like) database is used for storing stock and prediction data. In contrast MongoDB(JSON like) is used for storing configuration data which will be used during stock's data processing.

## Database admin tool (Docker container)

In order to manage database visually, the project employed [**admine**](https://hub.docker.com/_/adminer) for **MySQL** and [**mongo-express**](https://hub.docker.com/_/mongo-express) for **MongoDB**.

## Stock API (Docker container)

Main purpose is to provide endpoint restful API. Therefore any clients can use this endpoint API.

Framework use [FastAPI](https://fastapi.tiangolo.com/).

The API provide stock data and configuration.
The backend api service running at port 8002 by default.

To consume api `http://localhost:8002`.
To see how to use api or what api is avaliable `http://locahost:8002/docs`.

## Stock Manager (Docker container)

Main purpose is to **processing stock data**, **train model from stock data**, **make stock prediction**, **write data into database**.

In addition, entire procedure is scheduled to be run everyday with cornjob.

Whenever configuration/setting updated then entire procedure will run again in order to achieve up to date stock data.

## Web app (Not docker container)

This is not part of docker container service. This is a demo for how to use **Stock API**.

# Project structure

## Root directory

- [app/](./app)
- [docker/](./docker)
  - [libs/](./docker/libs)
  - [mongodb/](./docker/mongodb)
  - [stock_api/](./docker/stock_api)
  - [stock_manager/](./docker/stock_manager)
- [.gitignore](./.gitignore)
- [docker-compose-dev.yml](./docker-compose-dev.yml)
- [docker-compose.yml](./docker-compose.yml)
- [README.md](./README.md)

---

- **app**: Frontend web app
- **libs**: Common libraries
- **mongodb**: Docker container for Mongo database.
- **stock_api**: Docker container for backend Restful endpoint api.
- **stock_manager**: Docker container for processing stock data.
- **docker-compose-dev.yml**: YAML file for docker compose only for development purpose.
- **docker-compose.yml**: YAML file for docker compose only for production purpose.
- **README.md**: Documentation.

## app directory

- [pages/](./app/pages)
  - [config.py](./app/pages/config.py)
- [api.py](./app/api.py)
- [app.py](./app/app.py)
- [requirements.txt](./app/requirements.txt)

---

**config.py**: Web page to manage stock such as add a new stock, remove a stock.
**api.py**: An utility for frontend web app to communicate with backend restful api service.
**app.py**: Main frontend web app/main page.
**requirements.txt**: python pip requirements.txt.

## libs directory

A set of handful libraries to be used by docker services such as **stock_api**, **stock_mananger**. Libraries need to connect to database in order to work. Therefore `.env` file is where it defiend all setting.

## mongodb directory

This database is only for store configurations such as size of window to be used for machine learning to learn to make stock prediction. Store symbol of which stock will be processed.

- [Dockerfile](./docker/mongodb/Dockerfile)
- [init_rs.sh](./docker/mongodb/init_rs.sh)
- [init_stock_config.js](./docker/mongodb/init_stock_config.js)

---

- **Dockerfile**: To build mongodb docker service on top of [mongo docker image](https://hub.docker.com/_/mongo). Doing so is because we want to create a collection with configuration files in database when container started.
  In addition we need to setup [replica set](https://www.mongodb.com/docs/manual/replication/).
- **init_rs.sh**: Bash shell for configure mongodb [replica set](https://www.mongodb.com/docs/manual/replication/).
- **init_stock_config.js**: This javascript file will be used and called when mongodb started. And is where we write script to create a collection with files. [How is this work?](https://hub.docker.com/_/mongo) look at section **Initializing a fresh instance**.

## stock_api directory

This is source code of backend Restful API, which act as interface between frontend and backend database. The framework for backend Restful API is [FastAPI](https://fastapi.tiangolo.com/). Furthermore the server is running on [Uvicorn](https://www.uvicorn.org/).

- [Dockerfile](./docker/stock_api/Dockerfile)
- [main.py](./docker/stock_api/main.py)
- [requirements.txt](./docker/stock_api/requirements.txt)
- [run.sh](./docker/stock_api/run.sh)

---

- **Dockerfile**: Dockerfile that is base on [Python image](https://hub.docker.com/_/python).
- **main.py**: Restful API.
- **requirements.txt**: Python pip requirement.txt.
- **run.sh**: Bash shell for starting backend Restful API.

## stock_manager directory

The heart of project and source code of stock's data processing. It download stock data from Yahoo financial the processing those data and make prediction for 1 day in future for the stock.

- [Dockerfile](./docker/stock_manager/Dockerfile)
- [run.sh](./docker/stock_manager/run.sh)
- [stock_config_listener.py](./docker/stock_manager/stock_config_listener.py)
- [stock_cronjob.cron](./docker/stock_manager/stock_cronjob.cron)
- [stock_processor.py](./docker/stock_manager/stock_processor.py)

---

- **Dockerfile**: Dockerfile that is base on [Python image](https://hub.docker.com/_/python).
- **run.sh**: Bash shell to schedule and run cronjob.
- **stock_config_listener.py**: A listener who listen to mongo database changed event then run **stock_processor.py**. This file listen to confiuration file changed in mongo database constantly.
- **stock_cronjob**: A file define the cronjob to be scheduled for linux.
- **stock_processor.py**: Main script to process downloaded stock data and use machine learning to learn and make prediction. Finally to write stock and prediction data into database.
