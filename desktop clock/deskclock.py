from time import sleep, strftime,localtime
import datetime        #we are calling for DATE
import RPi.GPIO as GPIO  #calling for header file which helps in using GPIO’s of PI

from board import *

h=0                    #integers for storing values
m=0
alarm=0
string_of_characters = 0


GPIO.setwarnings(False)  #do not show any warnings
GPIO.setmode (GPIO.BCM)    #programming the GPIO by BCM pin numbers. (like PIN29 as'GPIO5')

#initialize GPIO17,27,24,23,18,26,5,6,13,19 as an output
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)

GPIO.setup(21,GPIO.IN)  #initialize GPIO21 as an input.
GPIO.setup(20,GPIO.IN)  #initialize GPIO20 as an input.
GPIO.setup(16,GPIO.IN) 
GPIO.setup(12,GPIO.IN) 
GPIO.setup(25,GPIO.IN) 

GPIO.setup(22,GPIO.OUT) #initialize GPIO22 as an output.

def send_a_command (command):  #steps for sending a command to 16*2LCD
    pin=command
    PORT(pin);
    GPIO.output(17,GPIO.LOW)
    GPIO.output(27,GPIO.HIGH)
    sleep(0.001)
    GPIO.output(27,GPIO.LOW)
    pin=0
    PORT(pin); 

def send_a_character (character):#steps for sending a character to 16*2 LCD
    pin=character
    PORT(pin);
    GPIO.output(17,GPIO.HIGH)
    GPIO.output(27,GPIO.HIGH)
    sleep(0.001)
    GPIO.output(27,GPIO.LOW)
    pin=0
    PORT(pin);

def PORT(pin):            #assigning level for PI GPIO for sending data to LCD through D0-D7
    if(pin&0x01 == 0x01):
        GPIO.output(24,GPIO.HIGH)
    else:
        GPIO.output(24,GPIO.LOW)
    if(pin&0x02 == 0x02):
        GPIO.output(23,GPIO.HIGH)
    else:
        GPIO.output(23,GPIO.LOW)
    if(pin&0x04 == 0x04):
        GPIO.output(18,GPIO.HIGH)
    else:
        GPIO.output(18,GPIO.LOW)
    if(pin&0x08 == 0x08):
        GPIO.output(26,GPIO.HIGH)
    else:
        GPIO.output(26,GPIO.LOW)    
    if(pin&0x10 == 0x10):
        GPIO.output(5,GPIO.HIGH)
    else:
        GPIO.output(5,GPIO.LOW)
    if(pin&0x20 == 0x20):
        GPIO.output(6,GPIO.HIGH)
    else:
        GPIO.output(6,GPIO.LOW)
    if(pin&0x40 == 0x40):
        GPIO.output(13,GPIO.HIGH)
    else:
        GPIO.output(13,GPIO.LOW)
    if(pin&0x80 == 0x80):
        GPIO.output(19,GPIO.HIGH)
    else:
        GPIO.output(19,GPIO.LOW)

def send_a_string(string_of_characters):  #steps for sending string of characters to LCD
  string_of_characters = string_of_characters.ljust(16," ")
  for i in range(16):
    send_a_character(ord(string_of_characters[i])) #send characters one by one until all the strings characters are sent through data port

while True: 
    send_a_command(0x38); #use two lines of LCD
    send_a_command(0x0E); #screen and cursor ON
    send_a_command(0x01); #clear screen
    sleep(0.1)       #sleep for 100msec
    while True:
        dt = localtime()
        hour = dt[3]
        minute = dt[4]
        second = dt[5]
        if (GPIO.input(21) == 0):
            if (h<23):    #if button1 is pressed and hour count is less than 23 increment 'h' by one
                h=h+1

        if (GPIO.input(20) == 0):
            if (h>0):     #if button2 is pressed and hour count is more than 0 decrease 'h' by one
                h=h-1

        if (GPIO.input(16) == 0):
            if (m<59):    #if button3 is pressed and minute count is less than 59 increment 'm' by one
                m=m+1

        if (GPIO.input(12) == 0):
            if (m>0):     #if button4is pressed and minute count is more than 0 decrease 'm' by one
                m=m-1

        if (GPIO.input(25) == 0):  #if button5 is pressed toggle Alarm ON and OFF
            if (alarm==0):
                alarm = 1
            else:
                alarm = 0
            sleep(0.1)

        if (alarm==1):
            send_a_command(0x80 + 0x40 + 12);
            send_a_string("ON");  #if alarm is set, then display "ON" at the 12th position of second line of LCD

            if ((h==hour)):
                if ((m==minute)):
                    GPIO.output(22,1)  #if alarm is set, and hour-minute settings match the RTC time, trigger the buzzer
                    sleep(0.1)
                    GPIO.output(22,0)
                    sleep(0.1)
                else:
                    GPIO.output(22,0)
        if (alarm==0):
            send_a_command(0x80 + 0x40 + 12);
            send_a_string("OFF"); #if alarm is OFF, then display "OFF" at the 12th position of second line of LCD
            GPIO.output(22,0)       #turn off the buzzer         

        send_a_command(0x80 + 0);   #move cursor to 0 position
        send_a_string ("Time:%02d:%02d:%02d" % (hour,minute,second)); #display RTC hours, minutes, seconds
        send_a_command(0x80 + 0x40 + 0);  #move cursor to second line
        send_a_string ("Alarm:%02d:%02d" % (h,m));  #show alarm time
        sleep(0.1)  #wait for 100msec
