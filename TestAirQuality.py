import Adafruit_SSD1306
import time
import board
import busio
import adafruit_scd30
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def celsius_to_fahrenheit(celsius):
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit


# SCD-30 has tempremental I2C with clock stretching, datasheet recommends
# starting at 50KHz
i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
scd = adafruit_scd30.SCD30(i2c)

# Raspberry Pi pin configuration:
RST = 24

# Initialize OLED display
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C, i2c_bus=1)
disp.begin()
disp.clear()
disp.display()

# Load font
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)



while True:
    # since the measurement interval is long (2+ seconds) we check for new data before reading
    # the values, to ensure current readings.
    if scd.data_available:
        print("Data Available!")
        print("CO2: %d PPM" % scd.CO2)
        cTemp = scd.temperature
        fTemp = (cTemp * 9/5) + 32
        humidity = scd.relative_humidity
        print("Temperature in Fahrenheit : %.2f F" %fTemp)
        print("Relative Humidity : %.2f %%RH" %humidity)
        print("")
        print("Waiting for new data...")
        print("")

    # Create image buffer
    image = Image.new('1', (disp.width, disp.height))
    draw = ImageDraw.Draw(image)

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
    disp.clear()
    disp.image(image)
    disp.display()
        
    time.sleep(2)

