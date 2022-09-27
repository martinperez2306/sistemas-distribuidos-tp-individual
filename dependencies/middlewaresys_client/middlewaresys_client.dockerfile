FROM commons

# Install Middleware System client library
RUN mkdir -p /root/dependencies/middlewaresys_client
WORKDIR /root/dependencies/middlewaresys_client
COPY . .