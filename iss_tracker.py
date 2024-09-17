
import urllib.request
import json  
import time
import matplotlib.pyplot as plt
import numpy as np

now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

for i in range(30):
    if 1:
        url = "http://api.open-notify.org/iss-now.json"
        response = urllib.request.urlopen(url)
        result = json.loads(response.read())
        
        # Extract the ISS location
        location = result["iss_position"]
        latstr = location['latitude']
        lonstr = location['longitude']
        timestamp = result['timestamp']
    else:
        latstr = '12.34'
        lonstr = '56.78'
        timestamp = 000

    # Output lon and lat to the terminal in the 
    # float format
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
    print("waiting 10 minutes, loop: ",i)
    time.sleep(5*60)

