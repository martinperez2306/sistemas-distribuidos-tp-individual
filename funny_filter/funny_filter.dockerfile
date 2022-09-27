FROM middlewaresys_client

# Install Like Filter
RUN mkdir -p /root/funny_filter
WORKDIR /root
COPY . ./funny_filter/
CMD ["python3", "-m", "funny_filter"]