FROM middlewaresys_client

# Install Like Filter
RUN mkdir -p /root/trending_filter
WORKDIR /root
COPY . ./trending_filter/
CMD ["python3", "-m", "trending_filter"]