# syntax=docker/dockerfile:1
FROM python:latest

# Update package list
RUN apt-get update

# Install apt dependencies
RUN apt-get install -y python3 python3-pip i2c-tools

# Install pip dependencies
RUN pip install Adafruit-SSD1306 adafruit-circuitpython-scd30 adafruit-circuitpython-pm25 RPi.GPIO pillow

# Install timezone dependencies and establish docker container timezone
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install tzdata
ENV TZ=America/Phoenix
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Copy necessary files to local docker container environment
ADD AirQuality.py /AirQuality.py
ADD AirQuality.sh /AirQuality.sh

# Create necessary files and directories inside docker container
RUN mkdir -p /Data
RUN mkdir -p /Data/logs

# Establish correct permissions for files
RUN chmod +x /AirQuality.py
RUN chmod +x /AirQuality.sh

# Execute script
CMD ./AirQuality.sh \
    && bash
