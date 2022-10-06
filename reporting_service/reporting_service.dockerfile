FROM middlewaresys_client

# Install Reporting Service
RUN mkdir -p /root/reporting_service
RUN mkdir -p /root/reporting_service/thumbnails
WORKDIR /root
COPY . ./reporting_service/
CMD ["python3", "-m", "reporting_service"]