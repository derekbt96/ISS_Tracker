
import numpy as np 
import matplotlib
import matplotlib.pyplot as plt



log_file = 'ISS_Tracker/iss_positions.txt'

dat = np.genfromtxt(log_file,delimiter=',')
print(dat)
tim = (dat[:,1]-dat[0,1])/(1000.0)
lat = dat[:,3]
lon = dat[:,4]

phi = 180
simLon = np.arange(-180,180)
simLat = 51.6 * np.sin((np.pi/180.0)*(simLon + phi))
print(simLon)
plt.plot(lon, lat)
plt.scatter(lon, lat)
plt.plot(simLon*0.93, simLat)

plt.title('Data Set 1')
plt.xlabel('Time')
plt.ylabel('Data')
plt.grid()
plt.ylim(-90,90)
plt.xlim(-180,180)
plt.show()
