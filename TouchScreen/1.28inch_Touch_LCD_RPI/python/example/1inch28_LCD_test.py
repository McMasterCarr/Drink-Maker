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
    draw.text((20, 120), 'By Seneca', fill = "BLACK",font=Font)
    disp.ShowImage(image1)
    time.sleep(5.5)
    Font = ImageFont.truetype("../Font/FlyingBirdFont.ttf",35)    
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

    #Draw line and show  
    x = y = data = l = 0
    color = "BLACK"
    Mode = 1
    Flag = 0
    Flgh = 0

    touch.Set_Mode(Mode)
    draw.rectangle((0,0,240,240),fill = "WHITE", outline=None, width=1)
    draw.rectangle((0, 0, 34, 208),fill = "RED", outline=None, width=1)
    draw.rectangle((0, 0, 208, 34),fill = "LIME", outline=None, width=1)
    draw.rectangle((205, 0, 240, 240),fill = "BLUE", outline=None, width=1)
    draw.rectangle((0, 205, 240, 240),fill = "GRAY", outline=None, width=1)
    disp.ShowImage(image1)

    while True:
             
        if Flgh == 0 and touch.X_point != 0:
            Flgh = 1
            x = touch.X_point
            y = touch.Y_point
                    
        if Flag == 1:
            if (touch.X_point > 34 and touch.X_point < 205) and (touch.Y_point > 34 and touch.Y_point < 208):
                Flgh = 3
            else:
                if (touch.X_point > 0 and touch.X_point < 33) and (touch.Y_point > 0 and touch.Y_point < 208):
                    color = "RED"
                    
                if (touch.X_point > 0 and touch.X_point < 208) and (touch.Y_point > 0 and touch.Y_point < 33):
                    color = "LIME"
                    
                if (touch.X_point > 208 and touch.X_point < 240) and (touch.Y_point > 0 and touch.Y_point < 240):
                    color = "BLUE"
                    
                if (touch.X_point > 0 and touch.X_point < 240) and (touch.Y_point > 208 and touch.Y_point < 240):
                    draw.rectangle((35,35,204,204),fill = "WHITE", outline=None, width=1)
                    disp.ShowImage(image1)
                Flgh = 4
                Flag = 0
                
            if Flgh == 3:
                if touch.X_point < 35:
                    touch.X_point = 35

                if touch.Y_point < 35:
                    touch.Y_point = 35
                
                if touch.Y_point > 203:
                    touch.Y_point = 203
                
                if touch.Y_point > 206:
                    touch.Y_point = 206

                # time.sleep(0.001) #Prevent disconnection  防止断触
                if l < 17000:           
                    Flag = 0
                    draw.line((x,y,touch.X_point,touch.Y_point), fill = color,width = 4)
                    disp.ShowImage_Windows(x,y,touch.X_point,touch.Y_point,image1)
                    l=0
                else:
                    Flag = 0
                    draw.rectangle((touch.X_point,touch.Y_point,touch.X_point+2,touch.Y_point+2),fill = color)
                    disp.ShowImage_Windows(x,y,touch.X_point,touch.Y_point,image1)
                    l=0
                    
                x = touch.X_point
                y = touch.Y_point
        
        l += 1 
        if l > 20000:
            l = 19000

except IOError as e:
    logging.info(e)    
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()