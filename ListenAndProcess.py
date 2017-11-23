"""
    Simple program structure
    
"""
import time, serial, requests, json
import datetime

base = 'http://127.0.0.1:5000'
network_id = 'local'
header = {}

serial_port_name = '/dev/cu.usbmodem1421'
ser = serial.Serial(serial_port_name, 9600, timeout=1)

delay = 1*5# Delay in seconds

# Run once at the start
def setup():
    try:
        query = {
            'object-name': 'Python Response'
        }
        endpoint = '/networks/'+network_id+'/objects/python-resp'
        response = requests.request('PUT', base + endpoint, params=query, headers=header, timeout=120 )
        resp = json.loads( response.text )
        if resp['object-code'] == 201:
            print('Create object python-resp: ok')
        else:
            print('Create object python-resp: error')
            print( response.text )
            
        query = {
            'stream-name': 'LED Value stream',
            'points-type': 'i' # 'i', 'f', or 's'
        }
        endpoint = '/networks/'+network_id+'/objects/python-resp/streams/LED-stream'
        response = requests.request('PUT', base + endpoint, params=query, headers=header, timeout=120 )
        resp = json.loads( response.text )
        if resp['stream-code'] == 201:
            print('Create stream LED-stream: ok')
        else:
            print('Create stream LED-stream: error')
            print( response.text )
    except:
        print "Setup Error"

# Run continuously forever
def delayed_loop(oldUpdate):
    try:
        query = {}
        endpoint = '/networks/'+network_id+'/objects/arduino-temp/streams/temp-stream'
        response = requests.request('GET', base + endpoint, params=query, headers=header, timeout=120 )
        resp = json.loads( response.text )
        updated = resp['stream-details']['updated-at']
        newUpdate = datetime.datetime.strptime(updated, "%Y-%m-%dT%H:%M:%S.%fZ")
        if newUpdate > oldUpdate:
            # Points have been updated
            # Grab newest point
            temp = resp['points'][0]['value']
            # If temperature is high enough, turn LED on
            if temp >= 70:
                LEDval = 255
            else:
                LEDval = 0
            query = {
                'points-value': LEDval,
                'points-at': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            }
            endpoint = '/networks/'+network_id+'/objects/python-resp/streams/LED-stream/points'
            response = requests.request('POST', base + endpoint, params=query, headers=header, timeout=120 )
            resp = json.loads( response.text )
            if resp['points-code'] == 200:
                print( 'Update LED-stream points: ok')
            else:
                print( 'Update LED-stream points: error')
                print( response.text )
    except:
        print "Error"

    return newUpdate

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
    update_time = datetime.datetime(1,1,1) #Set initial date to be early
    while(True):
        # Try loop()
        try:
            # loop()
            if time.time() > nextLoop:
                # If next loop time has passed...
                nextLoop = time.time() + delay
                update_time = delayed_loop(update_time)
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
