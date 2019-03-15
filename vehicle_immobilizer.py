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
key=13
motor=21
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,lcd_columns, lcd_rows, lcd_backlight)
passwd=['0','0','0','0']
a=[]
GPIO.setup(10, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)   #increment
GPIO.setup(9, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)    #decrement
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)   #enter
GPIO.setup(19, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)   #cursor front
GPIO.setup(26, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)   #cursor back
GPIO.setup(key, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)  #key
GPIO.setup(motor,GPIO.OUT)
GPIO.output(motor,GPIO.LOW)
count=0
a=0
error_count=0
send_count=1
numbers=['0','1','2','3','4','5','6','7','8','9']
##SERIAL_PORT = "/dev/ttyAMA0"
##ser2 = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 5)
##ldrmsg=0
##tempmsg=0
##ser2.write("AT+CMGF=1\r") # set to text mode
##time.sleep(1)
##ser2.write('AT+CMGDA="DEL ALL"\r') # delete all SMS
##time.sleep(1)
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
    for i in range(20):
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
    port.write('AT+CMGDA="DEL ALL"\r')
    rcv=port.read(10)
    print rcv
    time.sleep(1)
    port.write('AT+CMGD=1,4\r')
    rcv=port.read(10)
    print rcv
    time.sleep(1)

def deletesms():
    port.write("AT\r")
    time.sleep(1)
    port.write("AT+CMGF=1\r") # set to text mode
    time.sleep(1)
    port.write("AT+CNMI=1,2,0,0,0\r")
    time.sleep(1)
    port.write("AT+IPR=9600\r")
    time.sleep(1)
    port.write("AT&W\r")
    time.sleep(1)
    port.write('AT+CMGDA="DEL ALL"\r')
    rcv=port.read(10)
    print rcv
    time.sleep(1)
    port.write('AT+CMGD=1,4\r')
    rcv=port.read(10)
    print rcv
    time.sleep(1)

deletesms()
while True:
    gps=GPS()
    if GPIO.input(key)==GPIO.HIGH:
        passwd=['0','0','0','0']
        count=0
        a=0
        lcd.message('**MOTOR TURN ON*')
        time.sleep(2)
        lcd.clear()
        lcd.message('****WELCOME*****')
        time.sleep(2)
        lcd.clear()
        lcd.message('*ENTER PASSWORD*')
        time.sleep(2)
        lcd.clear()
        while True:
            #reply = port.read(port.inWaiting())
            gps=GPS()
            try:
                if count<1000:
                    if error_count>=3:
                        while True:
                            GPIO.output(motor,GPIO.LOW)
                            lcd.message('ALL WRONG PASSWD')
                            time.sleep(2)
                            lcd.clear()
                            lcd.message('VEHICLE LOCKED')
                            time.sleep(3)
                            lcd.clear()
                            if send_count<2:
                                lcd.message('LOCATION SENDING')
                                send_count+=1
                                time.sleep(3)
                                lcd.clear()
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
                                    deletesms()
                                    break
                                
                    if GPIO.input(10)==GPIO.HIGH:
                        count+=1
                        passwd[a]=numbers[count]
                        #time.sleep(1)
                        print passwd
                        #lcd.clear()
                    if GPIO.input(9)==GPIO.HIGH:
                        count-=1
                        passwd[a]=numbers[count]
                        #lcd.clear()
                        #time.sleep(1)
                        print passwd
                    if GPIO.input(19)==GPIO.HIGH:
                        a+=1
                        if a>4:
                            a=0
                        #lcd.clear()
                        print passwd
                    if GPIO.input(26)==GPIO.HIGH:
                        a-=1
                        if a<=0:
                            a=0
                        #lcd.clear()
                        print passwd
                    reply = port.read(port.inWaiting()) # Clean buf
                    if reply != "":
                        print "SMS received. Content: TRACK"
                        print reply
                        if "TRACK" in reply:
                            print "GOT TRACK IN REPLY"
                            lcd.message("GOT TRACK IN SMS")
                            time.sleep(2)
                            lcd.clear()
                            data=ser.readline()
                            time.sleep(3)
                            sms()
                            port.write("AT+CMGF=1\r") # set to text mode
                            time.sleep(1)
                            port.write('AT+CMGDA="DEL ALL"\r')
                            rcv=port.read(10)
                            print rcv
                            time.sleep(1)
                            port.write('AT+CMGD=1,4\r')
                            rcv=port.read(10)
                            print rcv
                            time.sleep(1)
                    else:
                        time.sleep(1)
                        pass
                #data='---',str(passwd),'---'
                lcd.message(passwd)
                time.sleep(2)
                lcd.clear()
                if GPIO.input(key)==GPIO.LOW:
                    break
                reply = port.read(port.inWaiting()) # Clean buf
                if reply != "":
                    print "SMS received. Content: TRACK1"
                    print reply
                    if "TRACK" in reply:
                        print "GOT TRACK IN REPLY"
                        lcd.message("GOT TRACK IN SMS")
                        time.sleep(2)
                        lcd.clear()
                        data=ser.readline()
                        time.sleep(3)
                        sms()
                        deletesms()
                        break
                    if "STOP" in reply:
                        print "GOT STOP IN REPLY"
                        lcd.message("GOT STOP IN SMS")
                        time.sleep(2)
                        lcd.clear()
                        data=ser.readline()
                        time.sleep(3)
                        GPIO.output(motor,GPIO.LOW)
                        print 'ENGINE STOP'
                        lcd.message('ENGINE OFF')
                        time.sleep(5)
                        lcd.clear()
                        while True:
                            lcd.message('BIKE IMMOBILIZED')
                            time.sleep(3)
                            lcd.clear()
                            reply = port.read(port.inWaiting()) # Clean buf
                            if reply != "":
                                print "SMS received. Content:"
                                print reply
                                if "START" in reply:
                                    print "GOT START IN REPLY"
                                    lcd.message("GOT START IN SMS")
                                    time.sleep(2)
                                    lcd.clear()
                                    data=ser.readline()
                                    GPIO.output(motor,GPIO.HIGH)
                                    print 'ENGINE START'
                                    lcd.message('ENGINE START')
                                    time.sleep(5)
                                    lcd.clear()
                                    sms()
                                    deletesms()
                                    break
                    if "START" in reply:
                        print "GOT START IN REPLY"
                        lcd.message("GOT START IN SMS")
                        time.sleep(2)
                        lcd.clear()
                        data=ser.readline()
                        time.sleep(3)
                        GPIO.output(motor,GPIO.HIGH)
                        print 'ENGINE START'
                        lcd.message('ENGINE START')
                        time.sleep(5)
                        lcd.clear()
                        sms()
                        deletesms()
                        break
                
                if len(passwd)>5:
                    lcd.clear()
                if GPIO.input(11)==GPIO.HIGH:
                    data=''.join(passwd)
                    while True:
                        try:
                            if data=='1234':
                                while True:
                                    print 'ENGINE START'
                                    GPIO.output(motor,GPIO.HIGH)
                                    lcd.message("ENGINE START")
                                    time.sleep(2)
                                    lcd.clear()
                                    reply = port.read(port.inWaiting()) # Clean buf
                                    if reply != "":
                                        print "SMS received. Content:"
                                        print reply
                                        if "STOP" in reply:
                                            print "GOT STOP IN REPLY"
                                            lcd.message("GOT STOP IN SMS")
                                            time.sleep(1)
                                            lcd.clear()
                                            print "BIKE IMMOBILIZED"
                                            lcd.message("BIKE IMMOBILIZED")
                                            time.sleep(1)
                                            lcd.clear()
                                            GPIO.output(motor,GPIO.LOW)
                                            lcd.message('ENGINE OFF')
                                            time.sleep(5)
                                            lcd.clear()
                                            data=ser.readline()
                                            time.sleep(1)
                                            sms()
                                            deletesms()
                                            break
                                            while True:
                                                lcd.message('BIKE IMMOBILIZED')
                                                time.sleep(3)
                                                lcd.clear()
                                    if GPIO.input(key)==GPIO.LOW:
                                        print 'MOTOR IS OFF'
                                        lcd.message('MOTOR TURNED OFF')
                                        time.sleep(1)
                                        lcd.clear()
                                        data=None
                                        passwd=['0','0','0','0']
                                        count=0
                                        a=0
                                        GPIO.output(motor,GPIO.LOW)
                                        break
                                
                            elif data!=None and data!='1234':
                                print 'PASSWORD IS WRONG'
                                lcd.message('WRONG PASSWORD')
                                time.sleep(3)
                                lcd.clear()
                                lcd.message('TRY AGAIN')
                                time.sleep(2)
                                lcd.clear()
                                error_count+=1
                                print error_count
                                break
                            else:
                                break
                        except:
                            lcd.message('WRONG PASSWORD')
                            time.sleep(2)
                            lcd.clear()
                            
                                
                                
                            
            except:
                count=0
    else:
        lcd.message('MOTOR TURNED OFF')
        time.sleep(3)
        lcd.clear()
