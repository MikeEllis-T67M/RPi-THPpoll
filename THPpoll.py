import time
import sys
import requests
import traceback

import bme280    # Read the BME sensor

database   = 'http://192.168.16.1:8086/write?db=temperature'
sampleTime = 10

# Change the log location here
sensors = { 0x76: {'location':'outside', 'sublocn':'upstairs'},
            0x77: {'location':'office',  'sublocn':'room'},
            }

def main():
    while True:
        try:
            measurements  = ''
            for id, locn in sensors.items():
                temperature,pressure,humidity = bme280.readBME280All(addr=id)
                measurements += 'temperature,location={0},type={1} value={2}\n'.format(locn['location'], locn['sublocn'], temperature)
                measurements +=    'humidity,location={0},type={1} value={2}\n'.format(locn['location'], locn['sublocn'], humidity)
                measurements +=    'pressure,location={0},type={1} value={2}\n'.format(locn['location'], locn['sublocn'], pressure)

            #print('\nSending to {}\n{}'.format(database,measurements))
            response = requests.post(database, data=measurements)
            #print('HTTP:{0}'.format(response.status_code))   

            time.sleep(sampleTime)

        except Exception as e:
            track = traceback.format_exc()
            print("Unexpected error:", track)
            break
            
if __name__ == '__main__':
    main()
