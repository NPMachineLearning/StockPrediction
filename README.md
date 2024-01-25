# Stock Prediction

The purpose of this project is to grab Yahoo's financial stocks' data and then use meachine learning to make prediction for stocks. Store stock data and prediction in database.

The project is docker based and each services are containerized.

# How to start service

1. Make sure docker is installed.
2. Open terminal and go to project root directory.
3. Run command `docker-compose up -d` for dettach mode or `docker-compose up` for none dettach mode.
4. Run command `docker-compose down` if in dettach mode or **control key + C** to exit in none dettach mode.

# Docker services

Number of services will start when docker-compose is up.

- [mysql database](https://hub.docker.com/_/mysql): For storing stock and prediction data.
- [admine](https://hub.docker.com/_/adminer): User interface for mysql database.
- [mongo database](https://hub.docker.com/_/mongo): NoSQL database for storing configuration values.
- [mongo-express](https://hub.docker.com/_/mongo-express): User interface for monogo database.
- stock_manager: Custom service for processing stock'data and make prediction. In addition to store data into database. This service is running in schedule with cronjob.

# File structure

## Root directory

- [mongodb/](.\stock_predictions\mongodb)
- [secrets/](.\stock_predictions\secrets)
- [stocks/](.\stock_predictions\stocks)
- [.env](.\stock_predictions.env)
- [.gitignore](.\stock_predictions.gitignore)
- [docker-compose.yml](.\stock_predictions\docker-compose.yml)
- [ReadMe.md](.\stock_predictions\ReadMe.md)

* **stock_predictions/**: The project root.
* **mongodb**: Mongo database for docker.
* **secrets**: Not in github but [here(private)](https://drive.google.com/drive/folders/16ypKrONqN92Ub2SW16mLsxj5S7-AXb74?usp=drive_link). Contain all docker secrets such as root user or password senstive information.
* **stocks**: A docker service for processing stock data with cronjob.
* **.env**: Environment variables for docker.
* **docker-compose.yml**: YAML file for docker compose.

## mongodb directory

This database is only for store configurations such as size of window to be used for machine learning to learn to make stock prediction. Store symbol of which stock will be processed.

- [Dockerfile](.\mongodb\Dockerfile)
- [init_stock_config.js](.\mongodb\init_stock_config.js)

* **Dockerfile**: To build mongodb docker service on top of [mongo docker image](https://hub.docker.com/_/mongo). Doing so is because we want to create a collection with configuration files in database when container started.
* **init_stock_config.js**: This javascript file will be used and called when mongodb started. And is where we write script to create a collection with files. [How is this work?](https://hub.docker.com/_/mongo) look at section **Initializing a fresh instance**.

## stocks directory

This is a scheduled service that will run by itself in interval. The main purpose of this service is to download required stock data from Yahoo financial and make stock prediction. In addtion to store data into database.

- [utils/](.\stocks\utils)
  - [db_env_utils.py](.\stocks\utils\db_env_utils.py)
  - [mongo_utils.py](.\stocks\utils\mongo_utils.py)
  - [mysql_utils.py](.\stocks\utils\mysql_utils.py)
  - [stock_utils.py](.\stocks\utils\stock_utils.py)
  - [utils.py](.\stocks\utils\utils.py)
  - [\_\_init\_\_.py](.\stocks\utils__init__.py)
- [.env](.\stocks.env)
- [Dockerfile](.\stocks\Dockerfile)
- [requirements.txt](.\stocks\requirements.txt)
- [run.sh](.\stocks\run.sh)
- [stock_cronjob](.\stocks\stock_cronjob)
- [stock_processor.py](.\stocks\stock_processor.py)

* **Utils**: Folder contain all helper functions that will be used in **stock_processor.py**.
* **.env**: Environment variables that will be used for connecting to database.
* **Dockerfile**: Customzied docker service that build on top of [Python image](https://hub.docker.com/_/python).
* **requirements.txt**: File that pip will use to install required python modules.
* **run.sh**: Bash shell to schedule cronjob, run cronjob at foreground and run **stock_processor.py** once.
* **stock_cronjob**: Base on linux cronjob. A file define the cronjob to be scheduled.
* **stock_processor.py**: Main script to process downloaded stock data and use machine learning to learn data then make prediction. Finally to write stock and prediction data into database.
