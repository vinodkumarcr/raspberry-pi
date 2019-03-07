
from flask import Flask, render_template, Response, stream_with_context, copy_current_request_context,redirect,url_for 
from flask_socketio import SocketIO
from time import sleep
from threading import Thread, Event
import random
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
TRIG=18 #GPIO03                 one Ultrasonic sensors
ECHO=23 #GPIO04
motor=24
motor1a=12              #Two motors
motor1b=16
motor2a=20
motor2b=21
GPIO.setup(motor,GPIO.OUT)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(motor1a,GPIO.OUT)
GPIO.setup(motor1b,GPIO.OUT)
GPIO.setup(motor2a,GPIO.OUT)
GPIO.setup(motor2b,GPIO.OUT)
i=1
def get_distance():
    try:                        #get the data from one ultrasonic value in distace
        GPIO.output(TRIG,GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(TRIG,GPIO.LOW)
        while GPIO.input(ECHO)==False:
            start=time.time()
        while GPIO.input(ECHO)==True:
            end=time.time()
        seg_time=end-start
        distance=seg_time/0.000058
    except:
        distance=2.10
    return distance

def calculate():

    a=get_distance()
    b="%0.2f" %a
    plant=float(b)
    #a=random.randint(0,20)
    if plant>5.20:
        data='MOTOR ON'
        print(data)
        GPIO.output(motor,GPIO.HIGH)
        GPIO.output(red,GPIO.HIGH)
        GPIO.output(green,GPIO.LOW)
        GPIO.output(buzz,GPIO.HIGH)
        
        
    else:
        data='MOTOR OFF'
        print(data)
        GPIO.output(motor,GPIO.LOW)
        GPIO.output(red,GPIO.LOW)
        GPIO.output(green,GPIO.HIGH)
        GPIO.output(buzz,GPIO.LOW)
        
    list=[data,plant]
        
        
        
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

   
