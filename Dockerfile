
# FROM python:3.10

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD exec uvicorn app.main:app --host 0.0.0.0 --env-file .env.prod --reload --port $PORT

# Step 4: Run the web service on container startup using gunicorn webserver.
# CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 main:app




