FROM python:3.10

WORKDIR /app

RUN apt-get update

COPY ./requirements.txt /app/requirements.txt


RUN pip install -r requirements.txt

RUN apt-get install -y supervisor

COPY . /app
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENTRYPOINT ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

# ENTRYPOINT [ "python" ]

# CMD [ "src/main.py" ]