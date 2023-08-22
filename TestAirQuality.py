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


def celsius_to_fahrenheit(celsius):
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit


def scd30_initialization():
    # SCD-30 has tempremental I2C with clock stretching, datasheet recommends
    # starting at 50KHz
    i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
    scd = adafruit_scd30.SCD30(i2c)
    # Raspberry Pi pin configuration:
    RST = 24


def oled_initialization():
    # Initialize OLED display
    disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C, i2c_bus=1)
    disp.begin()
    disp.clear()
    disp.display()
    # Load font
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)


def pmsensor_initialization():
    # Define the serial port and baud rate
    serial_port = "/dev/ttyS0"
    baud_rate = 9600
    # Initialize the serial connection
    uart = serial.Serial(serial_port, baudrate=baud_rate, timeout=0.25)
    # Initialize the PM2.5 sensor over UART
    pm25 = PM25_UART(uart)

def create_image_buffer(disp_width, disp_height):
    # Create image buffer
    image = Image.new('1', (disp_width, disp_height))
    draw = ImageDraw.Draw(image)
    return image, draw


def main():
    scd30_initialization()

    oled_initialization()

    pmsensor_initialization()


    while True:
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

        # Create image buffer
        image, draw = create_image_buffer(disp.width, disp.height)

    # Assign values to variables
    temp = "Temp: "
    tempval = ("%.2f F" %fTemp)
    hum = "Humidity: "
    humval = ("%.2f %%RH" %humidity)
    co2 = "CO2: "
    co2val = ("%.2f PPM" %co2ppm)

    # Prepare temp and hum for display
    draw.text((32, 15), temp, font=font, fill=255)
    draw.text((32, 25), tempval, font=font, fill=255)
    draw.text((32, 40), hum, font=font, fill=255)
    draw.text((32, 50), humval, font=font, fill=255)
        
    # Display temp and humidity
    disp.clear()
    disp.image(image)
    disp.display()
        
    time.sleep(5)


    # Prepare co2 for display
    # Create image buffer
    image = Image.new('1', (disp.width, disp.height))
    draw = ImageDraw.Draw(image)
    draw.text((32, 15), co2, font=font, fill=255)
    draw.text((32, 25), co2val, font=font, fill=255)

    # Display co2 value
    disp.clear()
    disp.image(image)
    disp.display()
        
    time.sleep(5)

    
    try:
        aqdata = pm25.read()
    except RuntimeError as e:
        print("Error reading from sensor:", e)
        print("Retrying...")
        continue


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
    
    # Prepare pm1.0 value for display
    # Create image buffer
    image = Image.new('1', (disp.width, disp.height))
    draw = ImageDraw.Draw(image)
    draw.text((32, 15), pm10, font=font, fill=255)
    draw.text((32, 25), pm10val, font=font, fill=255)
       
    # Display pm1.0 value
    disp.clear()
    disp.image(image)
    disp.display()
        
    time.sleep(5)

    # Prepare pm2.5 value for display
    # Create image buffer
    image = Image.new('1', (disp.width, disp.height))
    draw = ImageDraw.Draw(image)
    draw.text((32, 15), pm25, font=font, fill=255)
    draw.text((32, 25), pm25val, font=font, fill=255)  
    # Display pm2.5 value
    disp.clear()
    disp.image(image)
    disp.display()
        
    time.sleep(5)


    # Prepare pm10.0 value for display
    # Create image buffer
    image = Image.new('1', (disp.width, disp.height))
    draw = ImageDraw.Draw(image)
    draw.text((32, 15), pm100, font=font, fill=255)
    draw.text((32, 25), pm100val, font=font, fill=255)
       
    # Display pm10.0 value
    disp.clear()
    disp.image(image)
    disp.display()
        
    time.sleep(5)
