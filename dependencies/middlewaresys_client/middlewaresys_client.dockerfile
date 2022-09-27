FROM commons

# Install Middleware System client library
RUN mkdir -p /root/middlewaresys_client
WORKDIR /root/middlewaresys_client
COPY . .