FROM python-rabbitmq

COPY middleware.py /root/middleware.py
WORKDIR /root/
ENTRYPOINT ["python3", "/root/middleware.py"]