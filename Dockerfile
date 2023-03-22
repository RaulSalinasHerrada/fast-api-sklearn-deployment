FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app/.

RUN python generate_apikey.py