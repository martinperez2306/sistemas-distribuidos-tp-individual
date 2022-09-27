FROM python-rabbitmq

# Install Commons
RUN mkdir -p /root/commons
WORKDIR /root/commons
COPY . .