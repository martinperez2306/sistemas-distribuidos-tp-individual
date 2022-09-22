FROM python-rabbitmq

COPY client.py /root/client.py
ENTRYPOINT ["python3", "/root/client.py"]