# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./* /code/

# 
CMD ["uvicorn", "API.py:app", "--host", "0.0.0.0", "--port", "80"]