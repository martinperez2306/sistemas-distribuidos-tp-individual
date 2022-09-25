FROM python-rabbitmq

# Install Middleware
RUN mkdir -p /root/middleware
WORKDIR /root/middleware
COPY . .
ENTRYPOINT ["python3", "/root/middleware/src/main.py"]