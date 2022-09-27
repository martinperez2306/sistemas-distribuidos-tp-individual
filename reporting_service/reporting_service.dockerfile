FROM middlewaresys_client

# Install Reporting Service
RUN mkdir -p /root/reporting_service
WORKDIR /root
COPY . ./reporting_service/
CMD ["python3", "-m", "reporting_service"]