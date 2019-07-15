from time import sleep, strftime,localtime
from datetime import datetime
from DS3231 import DS3231

rtc = DS3231.SDL_DS3231(1,0x68)
rtc.write_now()

w = rtc._read_hours()
print(w)
