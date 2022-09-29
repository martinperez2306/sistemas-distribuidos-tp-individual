FROM middlewaresys_client

# Install Day Grouper
RUN mkdir -p /root/day_grouper
WORKDIR /root
COPY . ./day_grouper/
CMD ["python3", "-m", "day_grouper"]