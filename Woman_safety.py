#! /usr/bin python
import RPi.GPIO as GPIO
import time
import os
import serial
import pynmea2
import Adafruit_CharLCD as LCD
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
lcd_rs        = 27
lcd_en        = 22
lcd_d4        = 25
lcd_d5        = 24
lcd_d6        = 23
lcd_d7        = 18
lcd_backlight = 4
lcd_columns = 16
lcd_rows    = 2
key=3
buzz=4
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,lcd_columns, lcd_rows, lcd_backlight)
GPIO.setup(key, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(buzz,GPIO.OUT)

gps_port = "/dev/ttyUSB0" # the serial port to which the pi is connected.
 
#create a serial object
ser = serial.Serial(gps_port, baudrate = 9600, timeout = 0.5)
port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
def GPS():
    try:
        data = ser.readline()
    except:
	print "loading" 
	#wait for the serial port to churn out data
 
    if data[0:6] == '$GPGGA': # the long and lat data are always contained in the GPGGA string of the NMEA data
 
        msg = pynmea2.parse(data)
 
	#parse the latitude and print
        latval = msg.latitude
	concatlat = "lat:" + str(latval)
	#print concatlat
	longval = msg.longitude
	concatlong = "long:"+ str(longval)
	#print concatlong
           
	time.sleep(0.5)
	return [latval,longval]

def sms():
    # Enable Serial Communication
    port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
 
    # Transmitting AT Commands to the Modem
    # '\r\n' indicates the Enter key
    lcd.message('SMS SENDING....')
    port.write('AT'+'\r\n')
    rcv = port.read(10)
    print rcv
    time.sleep(1)
 
    port.write('ATE0'+'\r\n')      # Disable the Echo
    rcv = port.read(10)
    print rcv
    time.sleep(1)
 
    port.write('AT+CMGF=1'+'\r\n')  # Select Message format as Text mode 
    rcv = port.read(10)
    print rcv
    time.sleep(1)
 
    port.write('AT+CNMI=2,1,0,0,0'+'\r\n')   # New SMS Message Indications
    rcv = port.read(10)
    print rcv
    time.sleep(1)
    lcd.clear()
    # Sending a message to a particular Number
    gps=GPS()
 
    port.write('AT+CMGS="+919603896706"'+'\r\n')
    rcv = port.read(10)
    print rcv
    time.sleep(1)
    #lcd.message(str(gps))
    #time.sleep(3)
    #lcd.clear()
    while True:
        data=GPS()
        if data!=None and data!=[0.0,0.0]:
            gps=data
            break
        else:
            pass
    if gps!=None:
        message='http://www.google.com/maps/place/'+str(gps[0])+','+str(gps[1])
        lcd.message(str(gps))
        time.sleep(3)
        lcd.clear()
        print message
        port.write(message+'\r\n')  # Message
        rcv = port.read(10)
        print rcv
    else:
        port.write('GPS Coordinates Not available'+'\r\n')
        rcv=port.read(10)
        print rcv
 
    port.write("\x1A") # Enable to send SMS
    for i in range(10):
        rcv = port.read(10)
        print rcv

while True:
    try:
        if GPIO.input(key)==GPIO.HIGH:
            GPIO.output(buzz,GPIO.HIGH)
            lcd.message('WOMAN IS IN DANGER')
            time.sleep(2)
            lcd.clear()
            lcd.message('HELP! HELP!')
            time.sleep(2)
            lcd.clear()
            GPIO.output(buzz,GPIO.LOW)
            sms()
        reply = port.read(port.inWaiting()) # Clean buf
        if reply != "":
            print "SMS received. Content:"
            print reply
            if "TRACK" in reply:
                print "GOT TRACK IN REPLY"
                lcd.message("GOT TRACK IN SMS")
                time.sleep(2)
                lcd.clear()
                data=ser.readline()
                time.sleep(3)
                sms()
        else:
            print "woman is safe"
            lcd.message('WOMAN IS SAFE')
            time.sleep(3)
            lcd.clear()
            
            

