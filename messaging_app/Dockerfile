#using this base image
FROM python:3.10 

COPY . /messaging_app/

WORKDIR /messaging_app

#update the image and  install python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip

#install all the needed dependencies
RUN pip install -r requirements.txt

#expose this port for use  in the django app
EXPOSE 8000

CMD ["python3", "manage.py", "runserver"]