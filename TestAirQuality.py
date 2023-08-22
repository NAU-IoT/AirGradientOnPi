import Adafruit_SSD1306
import time
import board
import busio
import adafruit_scd30
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import serial
from adafruit_pm25.uart import PM25_UART
import sys

def celsius_to_fahrenheit(celsius):
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit


def scd30_initialization():
    # SCD-30 has tempremental I2C with clock stretching, datasheet recommends
    # starting at 50KHz
    i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
    scd = adafruit_scd30.SCD30(i2c)
    return scd


def oled_initialization():
    # Raspberry Pi pin configuration:
    RST = 24
    # Initialize OLED display
    disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C, i2c_bus=1)
    disp.begin()
    disp.clear()
    disp.display()
    # Load font
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)
    return disp


def pmsensor_initialization():
    # Define the serial port and baud rate
    serial_port = "/dev/ttyS0"
    baud_rate = 9600
    # Initialize the serial connection
    uart = serial.Serial(serial_port, baudrate=baud_rate, timeout=0.25)
    # Initialize the PM2.5 sensor over UART
    pm25 = PM25_UART(uart)
    return pm25


def create_image_buffer(disp_width, disp_height):
    # Create image buffer
    image = Image.new('1', (disp_width, disp_height))
    draw = ImageDraw.Draw(image)
    return image, draw


def display_values(disp, image):
    disp.clear()
    disp.image(image)
    disp.display()


def display_sensor_values(disp, variables):
    # Create image buffer
    image, draw = create_image_buffer(disp.width, disp.height)
    y_coord = 15
    for item in variables:
        draw.text((32, y_coord), item, font=font, fill=255)
        y_coord += 10
    display_values(disp, image)
    time.sleep(5)


def read_scd(scd):
    if scd.data_available:
        #print("Data Available!")
        #print("CO2: %d PPM" % scd.CO2)
        cTemp = scd.temperature
        fTemp = (cTemp * 9/5) + 32
        co2ppm = scd.CO2
        humidity = scd.relative_humidity
        #print("Temperature in Fahrenheit : %.2f F" %fTemp)
        #print("Relative Humidity : %.2f %%RH" %humidity)
        #print("")
        #print("Waiting for new data...")
        #print("")
    # Assign values to variables
    temp = "Temp: "
    tempval = ("%.2f F" %fTemp)
    hum = "Humidity: "
    humval = ("%.2f %%RH" %humidity)
    co2 = "CO2: "
    co2val = ("%.2f PPM" %co2ppm)
    return temp, tempval, hum, humval, co2, co2val


def read_pm25(pm25):
    try:
        aqdata = pm25.read()
    except RuntimeError as e:
        print("Error reading from sensor:", e)
        sys.exit()

    # Assign standard particle data to variables
    pm10 = "PM1.0: "
    pm10val = ("%.2f ug/m^3" %aqdata["pm10 standard"])
    pm25 = "PM2.5: "
    pm25val = ("%.2f ug/m^3" %aqdata["pm25 standard"])
    pm100 = "PM10: "
    pm100val = ("%.2f ug/m^3" %aqdata["pm100 standard"])
    # Assign environmental particle data to variables
    #pm1 = "PM1.0: "
    #pm10val = (aqdata["pm10 env"]
    #pm25 = "PM2.5: "
    #pm25val = aqdata["pm25 env"]
    #pm10 = "PM10: "
    #pm100val = aqdata["pm100 env"]
    return pm10, pm10val, pm25, pm25val, pm100, pm100val


def main():
    scd = scd30_initialization()
    disp = oled_initialization()
    pm25 = pmsensor_initialization()

    while True:
        # Read data from scd30 sensor
        temp, tempval, hum, humval, co2, co2val = read_scd(scd)

        # Read data from pm2.5 sensor
        pm10, pm10val, pm25, pm25val, pm100, pm100val = read_pm25(pm25)

        # Display temp and humidity
        display_sensor_values(disp, {temp, tempval, hum, humval})

        # Display co2 value
        display_sensor_values(disp, {co2, co2val})

        # Display pm1.0 value
        display_sensor_values(disp, {pm10, pm10val})

        # Display pm2.5 value
        display_sensor_values(disp, {pm25, pm25val})

        # Display pm10.0 value
        display_sensor_values(disp, {pm100, pm100val})


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Script terminated by user")
        sys.exit()
