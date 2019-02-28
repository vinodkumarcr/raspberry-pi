import math
import time
import serial
import string
import pynmea2
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
BUZZ=18
red=3
green=4
gpio.setup(BUZZ,gpio.OUT)
gpio.setup(red,gpio.OUT)
gpio.setup(green,gpio.OUT)
port = "/dev/ttyUSB0" # the serial port to which the pi is connected.
 
#create a serial object
ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)
 
def gps():
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


def getPathLength(lat1,lng1,lat2,lng2):
    '''calculates the distance between two lat, long coordinate pairs'''
    R = 6371000 # radius of earth in m
    lat1rads = math.radians(lat1)
    lat2rads = math.radians(lat2)
    deltaLat = math.radians((lat2-lat1))
    deltaLng = math.radians((lng2-lng1))
    a = math.sin(deltaLat/2) * math.sin(deltaLat/2) + math.cos(lat1rads) * math.cos(lat2rads) * math.sin(deltaLng/2) * math.sin(deltaLng/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d

def getDestinationLatLong(lat,lng,azimuth,distance):
    '''returns the lat an long of destination point 
    given the start lat, long, aziuth, and distance'''
    R = 6378.1 #Radius of the Earth in km
    brng = math.radians(azimuth) #Bearing is degrees converted to radians.
    d = distance/1000 #Distance m converted to km
    lat1 = math.radians(lat) #Current dd lat point converted to radians
    lon1 = math.radians(lng) #Current dd long point converted to radians
    lat2 = math.asin(math.sin(lat1) * math.cos(d/R) + math.cos(lat1)* math.sin(d/R)* math.cos(brng))
    lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(d/R)* math.cos(lat1), math.cos(d/R)- math.sin(lat1)* math.sin(lat2))
    #convert back to degrees
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    return[lat2, lon2]

def calculateBearing(lat1,lng1,lat2,lng2):
    '''calculates the azimuth in degrees from start point to end point'''
    startLat = math.radians(lat1)
    startLong = math.radians(lng1)
    endLat = math.radians(lat2)
    endLong = math.radians(lng2)
    dLong = endLong - startLong
    dPhi = math.log(math.tan(endLat/2.0+math.pi/4.0)/math.tan(startLat/2.0+math.pi/4.0))
    if abs(dLong) > math.pi:
         if dLong > 0.0:
             dLong = -(2.0 * math.pi - dLong)
         else:
             dLong = (2.0 * math.pi + dLong)
    bearing = (math.degrees(math.atan2(dLong, dPhi)) + 360.0) % 360.0;
    return bearing

def main(interval,azimuth,lat1,lng1,lat2,lng2):
    '''returns every coordinate pair inbetween two coordinate 
    pairs given the desired interval'''

    d = getPathLength(lat1,lng1,lat2,lng2)
    remainder, dist = math.modf((d / interval))
    counter = float(interval)
    coords = []
    coords.append([lat1,lng1])
    for distance in range(0,int(dist)):
        coord = getDestinationLatLong(lat1,lng1,azimuth,counter)
        counter = counter + float(interval)
        coords.append(coord)
    coords.append([lat2,lng2])
    return coords

if __name__ == "__main__":
    #point interval in meters
    interval = 1
    #direction of line in degrees
    #start point
    lat1 = 17.385044
    lng1 = 78.486671
    #end point
    lat2 = 16.235001
    lng2 = 77.799698
    azimuth = calculateBearing(lat1,lng1,lat2,lng2)
    #print (azimuth)
    coords = main(interval,azimuth,lat1,lng1,lat2,lng2)
    final_dist_coords=[]
    #print coords
    for gps_data in coords:
            lat_gps_data='%.5f'%gps_data[0]
            lng_gps_data='%.5f'%gps_data[1]
            final_dist_coords.append([lat_gps_data,lng_gps_data])
    print final_dist_coords
                

while True:
    gpscoords=gps()
    try:
        if gpscoords!=None:
            lat_gpscoords='%.5f'%gpscoords[0]
            lng_gpscoords='%.5f'%gpscoords[1]
            final_gpscoords=[str(lat_gpscoords),str(lng_gpscoords)]
            print 'latitude: ',lat_gpscoords
            print 'longitude: ',lng_gpscoords
            time.sleep(0.5)
            if final_gpscoords in final_dist_coords:
                gpio.output(BUZZ,gpio.LOW)
                gpio.output(red,gpio.LOW)
                gpio.output(green,gpio.HIGH)
                print 'You are going perfect'
                time.sleep(0.5)
            else:
                gpio.output(BUZZ,gpio.HIGH)
                gpio.output(red,gpio.HIGH)
                gpio.output(green,gpio.LOW)
                print 'WARNING:WRONG DIRECTION'
                time.sleep(0.5)
    except:
        print 'The System Shutdown'
        break
                
            
            
    
