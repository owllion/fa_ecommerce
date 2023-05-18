# fa_ecommerce - MERN Stack Shopping App Server
 
[![CI CD Pipeline](https://github.com/owllion/fa_ecommerce/actions/workflows/main.yml/badge.svg)](https://github.com/owllion/fa_ecommerce/actions/workflows/main.yml)

- A shopping app created with React.js , styled-components , TypeScript , Node.js , Typegoose and MongoDB.  

## Table of Contents

- [Technologies](#technologies)
- [Setup](#setup)
- [Project Status](#project-status)
- [License](#license)

## Technologies

- fastapi - v0.95.0
- SQLAlchemy - v2.0.7
- mysql - v8.0.31
- redis-py - 4.5.5

## Setup
- Clone
```
git clone https://github.com/owllion/EC-Server.git
```

- Server - local

```
uvicorn app.main:main --reload
```
 - Server - production
```
uvicorn app.main:main --reload --env-file app/.env.prod
```

- docker - local
```
docker-compose --build -d up
```

- docker - production
```
docker-compose -f docker-compose.prod.yml --env-file .env.prod --build -d up
```

## Project Status

Under Refactoring.

## License

This project is licensed under the terms of the MIT license

