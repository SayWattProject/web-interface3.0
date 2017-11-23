"""
    Simple program structure
    
"""
import time, serial, requests, json
import datetime

base = 'http://13.92.90.127:8000'
network_id = 'local'
header = {}

serial_port_name = '/dev/cu.usbmodem1421'
ser = serial.Serial(serial_port_name, 9600, timeout=1)

delay = 1*5 # Delay in seconds

# Run once at the start
def setup():
    try:
        query = {
            'object-name': 'Arduino Temp Sensor'
        }
        endpoint = '/networks/'+network_id+'/objects/arduino-temp'
        response = requests.request('PUT', base + endpoint, params=query, headers=header, timeout=120 )
        resp = json.loads( response.text )
        if resp['object-code'] == 201:
            print('Create object arduino-temp: ok')
        else:
            print('Create object arduino-temp: error')
            print( response.text )
            
        query = {
            'stream-name': 'Temperature Stream',
            'points-type': 'f' # 'i', 'f', or 's'
        }
        endpoint = '/networks/'+network_id+'/objects/arduino-temp/streams/temp-stream'
        response = requests.request('PUT', base + endpoint, params=query, headers=header, timeout=120 )
        resp = json.loads( response.text )
        if resp['stream-code'] == 201:
            print('Create stream temp-stream: ok')
        else:
            print('Create stream temp-stream: error')
            print( response.text )
    except:
        print "Setup Error"

# Run continuously forever
def loop():
    # Check if something is in serial buffer 
    if ser.inWaiting() > 0:
        try:
            # Read entire line 
            # (until '\n')
            x = ser.readline()
            print "Received:", x
            query = {
                'points-value': float(x),
                'points-at': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            }
            endpoint = '/networks/'+network_id+'/objects/arduino-temp/streams/temp-stream/points'
            response = requests.request('POST', base + endpoint, params=query, headers=header, timeout=120 )
            resp = json.loads( response.text )
            if resp['points-code'] == 200:
                print( 'Update temp-stream points: ok')
            else:
                print( 'Update temp-stream points: error')
                print( response.text )
        except:
            print "Error"
    time.sleep(0.1)
    return

# Run continuously forever
# with a delay between calls
def delayed_loop():
    # Make GET request
    try:
        query = {'points-limit':1} # get most recent point
        endpoint = '/networks/'+network_id+'/objects/python-resp/streams/LED-stream/points'
        response = requests.request('GET', base + endpoint, params=query, headers=header, timeout=120 )
        resp = json.loads( response.text )
        ledBytes = bytes(str(resp['points'][0]['value']))
        # now write it to serial
        ser.write(ledBytes)
    except:
        print "Delayed loop error"

# Run once at the end
def close(): 
    try:
        print "Close Serial Port"
        ser.close() 
    except:
        print "Close Error"
    
# Program Structure    
def main():
    # Call setup function
    setup()
    # Set start time
    nextLoop = time.time()
    while(True):
        # Try loop()
        try:
            loop()
            if time.time() > nextLoop:
                # If next loop time has passed...
                nextLoop = time.time() + delay
                delayed_loop()
        except KeyboardInterrupt:
            # If user enters "Ctrl + C", break while loop
            break
        except:
            # Catch all errors
            print "Unexpected error."
    # Call close function
    close()

# Run the program
main()
