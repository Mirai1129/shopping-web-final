# What is this project?

My school database final project.

## How to run this project?

This project rely on Docker or you can just use [environment](##Environment)

1. Download [Docker](https://www.docker.com/products/docker-desktop/).
2. Run the docker command in your terminal.

```bash
docker-compose up --build
```

## Environment

If you don't want to use the docker.

- `.env` file

  ```env
    HOST="host ip address"
    USER="your user name"
    PASSWORD="your password"
    DATABASE="your databse name"
    CHARSET='utf8mb4'
  ```

- Python package
  - requests==2.31.0
  - flask==3.0.0
  - pymysql==1.1.0
  - python-dotenv==0.13.0
  - cryptography==3.4.7
- [MySQL database](./database/shoppingweb.sql)

## How to run the project

```bash
python run.py
```
