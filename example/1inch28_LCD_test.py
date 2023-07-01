#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import time
import logging
import spidev as SPI
from lib2_library.lib2 import LCD_1inch28
sys.path.append("..")
from PIL import Image,ImageDraw,ImageFont

# Rotary Encoder
from pyky040 import pyky040


# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level=logging.DEBUG)
try:
    # display with hardware SPI:
    ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    #disp = LCD_1inch28.LCD_1inch28(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp = LCD_1inch28(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    #disp = LCD_1inch28.LCD_1inch28()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()
    '''
    # Create blank image for drawing.
    image1 = Image.new("RGB", (disp.width, disp.height), "BLACK")
    draw = ImageDraw.Draw(image1)

    #logging.info("draw point")
    #draw.rectangle((Xstart,Ystart,Xend,Yend), fill = "color")
    logging.info("draw circle")
    draw.arc((1,1,239,239),0, 360, fill =(0,0,255))
    draw.arc((2,2,238,238),0, 360, fill =(0,0,255))
    draw.arc((3,3,237,237),0, 360, fill =(0,0,255))
    
    logging.info("draw dial line")
    draw.line([(120, 1),(120, 12)], fill = (128,255,128),width = 4)
    draw.line([(120, 227),(120, 239)], fill = (128,255,128),width = 4)
    draw.line([(1,120),(12,120)], fill = (128,255,128),width = 4)
    draw.line([(227,120),(239,120)], fill = (128,255,128),width = 4)

    logging.info("draw text")
    Font1 = ImageFont.truetype("../Font/Font01.ttf",25)
    Font2 = ImageFont.truetype("../Font/Font01.ttf",35)
    Font3 = ImageFont.truetype("../Font/Font02.ttf",32)

    draw.text((40, 50), 'WaveShare', fill = (128,255,128),font=Font2)
    text= u"微雪电子"
    draw.text((74, 150),text, fill = "WHITE",font=Font3)
    
    logging.info("draw pointer line")
    draw.line([(120, 120),(70, 70)], fill = "YELLOW",width = 3)
    draw.line([(120, 120),(176, 64)], fill = "BLUE",width = 3)
    draw.line([(120, 120),(120 ,210)], fill = "RED",width = 3)   
 
    im_r=image1.rotate(180)
    disp.ShowImage(im_r)
    time.sleep(3)
    logging.info("show image")
    '''
    while (True):
        '''
        # Show Possible Drinks
        # Blue
        image = Image.open('../pic/BlueDrink.jpg')	
        im_r=image.rotate(180)
        disp.ShowImage(im_r)
        time.sleep(5)
        # Green
        image = Image.open('../pic/GreenDrink.jpg')	
        im_r=image.rotate(180)
        disp.ShowImage(im_r)
        time.sleep(5)
        # Orange 
        image = Image.open('../pic/OrangeDrink.jpg')	
        im_r=image.rotate(180)
        disp.ShowImage(im_r)
        time.sleep(5)
        # Red
        image = Image.open('../pic/RedDrink.jpg')	
        im_r=image.rotate(180)
        disp.ShowImage(im_r)
        time.sleep(5)

        #Drink Animation
        #   25%
        for x in range(1, 10):
            image = Image.open('../pic/25_Filling_1.jpg')	
            im_r=image.rotate(180)
            disp.ShowImage(im_r)
            time.sleep(.25)
            image = Image.open('../pic/25_Filling_2.jpg')	
            im_r=image.rotate(180)
            disp.ShowImage(im_r)
            time.sleep(.25)
            image = Image.open('../pic/25_Filling_3.jpg')	
            im_r=image.rotate(180)
            disp.ShowImage(im_r)
            time.sleep(.25)
        #   50%
        for x in range(1, 10):
            image = Image.open('../pic/50_Filling_1.jpg')	
            im_r=image.rotate(180)
            disp.ShowImage(im_r)
            time.sleep(.25)
            image = Image.open('../pic/50_Filling_2.jpg')	
            im_r=image.rotate(180)
            disp.ShowImage(im_r)
            time.sleep(.25)
            image = Image.open('../pic/50_Filling_3.jpg')	
            im_r=image.rotate(180)
            disp.ShowImage(im_r)
            time.sleep(.25)
        image = Image.open('../pic/done.jpg')	
        im_r=image.rotate(180)
        disp.ShowImage(im_r)
        time.sleep(15)
        '''
        clkState = GPIO.input(clk)
        dtState = GPIO.input(dt)
        if clkState != clkLastState:
                if dtState != clkState:
                        counter += 1
                else:
                        counter -= 1
                if counter <= 25:   # Rotation Left?
                      counter = 0
                      print("Rotaiton Left?")
                if counter <= -25:  # Rotation Right?
                      counter = 0
                      print("Rotation Right?")       
        clkLastState = clkState
        time.sleep(0.01)
    disp.module_exit()
    logging.info("quit:")
    
except IOError as e:
    logging.info(e)    
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()
