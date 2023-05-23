
# FROM python:3.10

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD exec uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload 




