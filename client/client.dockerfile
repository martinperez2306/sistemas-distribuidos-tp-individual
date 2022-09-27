FROM middleware_client

# Install Client
RUN mkdir -p /root/client
RUN mkdir -p /root/client/videos
WORKDIR /root
COPY . ./client/
CMD ["python3", "-m", "client"]