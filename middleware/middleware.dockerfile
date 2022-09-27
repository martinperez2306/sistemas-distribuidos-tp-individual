FROM commons

# Install Middleware
RUN mkdir -p /root/middleware
WORKDIR /root
COPY . ./middleware/
CMD ["python3", "-m", "middleware"]