FROM middlewaresys_client

# Install Ingestion Service
RUN mkdir -p /root/like_filter
WORKDIR /root/like_filter
COPY . .
RUN mv /root/middlewaresys_client /root/like_filter/src/middlewaresys_client
ENTRYPOINT ["python3", "/root/like_filter/src/main.py"]