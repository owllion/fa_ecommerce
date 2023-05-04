FROM tiangolo/uvicorn-gunicorn:python3.10

WORKDIR /app

COPY ./requirements.txt /requirements.txt

RUN python -m venv /py\ 
    && pip install --no-cache-dir --upgrade -r /requirements.txt

# this is what changes most frequently, we put it near the end
COPY ./app /app


CMD ["uvicorn", "app.main:app", "--reload", "--port", "443", "--ssl-keyfile", "app/cert/key.pem", "--ssl-certfile", "app/cert/cert.pem"]




