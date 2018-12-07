FROM python:3.6

RUN pip3 install python-etcd requests

RUN mkdir -p /discovery

COPY app /app

CMD ["python3", "/app/main.py"]
