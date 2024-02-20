# How to RUN Docker 
# MacOS / Linux
# docker build -t pp_backend . && docker run --publish 8000:8000 pp_backend
# Windows
# docker build -t pp_backend . ; docker run --publish 8000:8000 pp_backend
FROM python:3.11

# 
WORKDIR /code
ENV MONGO_DB_USERNAME=admin
ENV MONGO_DB_PWD=password

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./routes /code/routes
COPY ./models /code/models
COPY ./API.py /code/API.py
COPY ./Database /code/Database

EXPOSE 8000

CMD ["uvicorn", "API:app", "--host=0.0.0.0", "--port=8000"]

