import numpy as np
import matplotlib.pyplot as plt




class orbitTracker():
    GM = 398602544600000.0
    
    def __init__(self,lat=0,lon=0,vNeg = False):
        alt = (6375 + 432) * 1000 # m
        self.inclination = 51.6 * np.pi/180.0
        self.r = alt * 1000
        # v = np.sqrt(GM/r)
        self.speed = 7652.303002166208
        # T = 2*np.pi*np.sqrt((r**3)/(GM))
        self.T = 5589.1203437532795

        self.timestamp = 0
        
        self.lat = lat
        self.lon = lon
        self.v = self.speed*np.array([np.cos(self.inclination),0,np.sin(self.inclination)])
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

    def toLatLon(self,v):
        lat = np.arcsin(v[2])*180.0/np.pi
        lon = np.arctan2(v[1],v[0])*180.0/np.pi
        return [lat,lon]

    def propagate(self,tim):

        rot = np.arcsin(max(-1,min(1, (np.pi/180.0)*self.lat/self.inclination )))
        # print("rot: ",rot)


        theta_prop = 2*np.pi*tim/self.T
        if self.v[2] > 0: 
            v_rot = np.array([np.sin(-rot),
                            np.cos(-rot)*-np.sin(self.inclination),
                            np.cos(self.inclination)])
        else:
            v_rot = np.array([np.sin(-rot),
                            -np.cos(-rot)*-np.sin(self.inclination),
                            np.cos(self.inclination)])
        # print("v_rot: ",v_rot)
        
        q_rot = np.array([np.cos(theta_prop/2),
                        np.sin(theta_prop/2)*v_rot[0],
                        np.sin(theta_prop/2)*v_rot[1],
                        np.sin(theta_prop/2)*v_rot[2]])
       
        pos = np.array([0,
                        np.cos((np.pi/180.0)*self.lat),
                        0,
                        np.sin((np.pi/180.0)*self.lat)])
        pos_rotated = self.point_rotation_by_quaternion(pos, q_rot)[1:]
        # print(pos_rotated)

        vel = np.append(0,np.cross(v_rot,pos[1:]))
        vel = vel*np.linalg.norm(vel)*self.speed
        self.v = self.point_rotation_by_quaternion(vel, q_rot)[1:]
        # print(self.v)

        location_new = self.toLatLon(pos_rotated)
        
        location_new[1] += self.lon

        location_new[1] -= 360*tim/86400

        if location_new[1] > 180:
            location_new[1] -= 360
        elif location_new[1] < -180:
            location_new[1] += 360

        self.lat = location_new[0]
        self.lon = location_new[1]
        self.timestamp += tim


ISS = orbitTracker()
ISS.calibrate(7.9938,64.4501,1726524904,False)

lat_data = np.array([ISS.lat])
lon_data = np.array([ISS.lon])
tim_data = np.array([ISS.timestamp])

for k in range(6):
    ISS.propagate(600)
    lat_data = np.append(lat_data,ISS.lat)
    lon_data = np.append(lon_data,ISS.lon)
    tim_data = np.append(tim_data,ISS.timestamp)
    

log_file = 'ISS_Tracker/iss_positions_1hour.txt'
dat = np.genfromtxt(log_file,delimiter=',')
lat_record = dat[:,3]
lon_record = dat[:,4]

plt.plot(lon_record, lat_record)
plt.scatter(lon_record, lat_record)


plt.plot(lon_data, lat_data)
plt.scatter(lon_data, lat_data)

plt.title('Data Set 1')
plt.xlabel('Time')
plt.ylabel('Data')
plt.grid()
plt.ylim(-90,90)
plt.xlim(-180,180)
plt.show()