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
        self.test = 0
        self.timestamp = 0
        
        self.lat = lat
        self.lon = lon
        self.x = self.alt*np.array([1,0,0])
        self.v = self.speed*np.array([0,np.cos(self.inclination),np.sin(self.inclination)])
        if vNeg:
            self.v[2] = -self.v[2]

    def calibrate(self,lat,lon,timestamp,velPos=1):
        self.lat = lat 
        self.lon = lon
        self.timestamp = timestamp

        self.x = self.alt*np.array([np.cos(lat*np.pi/180.0) * np.cos(lon*np.pi/180.0),
                                    np.cos(lat*np.pi/180.0) * np.sin(lon*np.pi/180.0),
                                    np.sin(lat*np.pi/180.0)])
        
        theta = np.arcsin(np.sin(velPos*lat*np.pi/180.0) / np.sin(self.inclination))
        
        v = self.speed * np.array([-np.sin(theta),
                                    np.cos(self.inclination) * np.cos(theta),
                                    np.sin(self.inclination) * np.cos(theta) * velPos])

        theta_update = lon*np.pi/180.0 - np.arctan(np.tan(theta) * np.cos(self.inclination))
        rot_lon = np.array([[np.cos(theta_update),-np.sin(theta_update),0],
                            [np.sin(theta_update),np.cos(theta_update),0],
                            [0,0,1]])
        self.test = theta
        self.v = np.matmul(rot_lon,v)

        

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

