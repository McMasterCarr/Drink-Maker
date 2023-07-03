#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_1inch28,Touch_1inch28
from PIL import Image,ImageDraw,ImageFont

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18

TP_INT = 4

Mode = 0
logging.basicConfig(level=logging.DEBUG)
global Flag

touch = Touch_1inch28.Touch_1inch28()

def Int_Callback(TP_INT):       
        if Mode == 1:
            global Flag 
            Flag = 1
            touch.get_point()
        else:
            touch.Gestures = touch.Touch_Read_Byte(0x01)


try:
    while True:
        ''' Warning!!!Don't  create multiple displayer objects!!! '''
        disp = LCD_1inch28.LCD_1inch28()
        # Initialize library.
        disp.Init()
        # Clear display.
        disp.clear()
        
        touch.init()
        
        touch.int_irq(TP_INT,Int_Callback) 
        # Create blank image for drawing.
        # Common HTML color names.
        image1 = Image.new("RGB", (disp.width, disp.height), "WHITE")
        draw = ImageDraw.Draw(image1)

        #Gestures
        Mode = 0
        touch.Set_Mode(Mode)
        Font1 = ImageFont.truetype("../Font/Font02.ttf",24)
        Font = ImageFont.truetype("../Font/FlyingBirdFont.ttf",24)
        draw.text((65, 80), 'Drink Maker', fill = "BLACK",font=Font)
        draw.text((65, 120), 'By Seneca', fill = "BLACK",font=Font)
        disp.ShowImage(image1)
        time.sleep(5.5)
        Font = ImageFont.truetype("../Font/FlyingBirdFont.ttf",45)    
        draw.rectangle((0,0,240,240),fill = "WHITE", outline=None, width=1)
        while touch.Gestures != 0x03:
            draw.text((65, 90), 'LEFT', fill = "BLACK",font=Font)
            disp.ShowImage(image1)
            time.sleep(0.001)

        draw.rectangle((0,0,240,240),fill = "WHITE", outline=None, width=1)
        while touch.Gestures != 0x04:
            draw.text((55, 90), 'RIGHT', fill = "BLACK",font=Font)
            disp.ShowImage(image1)
            time.sleep(0.001)

        draw.rectangle((0,0,240,240),fill = "WHITE", outline=None, width=1)
        while touch.Gestures != 0x0C:
            draw.text((35, 90), 'Long Press', fill = "BLACK",font=Font)
            disp.ShowImage(image1)
            time.sleep(0.001)

        draw.rectangle((0,0,240,240),fill = "WHITE", outline=None, width=1)
        while touch.Gestures != 0x0B:
            draw.text((30, 90), 'Double Click', fill = "BLACK",font=Font)
            disp.ShowImage(image1)
            time.sleep(0.001)

except IOError as e:
    logging.info(e)    
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()