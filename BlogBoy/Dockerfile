FROM python:3.5

#update
RUN apt-get update

COPY ./Config/blogboy_supervisor.conf /etc/supervisor/conf.d/
#install requirements
COPY ./requirements.txt /tmp/requirements.txt

WORKDIR /tmp
RUN pip3 install -r requirements.txt

#copy app
COPY . /BlogBoy
WORKDIR /BlogBoy

CMD ["sudo", "supervisorctl", "restart", "app"]
