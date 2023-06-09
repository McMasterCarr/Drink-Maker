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

drink_data = [{'name': 'Margarita', 'primary_color': 'LIME',
         'secondary_color': 'WHITE'}, {'name':'Mojito', 'primary_color':'green','secondary_color':'BLACK'}]

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
        time.sleep(1.5)
        Font = ImageFont.truetype("../Font/FlyingBirdFont.ttf",45)
        drink_list_index = 0
        while True:
            draw.rectangle((0,0,240,240),fill = drink_data[drink_list_index]['secondary_color'], outline=None, width=1)
            while touch.Gestures != 0x03 or touch.Gestures != 0x04:
                if touch.Gestures != 0x03:
                    drink_list_index-=1
                    if drink_list_index < 0:
                        drink_list_index = 0
                if touch.Gestures != 0x04:
                    drink_list_index+=1
                    if drink_list_index > len(drink_data):
                        drink_list_index == len(drink_data)
                        
                print(str(drink_list_index))
                draw.text((65, 90), drink_data[drink_list_index]['name'], fill = drink_data[drink_list_index]['primary_color'],font=Font)
                disp.ShowImage(image1)
                time.sleep(0.01)
            '''
            draw.rectangle((0,0,240,240),fill = drink_data[drink_list_index]['secondary_color'], outline=None, width=1)
            while touch.Gestures != 0x04:
                #   change code/drink_data to include text location coordinates
                draw.text((55, 90), drink_data[drink_list_index]['name'], fill = drink_data[drink_list_index]['primary_color'],font=Font)
                disp.ShowImage(image1)
                time.sleep(0.001)
            drink_list_index+=1
            '''

        '''
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
        '''

except IOError as e:
    logging.info(e)    
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()