import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import smbus
import time

# Get I2C bus for SHT30
bus = smbus.SMBus(1)

# SHT30 address, 0x44(68)
    # Send measurement command, 0x2C(44)
    #           0x06(06)        High repeatability measurement
bus.write_i2c_block_data(0x44, 0x2C, [0x06])
time.sleep(0.5)
    # SHT30 address, 0x44(68)
    # Read data back from 0x00(00), 6 bytes
    # cTemp MSB, cTemp LSB, cTemp CRC, Humididty MSB, Humidity LSB, Humidity CRC
data = bus.read_i2c_block_data(0x44, 0x00, 6)
    # Calculate the data
cTemp = ((((data[0] * 256.0) + data[1]) * 175) / 65535.0) - 45
fTemp = cTemp * 1.8 + 32
humidity = 100 * (data[3] * 256 + data[4]) / 65535.0
    # Output data to screen
print("Relative Humidity : %.2f %%RH" %humidity)
    #print("Temperature in Celsius : %.2f C" %cTemp)
print("Temperature in Fahrenheit : %.2f F" %fTemp)


# Raspberry Pi pin configuration:
RST = 24

# Initialize OLED display
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C, i2c_bus=1)
disp.begin()
disp.clear()
disp.display()

# Create image buffer
image = Image.new('1', (disp.width, disp.height))
draw = ImageDraw.Draw(image)

# Load font
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)

# Display temperature and humidity on OLED
temp = "Temp: "
tempval = ("%.2f F" %fTemp)
hum = "Humidity: "
humval = ("%.2f %%RH" %humidity)

draw.text((32, 15), temp, font=font, fill=255)
draw.text((32, 25), tempval, font=font, fill=255)
draw.text((32, 40), hum, font=font, fill=255)
draw.text((32, 50), humval, font=font, fill=255)

# Show the image on the display
disp.image(image)
disp.display()

time.sleep(2)
