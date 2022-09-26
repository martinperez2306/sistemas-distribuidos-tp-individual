FROM middlewaresys_client

# Install Ingestion Service
RUN mkdir -p /root/ingestion_service
WORKDIR /root/ingestion_service
COPY . .
RUN mv /root/middlewaresys_client /root/ingestion_service/src/middlewaresys_client
ENTRYPOINT ["python3", "/root/ingestion_service/src/main.py"]