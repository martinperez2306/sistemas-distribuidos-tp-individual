FROM middlewaresys_client

# Install Ingestion Service
RUN mkdir -p /root/ingestion_service
WORKDIR /root
COPY . ./ingestion_service/
CMD ["python3", "-m", "ingestion_service"]