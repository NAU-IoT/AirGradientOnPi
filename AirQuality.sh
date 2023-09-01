#!/bin/bash

python3 /AirQuality.py >> /Data/logs/AirQuality-`date '+%Y%m%d'`.log 2>&1
