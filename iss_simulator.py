import numpy as np
import matplotlib.pyplot as plt

alt = (6375 + 432) * 1000 # m
inclination = 51.6 # deg
# speed = 7651 # m/s
# G = 6.6743*(10**(-11))
# M = 5.9722*(10**24)
GM = 398602544600000.0
r = alt * 1000
# v = np.sqrt(GM/r)
v = 7652.303002166208
# T = 2*np.pi*np.sqrt((r**3)/(GM))
T = 5589.1203437532795

def quaternion_mult(q,r):
    return [r[0]*q[0]-r[1]*q[1]-r[2]*q[2]-r[3]*q[3],
            r[0]*q[1]+r[1]*q[0]-r[2]*q[3]+r[3]*q[2],
            r[0]*q[2]+r[1]*q[3]+r[2]*q[0]-r[3]*q[1],
            r[0]*q[3]-r[1]*q[2]+r[2]*q[1]+r[3]*q[0]]

def point_rotation_by_quaternion(r,q):
    q_conj = [q[0],-1*q[1],-1*q[2],-1*q[3]]
    return quaternion_mult(quaternion_mult(q,r),q_conj)

def toLatLon(v):
    lat = np.arcsin(v[2])*180.0/np.pi
    lon = np.arctan2(v[1],v[0])*180.0/np.pi
    return [lat,lon]  

def propagate(lat,lon,tim,velNeg):
    inclination = 51.6 * np.pi /  180.0 # deg
    rot = np.arcsin(max(-1,min((np.pi/180.0)*lat/inclination,1))) + np.pi*velNeg
    theta_prop = 2*np.pi*tim/86400
    # print(theta_prop)
    v_rot = np.array([np.sin(rot),
                      np.cos(rot)*np.sin(inclination),
                      np.cos(inclination)])
    # print(v_rot)
    q_rot = np.array([np.cos(theta_prop/2),
                      np.sin(theta_prop/2)*v_rot[0],
                      np.sin(theta_prop/2)*v_rot[1],
                      np.sin(theta_prop/2)*v_rot[2]])
    # print(q_rot)

    vecsq = np.array([0,
                      np.cos((np.pi/180.0)*lat),
                      0,
                      np.sin((np.pi/180.0)*lat)])
    # print(vecsq)

    vecsq_rotated = point_rotation_by_quaternion(vecsq, q_rot)[1:]
    # print(vecsq_rotated)

    return toLatLon(vecsq_rotated)
 
    

lat = 0.0
lon = 0.0
lat_data = np.array([lat])
lon_data = np.array([lon])

for k in range(30):
    [lat,lon] = propagate(lat,lon,3600,1)
    lat_data = np.append(lat_data,lat)
    lon_data = np.append(lon_data,lon)

print(lat_data)
print(lon_data)
plt.plot(lon_data, lat_data)
plt.scatter(lon_data, lat_data)

plt.title('Data Set 1')
plt.xlabel('Time')
plt.ylabel('Data')
plt.grid()
plt.ylim(-90,90)
plt.xlim(-180,180)
plt.show()