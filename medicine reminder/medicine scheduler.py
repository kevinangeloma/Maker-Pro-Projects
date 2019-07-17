from time import time,sleep, strftime,localtime
from datetime import datetime
import RPi.GPIO as GPIO
from Adafruit_CharLCD import Adafruit_CharLCD  as LCD


time_window_size = 5 #duration of the reminder in minutes
schedule = [390,720,875,1080] #list of scheduled medicine reminders
#schedule is kept in minutes past midnight

# Raspberry Pi pin setup
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 18
lcd_d7 = 22
lcd_backlight = 2

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

# Define pin number of specific day
sunday = 27
monday = 5
tuesday = 6
wednesday = 26
thursday = 16
friday = 12
saturday = 13

# Mode can either be BOARD or BCM
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Iniatilization of GPIO pins

GPIO.setup(sunday, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(monday, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(tuesday, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(wednesday, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(thursday, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(friday, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(saturday, GPIO.OUT, initial=GPIO.LOW)


lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows,lcd_backlight)

was_printed = False
off_was_printed = True
one_time_only = False
checked_schedule = False
run = True
while run:
  lcd.clear()
  message = (datetime.now().strftime('%b %d %Y \n%I:%M:%S %p\n'))
  lcd.message(message)
  sleep(1)
  dt = localtime()
  hour = dt[3]
  minute = dt[4]
  second = dt[5]
  weekday = dt[6] # Monday is 0

  if second < 10: #check schedule once a minute only
    if one_time_only == False:
      one_time_only = True
      checked_schedule = False
    else:
      one_time_only = 0
    cur_time_mins = minute + 60 * hour # current time in minutes past midnight
    if checked_schedule == False:
        if was_printed == False:
          checked_schedule = True
          schedule_loop = 0
          while schedule_loop < len(schedule):
            schedule_time_window = schedule[schedule_loop] + time_window_size
            if schedule_time_window > (59 + 23*60):
              schedule_time_window = (59 + 23*60)
            if cur_time_mins < schedule_time_window:
              if schedule[schedule_loop] <= cur_time_mins:
                print("Medicine Alarm!!")
                was_printed = True;
                turn_off_mins = schedule[schedule_loop] + time_window_size
                off_was_printed = False
                if turn_off_mins > (59 + 23*60): # if turn off past midnight
                  turn_off_mins = (59 + 23*60) #   then turn off one minute before midnight
                if weekday == 0:
                        GPIO.output(monday, GPIO.HIGH)
                elif weekday == 1:
                        GPIO.output(tuesday, GPIO.HIGH)
                elif weekday == 2:
                        GPIO.output(wednesday, GPIO.HIGH)
                elif weekday == 3:
                        GPIO.output(thursday, GPIO.HIGH)
                elif weekday == 4:
                        GPIO.output(friday, GPIO.HIGH)
                elif weekday == 5:
                        GPIO.output(saturday, GPIO.HIGH)
                elif weekday == 6:
                        GPIO.output(sunday, GPIO.HIGH)
                lcd.clear()
                message = 'Its Time!!'
                lcd.message(message)
                n=0
                while (n<12):
                  for i in range(lcd_columns-len(message)):
                    sleep(0.5)
                    lcd.move.right()
                for i in range(lcd_columns-len(message)):
                  sleep(0.5)
                  lcd.move_left()
                n += 1
            schedule_loop += 1
        if off_was_printed == False:
          if cur_time_mins >= turn_off_mins:
            print("Medicine Alarm Off!")
            off_was_printed = True
            was_printed = 0 # to prevent re-checking during the reminder period that would move the reminder window and we do not wan$
            if weekday == 0:
              GPIO.output(monday, GPIO.LOW)
            elif weekday == 1:
              GPIO.output(tuesday, GPIO.LOW)
            elif weekday == 2:
              GPIO.output(wednesday, GPIO.LOW)
            elif weekday == 3:
              GPIO.output(thursday, GPIO.LOW)
            elif weekday == 4:
              GPIO.output(friday, GPIO.LOW)
            elif weekday == 5:
              GPIO.output(saturday, GPIO.LOW)
            elif weekday == 6:
              GPIO.output(sunday, GPIO.LOW)
