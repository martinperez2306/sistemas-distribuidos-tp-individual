FROM middleware_client

# Install Client
RUN mkdir -p /root/client
WORKDIR /root/client
COPY . .
RUN mv /root/middleware_client /root/client/middleware_client
ENTRYPOINT ["python3", "/root/client/main.py"]