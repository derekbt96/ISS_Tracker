import numpy as np
import matplotlib.pyplot as plt

import orbitTracker


log_file = 'ISS_Tracker/iss_positions_2hour.txt'
dat = np.genfromtxt(log_file,delimiter=',')
# plt.plot(dat[:,4], dat[:,3],'r')
plt.scatter(dat[:,4], dat[:,3])

ISS = orbitTracker.orbitTracker(vNeg = True)

start_idx = 0
ISS.calibrate(dat[start_idx,3],dat[start_idx,4],dat[start_idx,2],-1)
# ISS.calibrate(0,0,0,-1)
print(ISS.test)

lat_data = np.array([ISS.lat])
lon_data = np.array([ISS.lon])
tim_data = np.array([ISS.timestamp])
x_data = np.array(ISS.x)
v_data = np.array(ISS.v)


for k in range(200):
# for k in range(1000):
    ISS.propagate(100)
    lat_data = np.append(lat_data,ISS.lat)
    lon_data = np.append(lon_data,ISS.lon)
    tim_data = np.append(tim_data,ISS.timestamp)
    x_data = np.vstack((x_data,ISS.x))
    v_data = np.vstack((v_data,ISS.v))



plt.plot(lon_data, lat_data,'b')
# plt.scatter(lon_data, lat_data)
plt.title('Data Set 1')
plt.xlabel('Time')
plt.ylabel('Data')
plt.grid()
plt.ylim(-90,90)
plt.xlim(-180,180)

# ax = plt.figure().add_subplot(projection='3d')
# ax.plot(x_data[:,0], x_data[:,1], x_data[:,2])
# ax.quiver(x_data[:,0], x_data[:,1], x_data[:,2],
#           v_data[:,0], v_data[:,1], v_data[:,2], length=100, color='r')
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')

plt.show()