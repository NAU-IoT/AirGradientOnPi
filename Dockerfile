# syntax=docker/dockerfile:1

FROM ubuntu:22.04

# Update package list
RUN apt-get update

# Install apt dependencies
RUN apt-get install -y python3 python3-pip i2c-tools

# Install pip dependencies
RUN pip install adafruit-circuitpython-ssd1306 adafruit-circuitpython-scd30 Pillow adafruit-circuitpython-pm25

# Install timezone dependencies and establish docker container timezone
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install tzdata
ENV TZ=America/Phoenix
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Copy necessary files to local docker container environment
ADD TestAirQuality.py /TestAirQuality.py
ADD TestAirQuality.sh /TestAirQuality.sh

# Create necessary files and directories inside docker container
RUN mkdir -p /Data
RUN mkdir -p /Data/logs

# Establish correct permissions for files
RUN chmod +x /TestAirQuality.py
RUN chmod +x /TestAirQuality.sh

# Execute script
CMD ./TestAirQuality.sh \ 
    && bash
