# Driver for JHD1313 based 16x2 LCD display

from utime import sleep_us, sleep
from machine import I2C, Pin

LCD_2LINE = 0x08
LCD_FUNCTIONSET = 0x20
LCD_CLEARDISPLAY = 0x01
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTDECREMENT = 0x00
LCD_ENTRYMODESET = 0x04

LCD_DISPLAYCONTROL = 0x08
LCD_DISPLAYON = 0x04
#define LCD_DISPLAYOFF 0x00
#define LCD_CURSORON 0x02
LCD_CURSOROFF = 0x00
#define LCD_BLINKON 0x01
LCD_BLINKOFF = 0x00

LCD_DDRAM = 0x80 

class LCD:
    def __init__(self, channel, sda, scl):
        
        self.i2c = I2C(channel, sda=Pin(sda), scl=Pin(scl), freq=400000)
        self.address = self.i2c.scan()[0]
        sleep(1)
        # first try
        self.send_command(LCD_FUNCTIONSET | LCD_2LINE)
        sleep_us(4500) # wait more than 4.1ms
        
        # second try
        self.send_command(LCD_FUNCTIONSET | LCD_2LINE)
        sleep_us(150)
        
        # third try
        self.send_command(LCD_FUNCTIONSET | LCD_2LINE)
        self.send_command(LCD_FUNCTIONSET | LCD_2LINE)
    
        # Set display on, cursor and blink off
        self.send_command(LCD_DISPLAYCONTROL | LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF)
        
        # Clear display
        self.clear()
        
        # Set display mode
        self.send_command(LCD_ENTRYMODESET | LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT)
    
    def clear(self):
        self.send_command(LCD_CLEARDISPLAY)
        sleep_us(2000)
        
    def send_command(self, command):
        self.i2c.writeto(self.address, bytes([0x80, command]))
    
    def write(self, str):
        for char in str:
            if char == '°':
                index = 223
            else:
                index = ord(char)
            
            self.i2c.writeto(self.address, bytes([0x40, index]))
    
    def move_cursor(self, x, y):
        address = x
        if (y == 1):
            address += 0x40
        self.send_command(LCD_DDRAM | address)
