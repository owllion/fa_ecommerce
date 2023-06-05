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
![](https://res.cloudinary.com/azainseong/image/upload/v1685869487/298279DC-B989-4044-AA37-F39F13D3BE4B_ww57ca.jpg)
[see table relation in notion](https://www.notion.so/fastapi-ecommerce-project-Table-Relationships-bdd84cf011fd49f39fcbc1c57cf05326?pvs=4)

## Features
- 🛒 <strong>Shopping Functionality</strong>: <br>Browse (by category and search), add to cart, apply coupons, leave comments, add to favorites, and complete checkout.
- 👤 <strong>User Management</strong>: <br>Login, logout, register (email/Google/GitHub), password recovery, profile page (view and update personal information, upload profile picture, view order history, and manage coupons .etc).
- 🔐 <strong>Pydantic Data Verification</strong>: Ensure data integrity and validation using Pydantic.
- ![image](https://res.cloudinary.com/azainseong/image/upload/c_scale,w_24/v1685956731/LINE-Pay_h__W238_n_l7bbkk.png)  <strong>LINE Pay Integration</strong>: Integration with LINE Pay for seamless payment processing.
- <img width="24" height="24" src="https://img.icons8.com/color/48/redis.png" alt="redis"  /><strong>Cache Optimization</strong>: Improve website performance and response time by utilizing Redis for data caching.
- 🐳 <strong>Containerized Deployment</strong>: 
<br>Containerize the application using Docker for easy deployment, scalability, and management.
- ![image](https://res.cloudinary.com/azainseong/image/upload/c_scale,w_15/v1685957609/44036562_i2zm0p.png) <strong>CI/CD Integration</strong>:  <br>Automate the build, packaging, and deployment processes with GitHub Actions for continuous integration and deployment.
- <img width="24" height="24" src="https://img.icons8.com/color/48/google-cloud.png" alt="google-cloud"/> <strong>Deployment to Google Cloud Platform</strong>: Deploy the server to Cloud Run for efficient scaling and deployment. Manage the database using Cloud SQL.

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
Choose one of them to launch the service
- uvicorn
```sh
#http
uvicorn app.main:main --reload  
#https
uvicorn app.main:app --reload --env-file=app/localhost.env 
--ssl-keyfile app/cert/key.pem --ssl-certfile app/cert/cert.pem --port=443
#production
uvicorn app.main:app --reload --env-file app/.env.prod 
```

- docker-compose
```sh
#use local mysql (dev)
docker-compose up -d --build 

#use cloud sql (prod)
docker-compose -f docker-compose.yml -f docker-compose.access.yml --env-file=.env.prod  up -d --build
```
📙 docker-compose.access.yml
- This file is used to configure the necessary authentication(ADC) and access settings for connecting to Cloud SQL in a production environment. 
- Make sure to generate an IAM key from your service account, download it to your local machine, and update the ./gcp_key.json file path accordingly in the docker-compose.access.yml file, then mount it on your main service(in my case is 'app') volumes.

## Project Status
Under Refactoring.

## License

This project is licensed under the terms of the MIT license.

Copyright &copy; 2023
