#for live video monitoring there is not code in html half page of image is created and in img tag at src change the image with ip address 
import RPi.GPIO as io   
import Adafruit_DHT
import time
import MCP3208 import MCP3208
io.setmode(io.BCM)
io.setwarnings(False)
pir=13                      #pir sensor
buzz=19
io.setup(pir,io.IN)
io.setup(buzz,io.OUT)
sen=18
buzz=26
io.setup(buzz,io.OUT)
sensor=Adafruit_DHT.DHT11
TRIG1=3 #GPIO03                 Two Ultrasonic sensors
ECHO1=4 #GPIO04
TRIG2=17 #GPIO17
ECHO2=27 #GIO27
motor1a=24              #Two motors
motor1b=23
motor2a=15
motor2b=14
i=1
ser = serial.Serial(gps_port, baudrate = 9600, timeout = 0.5)
def get_distance1(TRIG1,ECHO1):             #get the data from one ultrasonic value in distace
    io.output(TRIG1,io.HIGH)
    time.sleep(0.00001)
    io.output(TRIG1,io.LOW)
    while io.input(ECHO1)==False:
        start=time.time()
    while io.input(ECHO1)==True:
        end=time.time()
    seg_time=end-start
    distance=seg_time/0.000058
    return distance
def get_distance2(TRIG2,ECHO2):              #get the data from one ultrasonic value in distace
    io.output(TRIG2,io.HIGH)
    time.sleep(0.00001)
    io.output(TRIG2,io.LOW)
    while io.input(ECHO2)==False:
        start=time.time()
    while io.input(ECHO2)==True:
        end=time.time()
    seg_time=end-start
    distance=seg_time/0.000058
    return distance
def forward():                      #motor forward condition
    GPIO.output(motor1a,GPIO.HIGH)
    GPIO.output(motor1b,GPIO.LOW)
    GPIO.output(motor2a,GPIO.LOW)
    GPIO.output(motor2b,GPIO.HIGH)
def reverse():                      #motor reverse condition
    GPIO.output(motor1a,GPIO.LOW)
    GPIO.output(motor1b,GPIO.HIGH)
    GPIO.output(motor2a,GPIO.HIGH)
    GPIO.output(motor2b,GPIO.LOW)
def stop():                         #motor stop condition
    GPIO.output(motor1a,GPIO.LOW)
    GPIO.output(motor1b,GPIO.LOW)
    GPIO.output(motor2a,GPIO.LOW)
    GPIO.output(motor2b,GPIO.LOW)
def right():                        #motor right condition
    GPIO.output(motor1a,GPIO.HIGH)
    GPIO.output(motor1b,GPIO.LOW)
    GPIO.output(motor2a,GPIO.HIGH)
    GPIO.output(motor2b,GPIO.LOW)
def left():                         #motor left condition 
    GPIO.output(motor1a,GPIO.LOW)
    GPIO.output(motor1b,GPIO.HIGH)
    GPIO.output(motor2a,GPIO.LOW)
    GPIO.output(motor2b,GPIO.HIGH)
def GPS():                          #GPS value
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
adc=MCP3208()
while True:
	humidity,temp=Adafruit_DHT.read_retry(sensor,sen)
	print ("humidity:",humidity,"RH")       #HUmidity reading
	print ("temp:",temp,"C")                #temperature value
	gps_coords=gps()                        #gps coordinates will get
	value=adc.read(0)
	print('gas value:',value)               #gas sensor value and status
	time.sleep(0.5)
	

	if io.input(pir)==True:                 #pir status
            print ('person is detected')
            time.sleep(0.5)
        else:               
            print ('person is not detected')
	

