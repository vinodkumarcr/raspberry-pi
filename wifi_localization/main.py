
from flask import Flask, render_template, Response, stream_with_context, copy_current_request_context,redirect,url_for 
from flask_socketio import SocketIO
from time import sleep
from threading import Thread, Event
import random
from mcp3208 import MCP3208
import Adafruit_DHT
import serial
#app = Flask(__name__)
#app.config['SECRET_KEY'] = 'secret!'
#socketio = SocketIO(app)

import RPi.GPIO as GPIO   
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
red=17
green=27
buzz=22
GPIO.setup(buzz,GPIO.OUT)
GPIO.setup(red,GPIO.OUT)
GPIO.setup(green,GPIO.OUT)
sen=18
motor1a=12              #Two motors
motor1b=16
motor2a=20
motor2b=21
GPIO.setup(motor1a,GPIO.OUT)
GPIO.setup(motor1b,GPIO.OUT)
GPIO.setup(motor2a,GPIO.OUT)
GPIO.setup(motor2b,GPIO.OUT)
i=1
a=0
adc = MCP3208()
sensor=Adafruit_DHT.DHT11
ser=serial.Serial( port='/dev/ttyUSB0',
                    baudrate = 9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                   timeout=1)

def dht():
    humidity,temp=Adafruit_DHT.read_retry(sensor,sen)
    return humidity,temp

a='No location'
def loc():
    global a
    locat=ser.read(12)
    locati=str(locat)
    locatio=locati[2:-1]
    #print(locatio)
    #print(type(locatio))
    id1='5300CCA2E7DA'
    if locatio==str(id1):
        location='Plant'
        a=location
        #print(location)
    elif locatio=='5300CCA4764D':
        location='assembly section'
        #print(location)
        a=location
    elif locatio=='26005F8216ED':
        location='winding section'
        #print(location)
        a=location
    else:
        location=a
    return location
    
    
adc = MCP3208()
def calculate():
    gas=adc.read(0)
    #humidity,temp=dht()
    humidity=321
    temp=4214
    locs=loc()
            
    list=[locs,gas,humidity,temp]
    
        
        
        
        
    #list=[0,1,2,3,4]
    return list



app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

socketio = SocketIO(app)

thread = Thread()
thread_stop_event = Event()

class CountThread(Thread):
    def __init__(self):
        self.delay = 2
        super(CountThread, self).__init__()

    def ran(self):
        while True:
            temp=calculate()
            print(temp)
            socketio.emit('newnumber', {'number': temp}, namespace='/test')
            sleep(self.delay)

    def run(self):
        self.ran()

@app.route('/')
def index():
        return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = CountThread()
        thread.start()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')



@app.route("/move_forward")
def move_forward():                      #motor forward condition
    data1="FORWARD"
    GPIO.output(motor1a,GPIO.HIGH)
    GPIO.output(motor1b,GPIO.LOW)
    GPIO.output(motor2a,GPIO.LOW)
    GPIO.output(motor2b,GPIO.HIGH)#Moving forward code
    return 'true'

@app.route("/move_reverse")
def move_reverse():                      #motor reverse condition
    data1="BACK"
    GPIO.output(motor1a,GPIO.LOW)
    GPIO.output(motor1b,GPIO.HIGH)
    GPIO.output(motor2a,GPIO.HIGH)
    GPIO.output(motor2b,GPIO.LOW)
    return 'true'

@app.route("/stop/")
def stop():                         #motor stop condition
    data1="STOP"
    GPIO.output(motor1a,GPIO.LOW)
    GPIO.output(motor1b,GPIO.LOW)
    GPIO.output(motor2a,GPIO.LOW)
    GPIO.output(motor2b,GPIO.LOW)
    return 'true'

@app.route("/move_right")
def move_right():                        #motor right condition
    data1="RIGHT"
    GPIO.output(motor1a,GPIO.HIGH)
    GPIO.output(motor1b,GPIO.LOW)
    GPIO.output(motor2a,GPIO.HIGH)
    GPIO.output(motor2b,GPIO.LOW)
    return 'true'


@app.route("/move_left")
def move_left():                        #motor left condition 
        data1="LEFT"
        GPIO.output(motor1a,GPIO.LOW)
        GPIO.output(motor1b,GPIO.HIGH)
        GPIO.output(motor2a,GPIO.LOW)
        GPIO.output(motor2b,GPIO.HIGH)
        return 'true'


if __name__ == '__main__':
    socketio.run(app)
    app.run(host='0.0.0.0', debug=True)

   
