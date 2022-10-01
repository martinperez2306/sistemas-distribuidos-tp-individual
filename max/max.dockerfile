FROM middlewaresys_client

# Install Day Grouper
RUN mkdir -p /root/max
WORKDIR /root
COPY . ./max/
CMD ["python3", "-m", "max"]