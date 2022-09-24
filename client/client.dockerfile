FROM middleware_client

# Install Client
COPY client.py /root/client.py
WORKDIR /root/
ENTRYPOINT ["python3", "/root/client.py"]