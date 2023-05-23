
# FROM python:3.10

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

ENV PORT 8080
CMD exec uvicorn app.main:app --host 0.0.0.0 --port $PORT --env-file app/.env.prod --reload 

# Step 4: Run the web service on container startup using gunicorn webserver.
# CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 main:app




