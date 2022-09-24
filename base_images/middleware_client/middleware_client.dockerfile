FROM python-rabbitmq

# Install Middleware client library
RUN mkdir -p /root/middleware_client
WORKDIR /root/middleware_client
COPY . .