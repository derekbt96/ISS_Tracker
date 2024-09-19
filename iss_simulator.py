import numpy as np
import matplotlib.pyplot as plt




class orbitTracker():
    GM = 398602544600000.0
    
    def __init__(self,lat=0,lon=0,vNeg = False):
        self.alt = (6375 + 432) * 1000.0 # m
        self.inclination = 51.6 * np.pi/180.0
        # v = np.sqrt(GM/r)
        self.speed = 7652.303002166208
        # T = 2*np.pi*np.sqrt((r**3)/(GM))
        self.T = 5589.1203437532795

        self.timestamp = 0
        
        self.lat = lat
        self.lon = lon
        self.x = self.alt*np.array([1,0,0])
        self.v = self.speed*np.array([0,np.cos(self.inclination),np.sin(self.inclination)])
        if vNeg:
            self.v[2] = -self.v[2]

    def calibrate(self,lat,lon,timestamp,velPos=True):
        self.lat = lat 
        self.lon = lon
        self.timestamp = timestamp
        if not velPos:
            self.v[2] = -1


    def update(self,w,a,dt):
        self.prediction(dt)
        self.correction(w,a,dt)

    def quaternion_mult(self,q,r):
        return [r[0]*q[0]-r[1]*q[1]-r[2]*q[2]-r[3]*q[3],
                r[0]*q[1]+r[1]*q[0]-r[2]*q[3]+r[3]*q[2],
                r[0]*q[2]+r[1]*q[3]+r[2]*q[0]-r[3]*q[1],
                r[0]*q[3]-r[1]*q[2]+r[2]*q[1]+r[3]*q[0]]

    def point_rotation_by_quaternion(self,r,q):
        q_conj = [q[0],-1*q[1],-1*q[2],-1*q[3]]
        return self.quaternion_mult(self.quaternion_mult(q,r),q_conj)

    def updateLatLon(self):
        self.lat = np.arcsin(self.x[2]/self.alt)*180.0/np.pi
        self.lon = np.arctan2(self.x[1],self.x[0])*180.0/np.pi
        if self.lon > 180:
            self.lon -= 360
        elif self.lon < -180:
            self.lon += 360

    def propagate(self,tim):

        theta_prop = 2*np.pi*tim/self.T

        v_rot = np.cross(self.x,self.v)
        v_rot = v_rot/np.linalg.norm(v_rot)
        
        q_rot = np.array([np.cos(theta_prop/2),
                        np.sin(theta_prop/2)*v_rot[0],
                        np.sin(theta_prop/2)*v_rot[1],
                        np.sin(theta_prop/2)*v_rot[2]])
        
        pos = np.append(0,self.x)
        pos = self.point_rotation_by_quaternion(pos, q_rot)[1:]

        vel = np.append(0,self.v)
        vel = self.point_rotation_by_quaternion(vel, q_rot)[1:]

        theta_day = -2*np.pi*tim/86400

        rot_lon = np.array([[np.cos(theta_day),-np.sin(theta_day),0],
                            [np.sin(theta_day),np.cos(theta_day),0],
                            [0,0,1]])
        
        self.x = np.matmul(rot_lon,pos)
        self.v = np.matmul(rot_lon,vel)

        self.updateLatLon()
        self.timestamp += tim



ISS = orbitTracker(vNeg = True)

# log_file = 'ISS_Tracker/iss_positions_3.txt'
# dat = np.genfromtxt(log_file,delimiter=',')
# plt.plot(dat[:,4], dat[:,3],'r')
# plt.scatter(dat[:,4], dat[:,3])

log_file = 'ISS_Tracker/iss_positions_2hour.txt'
dat = np.genfromtxt(log_file,delimiter=',')
plt.plot(dat[:,4], dat[:,3],'r')
plt.scatter(dat[:,4], dat[:,3])

# log_file = 'ISS_Tracker/iss_positions_1hour.txt'
# dat = np.genfromtxt(log_file,delimiter=',')
# plt.plot(dat[:,4], dat[:,3],'r')
# plt.scatter(dat[:,4], dat[:,3])

# log_file = 'ISS_Tracker/iss_positions.txt'
# dat = np.genfromtxt(log_file,delimiter=',')
# plt.plot(dat[:,4], dat[:,3],'r')
# plt.scatter(dat[:,4], dat[:,3])

# ISS.calibrate(lat_record[0],lon_record[0],dat[0,2],True)

lat_data = np.array([ISS.lat])
lon_data = np.array([ISS.lon])
tim_data = np.array([ISS.timestamp])
x_data = np.array(ISS.x[0])

for k in range(446*2):
# for k in range(50):
    ISS.propagate(100)
    lat_data = np.append(lat_data,ISS.lat)
    lon_data = np.append(lon_data,ISS.lon)
    tim_data = np.append(tim_data,ISS.timestamp)
    x_data = np.append(x_data,ISS.x[0])




plt.plot(lon_data, lat_data,'b')
# plt.scatter(lon_data, lat_data,'b')

plt.title('Data Set 1')
plt.xlabel('Time')
plt.ylabel('Data')
plt.grid()
plt.ylim(-90,90)
plt.xlim(-180,180)
plt.show()