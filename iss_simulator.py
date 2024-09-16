import numpy as np


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

def point_rotation_by_quaternion(point,q):
    r = [0]+point
    q_conj = [q[0],-1*q[1],-1*q[2],-1*q[3]]
    return quaternion_mult(quaternion_mult(q,r),q_conj)[1:]

def propagate(lat,lon,tim,velNeg):
    inclination = 51.6 * np.pi /  180.0 # deg
    rot = np.arcsin(max(-1,min((np.pi/180.0)*lat/inclination,1))) + np.pi*velNeg
    theta_prop = 2*np.pi*tim/86400
    q_rot = np.quaternion([np.cos(theta_prop/2),
                       np.sin(theta_prop/2)*np.sin(rot),
                       np.sin(theta_prop/2)*np.cos(rot)*np.sin(inclination),
                       np.sin(theta_prop/2)*np.cos(inclination)])
    print(q_rot)

    x = np.sin((np.pi/180.0)*lat)
    y = 0
    z = np.sin((np.pi/180.0)*lat)

    vecsq_rotated = q_rot * vecsq * q_rot.conjugate()

    
    


propagate(12.34,56.78,3600,0)

