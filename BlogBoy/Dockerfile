FROM python:3.5

#update
RUN apt-get update

#install requirements
COPY ./requirements.txt /tmp/requirements.txt
WORKDIR /tmp
RUN pip3 install -r requirements.txt

#copy app
COPY . /BlogBoy
WORKDIR /

CMD ["python", "BlogBoy/manage.py", "gunicorn"]
