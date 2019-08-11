#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
sys.path.append(r'./lib')

import Adafruit_DHT
import datetime
import epd2in13
import epdconfig
import time
import locale
from PIL import Image,ImageDraw,ImageFont
import traceback

pin = 22

# Drawing on the image
font64 = ImageFont.truetype('./lib/Font.ttc', 70)
font20 = ImageFont.truetype('./lib/Font.ttc', 20)
font18 = ImageFont.truetype('./lib/Font.ttc', 18)
font9 = ImageFont.truetype('./lib/Font.ttc', 9)

try:
    locale.setlocale(locale.LC_ALL, 'cs_CZ.utf8')
    print("WeatherPi by WarewolfCZ")
    
    while True:
        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, pin)
    
        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}°C  Humidity={1:0.1f}%'.format(temperature, humidity))
	    with open("/var/log/weatherdata.log", "a") as myfile:
		myfile.write('{0:s},{1:0.1f}°C,{2:0.1f}%\n'.format(datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"),temperature, humidity))
        else:
            print('Failed to get reading. Try again!')
            continue

	epd = epd2in13.EPD()
        epd.init(epd.lut_full_update)
	#epd.reset()
        #epd.Clear()
        time.sleep(1)
    
        print("Displaying temperature and humidity") 
        HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
        drawblack = ImageDraw.Draw(HBlackimage)
        if humidity is not None and temperature is not None:
    	    drawblack.text((30,-10),'{0:0.1f}C'.format(temperature), font = font64, fill = 0)
    	    drawblack.text((30,50),'{0:0.1f}%'.format(humidity), font = font64, fill = 0)
	    drawblack.text((2, 112), datetime.datetime.now().strftime("%H:%M"), font = font9, fill = 0)
        HBlackimage = HBlackimage.transpose(Image.ROTATE_180)
        epd.display(epd.getbuffer(HBlackimage))
	
        epd.sleep()
	break
except IOError as e:
    print(e)
    
except KeyboardInterrupt:    
    print("ctrl + c:")
    epdconfig.module_exit()
    exit()



