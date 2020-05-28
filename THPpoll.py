import time
import sys
import requests

sys.path_append('/home/pi/THPpoll')

import bme280    # Read the BME sensor

database   = 'http://192.168.16.1:8086/write?db=temperature'
sampleTime = 10

# Change the log location here
location   = 'outside'
sublocn    = 'upstairs'

def main():
    while True:
        try:
            temperature,pressure,humidity = bme280.readBME280All()
            measurements  = ''
            measurements += 'temperature,location={0},type={1} value={2}\n'.format(location, sublocn, temperature)
            measurements += 'humidity,location={0},type={1} value={2}\n'.format(location, sublocn, humidity)
            measurements += 'pressure,location={0},type={1} value={2}\n'.format(location, sublocn, pressure)

            #print('\nSending to {}\n{}'.format(database,measurements))
            response = requests.post(database, data=measurements)
            #print('HTTP:{0}'.format(response.status_code))   

            time.sleep(sampleTime)

        except Exception as e:
            print("Unexpected error:", sys.exc_info()[0])
            break
            
if __name__ == '__main__':
    main()
