#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
sys.path.append(r'./lib')

import Adafruit_DHT
import datetime
import epd2in13bc
import epdconfig
import time
import locale
from PIL import Image,ImageDraw,ImageFont
import traceback

pin = 22

# Drawing on the image
font64 = ImageFont.truetype('./lib/Font.ttc', 64)
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

	epd = epd2in13bc.EPD()
        epd.init()
	#epd.reset()
        #epd.Clear()
        time.sleep(1)
    
        print("Displaying temperature and humidity") 
        HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
        HRYimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126  ryimage: red or yellow image  
        drawblack = ImageDraw.Draw(HBlackimage)
        drawry = ImageDraw.Draw(HRYimage)
        if humidity is not None and temperature is not None:
    	    drawblack.text((20,-10),'{0:0.1f}C'.format(temperature), font = font64, fill = 0)
    	    drawblack.text((20,40),'{0:0.1f}%'.format(humidity), font = font64, fill = 0)
	    drawblack.text((0, 94), datetime.datetime.now().strftime("%H:%M"), font = font9, fill = 0)
	
        #drawblack.text((10, 0), 'hello world', font = font20, fill = 0)
        #drawblack.text((10, 20), '2.13inch e-Paper bc', font = font20, fill = 0)
        
        #drawblack.line((20, 50, 70, 100), fill = 0)
        #drawblack.line((70, 50, 20, 100), fill = 0)
        #drawblack.rectangle((20, 50, 70, 100), outline = 0)    
	
        #drawry.line((165, 50, 165, 100), fill = 0)
        #drawry.line((140, 75, 190, 75), fill = 0)
        #drawry.arc((140, 50, 190, 100), 0, 360, fill = 0)
	
        #drawry.rectangle((80, 50, 130, 100), fill = 0)
        #drawry.chord((85, 55, 125, 95), 0, 360, fill =1)
        epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
        #time.sleep(1)
	
        #print("3.read bmp file")
        #HBlackimage = Image.open('../pic/2in13bc-b.bmp')
        #HRYimage = Image.open('../pic/2in13bc-ry.bmp')
        #epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
        #time.sleep(2)
	
        #print("Clear...")
        #epd.init()
        #epd.Clear()
	
        epd.sleep()
	break
except IOError as e:
    print(e)
    
except KeyboardInterrupt:    
    print("ctrl + c:")
    epdconfig.module_exit()
    exit()



