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

drinkSelection = 0
drinkSelection = 0
#]dispensing = False

Mode = 0
logging.basicConfig(level=logging.DEBUG)
global Flag

touch = Touch_1inch28.Touch_1inch28()

drink_data =    [{'name': 'Margarita', 'primary_color': 'LIME','secondary_color': 'WHITE'},
                {'name':'Mojito', 'primary_color':'green','secondary_color':'BLACK'},
                {'name':'Manhattan', 'primary_color':'coral','secondary_color':'BLACK'},
                {'name':'Mimosa', 'primary_color':'LIME','secondary_color':'OrangeRed'},
                {'name':'Screwdriver', 'primary_color':'coral','secondary_color':'orange'},
                ]

def Int_Callback(TP_INT):       
        if Mode == 1:
            global Flag 
            Flag = 1
            touch.get_point()
        else:
            touch.Gestures = touch.Touch_Read_Byte(0x01)

def dispense():
    print("\n\nDispense!\n\n")
    time.sleep(2)

def sizeOptions():
    global drinkSize
    dispensing = False
    drinkSize = 1
    image2 = Image.new("RGB", (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image2)
    draw.rectangle((0,0,240,240),fill = "BLACK", outline=None, width=1)
    draw.text((65, 90), str(drinkSize), fill = "WHITE",font=Font)
    disp.ShowImage(image1)
    time.sleep(0.5)
    while dispensing == False:
        if touch.Gestures == 0x03:
            drinkSize-=1
            if drinkSize <= 0:
                drinkSize = 1
        if touch.Gestures == 0x04:
            drinkSize+=1
            if drinkSize > 3 :
                drinkSize = 3
        if touch.Gestures == 0x05:
            dispensing = True
            dispense()
        touch.Gestures = 0x01
        time.sleep(0.01)

try:
    global dispensing
    dispensing = False
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
        draw.rectangle((0,0,240,240),fill = drink_data[drink_list_index]['secondary_color'], outline=None, width=1)
        while True:
            while touch.Gestures == 0x03 or touch.Gestures == 0x04:
                print('\nTouch Gesture:  ' + str(touch.Gestures))
                gesture = touch.Gestures
                if touch.Gestures == 0x03:
                    drink_list_index-=1
                    if drink_list_index < 0:
                        drink_list_index = 0
                if touch.Gestures == 0x04:
                    drink_list_index+=1
                    if drink_list_index > len(drink_data) -1 :
                        drink_list_index -= 1
                draw.rectangle((0,0,240,240),fill = drink_data[drink_list_index]['secondary_color'], outline=None, width=1)
                draw.text((65, 90), drink_data[drink_list_index]['name'], fill = drink_data[drink_list_index]['primary_color'],font=Font)
                disp.ShowImage(image1)
                time.sleep(0.001)
                touch.Gestures = 0x01

            if touch.Gestures == 0x05:
                touch.Gesture=0x01
                sizeOptions()
                dispensing = False
            
                
        '''
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
        draw.rectangle((0,0,240,240),fill = drink_data[drink_list_index]['secondary_color'], outline=None, width=1)
        while True:
            while touch.Gestures != 0x03 or touch.Gestures != 0x04 or touch.Gestures != 0x0C:
                print('\nTouch Gesture:  ' + str(touch.Gestures))
                if touch.Gestures != 0x0B:
                    drink_selection = drink_list_index
                    sizeOptions()
                if touch.Gestures != 0x03:
                    drink_list_index-=1
                    if drink_list_index < 0:
                        drink_list_index = 0
                if touch.Gestures != 0x04:
                    drink_list_index+=1
                    if drink_list_index > len(drink_data) -1 :
                        drink_list_index -= 1
                draw.rectangle((0,0,240,240),fill = drink_data[drink_list_index]['secondary_color'], outline=None, width=1)
                draw.text((65, 90), drink_data[drink_list_index]['name'], fill = drink_data[drink_list_index]['primary_color'],font=Font)
                disp.ShowImage(image1)
                time.sleep(0.1)



            draw.rectangle((0,0,240,240),fill = drink_data[drink_list_index]['secondary_color'], outline=None, width=1)
            while touch.Gestures != 0x04:
                #   change code/drink_data to include text location coordinates
                draw.text((55, 90), drink_data[drink_list_index]['name'], fill = drink_data[drink_list_index]['primary_color'],font=Font)
                disp.ShowImage(image1)
                time.sleep(0.001)
            drink_list_index+=1
            


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