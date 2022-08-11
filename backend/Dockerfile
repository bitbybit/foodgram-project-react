FROM python:3.9

RUN mkdir /app
RUN mkdir /app/data

COPY ./backend/ /app
COPY ./data/ /app/data

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r /app/requirements.txt --no-cache-dir

WORKDIR /app

CMD ["/bin/sh", "/app/run.sh"]
