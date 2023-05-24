# fa_ecommerce - MERN Stack Shopping App Server
 
[![CI CD Pipeline](https://github.com/owllion/fa_ecommerce/actions/workflows/main.yml/badge.svg)](https://github.com/owllion/fa_ecommerce/actions/workflows/main.yml)
[![MIT licensed][shield-license]](#)

[shield-license]: https://img.shields.io/badge/license-MIT-blue.svg

A server for a shopping app powered by FastAPI and utilizes MySQL and Redis for efficient data storage and retrieval. Containerized with Docker for easy deployment and scalability. 
Deployed on GCP Cloud Run with CI/CD integration for automated build, packaging, and deployment

## Table of Contents
- [Table Diagram](#table-diagram)
- [Technologies](#technologies)
- [Features](#features)
- [Setup](#setup)
- [Project Status](#project-status)
- [License](#license)

## Table Diagram
![](https://res.cloudinary.com/azainseong/image/upload/v1684509215/3183D9FE-849C-4815-AACB-6A7089BCCAE4_nacgr5.jpg)
[see table relation in text](https://kaput-hose-1ba.notion.site/fastapi-ecommerce-project-Table-Relationships-bdd84cf011fd49f39fcbc1c57cf05326)

## Features
- redis/redisJson for cache
- aws lambda for server deployment
- aws RDS for db deployment
- docker for containerization
- pydantic for data verification

## Technologies

- fastapi - v0.95.0
- SQLAlchemy - v2.0.7
- mysql - v8.0.31
- redis-py - 4.5.5

## Setup
- Clone the project
```sh
#clone
git clone https://github.com/owllion/EC-Server.git
```

- Launch server
```sh
#http
uvicorn app.main:main --reload  
#https
uvicorn app.main:app --port 8000 --reload --ssl-keyfile app/cert/key.pem --ssl-certfile app/cert/cert.pem 
#production
uvicorn app.main:app --reload --env-file app/.env.prod 
```

- Or develop with docker-compose
```sh
#use local mysql db(dev)
docker-compose --build -d up 

#use cloud sql(prod)
docker-compose -f docker-compose.yml -f docker-compose.access.yml --env-file=.env.prod  up -d --build #production
```

## Project Status
Under Refactoring.

## License

This project is licensed under the terms of the MIT license.
Copyright &copy; 2023

