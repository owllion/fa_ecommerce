# FROM python:3.9

# WORKDIR /app

# COPY ./requirements.txt /requirements.txt

# RUN python -m venv /py\
#     && pip install --upgrade pip\ 
#     && pip install --no-cache-dir --upgrade -r /requirements.txt

# # this is what changes most frequently, we put it near the end
# COPY ./app /app

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]




# 
FROM python:3.10

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

EXPOSE 8080
# 
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload" ]
# CMD ["uvicorn", "app.main:app","--host", "0.0.0.0", "--reload", "--port", "8025"]
