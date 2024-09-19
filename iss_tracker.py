
import urllib.request
from urllib.error import HTTPError, URLError
import socket
import json  
import time
import matplotlib.pyplot as plt
import numpy as np

now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

for i in range(18):
    try:
        url = "http://api.open-notify.org/iss-now.json"
        response = urllib.request.urlopen(url, timeout=10)
        result = json.loads(response.read())
        
        # Extract the ISS location
        location = result["iss_position"]
        latstr = location['latitude']
        lonstr = location['longitude']
        timestamp = result['timestamp']
    except HTTPError as error:
        print('Data not retrieved because %s\nURL: %s', error, url)
    except URLError as error:
        if isinstance(error.reason, socket.timeout):
            print('socket timed out - URL %s', url)
        else:
            print('some other error happened')
    else:
        print('Access successful.')

        lat = float(latstr)
        lon = float(lonstr)
        print("Latitude: " + str(lat))
        print("Longitude: " + str(lon))




        file = open('ISS_Tracker/iss_positions_2hour.txt','a+')
        file.write(now)
        file.write(',')
        file.write(str(time.time()))
        file.write(',')
        file.write(str(timestamp))
        file.write(',')
        file.write(latstr)
        file.write(',')
        file.write(lonstr)
        file.write('\n')

        file.close()
        print("Waiting, loop #",i)
        time.sleep(5*60)

