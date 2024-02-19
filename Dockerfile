# RUN Docker 
# docker build -t pp_backend . && docker run --publish 80:80 pp_backend
FROM python:3.11

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./routes /code/routes
COPY ./models /code/models
COPY ./API.py /code/API.py

EXPOSE 80

# 
#CMD ["uvicorn", "API:app", "--host", "127.0.0.1", "--port", "8080"]
#CMD [ "python","-m", "uvicorn", "API:app", "--host", "localhost", "--port", "8080", "--reload"]
CMD ["uvicorn", "API:app", "--host=0.0.0.0", "--port=80"]

