FROM middlewaresys_client

# Install Like Filter
RUN mkdir -p /root/like_filter
WORKDIR /root
COPY . ./like_filter/
CMD ["python3", "-m", "like_filter"]