FROM commons

# Install Middleware client library
RUN mkdir -p /root/dependencies/middleware_client
WORKDIR /root/dependencies/middleware_client
COPY . .