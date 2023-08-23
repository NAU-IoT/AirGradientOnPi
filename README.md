# AirGradientOnPi
This repository is aimed at developing a functional DIY Air Quality sensor based on AirGradient: https://www.airgradient.com/open-airgradient/instructions/diy/ except using a Raspberry Pi Zero with python instead of a D1 Mini Pro with Arduino/C++


## List of Parts:

- [Raspberry Pi Zero](https://www.raspberrypi.com/products/raspberry-pi-zero/) - Microprocessor
- [SCD30](https://www.adafruit.com/product/4867?gclid=Cj0KCQjwuZGnBhD1ARIsACxbAVgve1OAQdD3gp0jqKSIYp_K2yrBMNbA2bwQP-ByRS27HUvg1xQobhAaAok0EALw_wcB) - Measures Temperature, Humidity, and CO2
- [OLED Display](https://www.wemos.cc/en/latest/d1_mini_shield/oled_0_66.html) - Displays Values
- [PMS5003](https://www.adafruit.com/product/3686) - Measures Particulate Matter Concentrations


## Dependencies
- Install Dependencies:
  - Install OLED Library:
    ```
    sudo pip install adafruit-circuitpython-ssd1306
    ```
  - Install SCD30 library:
    ```
    sudo pip install adafruit-circuitpython-scd30
    ```
  - Install Python Imaging Library:
    ```
    sudo pip install Pillow
    ```
  - Install PM25 Library:
    ```
    sudo pip install adafruit-circuitpython-pm25
    ```


## Wiring Diagram

  <img width="1134" alt="Screen Shot 2023-08-22 at 4 41 33 PM" src="https://github.com/NAU-IoT/AirGradientOnPi/assets/72172361/709a9a90-fb5a-48a6-914a-ca861066eecc">


## Running with Docker

  - Install docker:
  ```
  sudo apt install docker.io
  ```
  - Check if docker is functioning:
  ```
  sudo docker run hello-world
  ```
  - Clone repository to get Dockerfile and configuration files: 
  ```
  git clone https://github.com/NAU-IoT/AirGradientOnPi.git
  ```
  - Change into directory: 
  ```
  cd AirGradientOnPi
  ```
  - OPTIONAL: To change the docker containers time zone, edit line 16 in the Dockerfile. A list of acceptable time zones can be found at https://en.wikipedia.org/wiki/List_of_tz_database_time_zones 
  - Build docker image in AirGradientOnPi directory, this will take a while: 
  ```
  docker build -t airquality .
  ```
  - Create a directory in a convenient location to store the docker volume. For example: 
  ```
  mkdir -p Data/AirQuality
  ```
  - Create a volume to store data inside the directory created in the previous step:
  ```
  docker volume create --driver local \
    --opt type=none \
    --opt device=/SOME/LOCAL/DIRECTORY \
    --opt o=bind \
    YOUR_VOLUME_NAME
  ```
  - Execute docker container in AirGradientOnPi directory:
    - Note for IoT Team: Your_port_number could be 31883, container_port_number should be 31883
  ```
  docker run --privileged -v YOUR_VOLUME_NAME:/Data -p YOUR_PORT_NUMBER:CONTAINER_PORT_NUMBER -t -i -d --restart unless-stopped airquality
  ```
  - Verify container is running: 
  ```
  docker ps
  ```
  - Done!


## Running With Python

- Clone This Repository:
  ```
  git clone https://github.com/NAU-IoT/AirGradientOnPi.git
  ```
- Ensure I2C and UART are enabled:
  ```
  sudo raspi-config
  ```

   **Enabling I2C**:

    Navigate To Interface Options:
  
    <img width="748" alt="Screen Shot 2023-08-22 at 2 14 33 PM" src="https://github.com/NAU-IoT/AirGradientOnPi/assets/72172361/dba9b9a3-5dfc-4c9e-848a-588ef172b74a">

    Enter I2C Options:
  
    <img width="773" alt="Screen Shot 2023-08-22 at 2 15 12 PM" src="https://github.com/NAU-IoT/AirGradientOnPi/assets/72172361/f9a83f3a-b3aa-41d8-ba30-afa35921f7d6">

    Select Yes:
  
    <img width="745" alt="Screen Shot 2023-08-22 at 2 15 26 PM" src="https://github.com/NAU-IoT/AirGradientOnPi/assets/72172361/d8987231-6dd1-4ea3-b933-116d0113d91e">

    **Enabling UART**:
  
    Enter Serial Port Options Within Interface Option Menu:
  
    <img width="753" alt="Screen Shot 2023-08-22 at 2 20 14 PM" src="https://github.com/NAU-IoT/AirGradientOnPi/assets/72172361/7be1c950-9ff5-498c-939a-6a1c91bc15a7">

    Select No:
  
    <img width="680" alt="Screen Shot 2023-08-22 at 2 15 50 PM" src="https://github.com/NAU-IoT/AirGradientOnPi/assets/72172361/243db493-39fe-4334-8a81-b99c3fe6a9dd">

    Select Yes:

    <img width="664" alt="Screen Shot 2023-08-22 at 2 16 01 PM" src="https://github.com/NAU-IoT/AirGradientOnPi/assets/72172361/49b7a8b3-1923-4631-9604-d266c138997c">

    Select Finish:
  
    <img width="764" alt="Screen Shot 2023-08-22 at 2 16 17 PM" src="https://github.com/NAU-IoT/AirGradientOnPi/assets/72172361/9b341d64-a712-446a-8ae5-afa4c6184938">

- Change into directory:
  ```
  cd AirGradientOnPi
  ```

- Execute script:
  ```
  sudo python3 AirQuality.py
  ```

- Done!





  
