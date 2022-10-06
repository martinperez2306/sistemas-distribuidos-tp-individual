FROM python-rabbitmq

# Install Commons
RUN pip3 install requests
RUN mkdir -p /root/dependencies/commons
WORKDIR /root/dependencies/commons
COPY . .