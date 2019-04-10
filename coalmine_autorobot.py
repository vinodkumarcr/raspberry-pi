import RPi.GPIO as GPIO
import RPi.GPIO as io
import time
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
red=2
green=3
buzz=4
motor1a=12              #Two motors
motor1b=16
motor2a=20
motor2b=21
TRIG1=6                #Two Ultrasonic sensors
ECHO1=13
TRIG2=19
ECHO2=26
ir1=9
ir2=11
ir3=5
up=8
down=7
lefts=14
rights=15
stops=10
GPIO.setup(ir1,GPIO.IN)
GPIO.setup(ir2,GPIO.IN)
GPIO.setup(ir3,GPIO.IN)
GPIO.setup(ECHO1,GPIO.IN)
GPIO.setup(ECHO2,GPIO.IN)
GPIO.setup(TRIG1,GPIO.OUT)
GPIO.setup(TRIG2,GPIO.OUT)
GPIO.setup(motor1a,GPIO.OUT)
GPIO.setup(motor1b,GPIO.OUT)
GPIO.setup(motor2a,GPIO.OUT)
GPIO.setup(motor2b,GPIO.OUT)
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,lcd_columns, lcd_rows, lcd_backlight)
GPIO.setup(up, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(down, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(lefts, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(rights, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(stops, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(red,GPIO.OUT)
GPIO.setup(green,GPIO.OUT)
GPIO.setup(buzz,GPIO.OUT)
GPIO.output(red,GPIO.LOW)
GPIO.output(green,GPIO.LOW)
GPIO.output(buzz,GPIO.LOW)
GPIO.output(motor1a,GPIO.LOW)
GPIO.output(motor1b,GPIO.LOW)
GPIO.output(motor2a,GPIO.LOW)
GPIO.output(motor2b,GPIO.LOW)
print(type(GPIO.input(up)),type(GPIO.LOW))
def front_distance(TRIG1,ECHO1):             #get the data from one ultrasonic value in distace
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
def back_distance(TRIG2,ECHO2):              #get the data from one ultrasonic value in distace
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
def reverse():                      #motor forward condition
    GPIO.output(motor1a,GPIO.HIGH)
    GPIO.output(motor1b,GPIO.LOW)
    GPIO.output(motor2a,GPIO.LOW)
    GPIO.output(motor2b,GPIO.HIGH)
def forward():                      #motor reverse condition
    GPIO.output(motor1a,GPIO.LOW)
    GPIO.output(motor1b,GPIO.HIGH)
    GPIO.output(motor2a,GPIO.HIGH)
    GPIO.output(motor2b,GPIO.LOW)
def stop():                         #motor stop condition
    GPIO.output(motor1a,GPIO.LOW)
    GPIO.output(motor1b,GPIO.LOW)
    GPIO.output(motor2a,GPIO.LOW)
    GPIO.output(motor2b,GPIO.LOW)
def left():                        #motor right condition
    GPIO.output(motor1a,GPIO.HIGH)
    GPIO.output(motor1b,GPIO.LOW)
    GPIO.output(motor2a,GPIO.HIGH)
    GPIO.output(motor2b,GPIO.LOW)
def right():                         #motor left condition 
    GPIO.output(motor1a,GPIO.LOW)
    GPIO.output(motor1b,GPIO.HIGH)
    GPIO.output(motor2a,GPIO.LOW)
    GPIO.output(motor2b,GPIO.HIGH)
def normal():
    GPIO.output(red,GPIO.LOW)
    GPIO.output(green,GPIO.HIGH)
    GPIO.output(buzz,GPIO.LOW)
def danger():
    GPIO.output(red,GPIO.HIGH)
    GPIO.output(green,GPIO.LOW)
    GPIO.output(buzz,GPIO.HIGH)
def left_ir():
    if GPIO.input(ir1)==True:
        data="danger"
    else:
        data="normal"
    return data
def right_ir():
    if GPIO.input(ir2)==True:
        data="danger"
    else:
        data="normal"
    return data
def middle_ir():
    if GPIO.input(ir3)!=True:
        data="danger"
    else:
        data="normal"
    return data
lcd.move_right()        
lcd.message("****WELCOME*****\nTO THE PROJECT")
time.sleep(3)
lcd.clear()
#lcd.message("*TO THE PROJECT*")
#time.sleep(3)
lcd.clear()
while True:
    front_ultra=front_distance(TRIG1,ECHO1)
    print(front_ultra)
    back_ultra=back_distance(TRIG2,ECHO2)
    print(back_ultra)
    time.sleep(1)
    print("")
    left_ir1=left_ir()
    right_ir1=right_ir()
    middle_ir1=middle_ir()
    if front_ultra<10.0:
        lcd.message("FRONT OBSTACLE\n  DETECTED")
        danger()
        reverse()
        time.sleep(5)
        stop()
        normal()
        lcd.clear()
        
    if back_ultra<10.0:
        lcd.message("BACK OBSTACLE\n  DETECTED")
        danger()
        forward()
        time.sleep(5)
        stop()
        normal()
        lcd.clear()
    if left_ir1!="danger":
        lcd.message("LEFT EDGE  \n DETECTION")
        danger()
        time.sleep(5)
        lcd.clear()
    if right_ir1!="danger":
        lcd.message("RIGHT EDGE  \n  DETECTION")
        danger()
        time.sleep(5)
        lcd.clear()
    if middle_ir1=="danger":
        lcd.message("FALLING DANGER")
        danger()
        time.sleep(5)
        lcd.clear()
    else:
        normal()
        lcd.message("  VEHICLE \n ON ITS WAY")
        time.sleep(3)
        lcd.clear()
        
    if GPIO.input(up)==False:
        lcd.message("MOVING FORWARD")
        forward()
        time.sleep(3)
        print("forward")
        lcd.clear()
    if GPIO.input(down)==False:
        lcd.message("MOVING REVERSE")
        reverse()
        time.sleep(3)
        lcd.clear()
        print("reverse")
    if GPIO.input(lefts)==False:
        lcd.message("MOVING LEFT")
        left()
        time.sleep(3)
        print("left")
        lcd.clear()
    if GPIO.input(rights)==False:
        lcd.message("MOVING RIGHT")
        right()
        time.sleep(3)
        lcd.clear()
        print("right")
    if GPIO.input(stops)==False:
        lcd.message("VEHICLE STOPPED")
        stop()
        time.sleep(3)
        print("stop")
        lcd.clear()
        
        
        
        
        
 
        
        
    
