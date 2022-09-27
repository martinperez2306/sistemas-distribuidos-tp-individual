FROM python-rabbitmq

# Install Commons
RUN mkdir -p /root/dependencies/commons
WORKDIR /root/dependencies/commons
COPY . .