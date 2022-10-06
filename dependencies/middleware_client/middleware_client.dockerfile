FROM commons

# Install Middleware client library
RUN pip3 install Pillow
RUN mkdir -p /root/dependencies/middleware_client
WORKDIR /root/dependencies/middleware_client
COPY . .