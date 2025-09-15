FROM python:3.9.16

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements.txt ./
#RUN apt upgrade
RUN apt update -y
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY ./app ./

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]