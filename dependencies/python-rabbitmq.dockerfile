FROM ubuntu:20.04

# Install Python with rabbit MQ library
RUN apt update && apt install python3 python3-pip -y
RUN pip3 install pika
RUN mkdir -p /root/dependencies