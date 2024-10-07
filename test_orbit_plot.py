
import numpy as np
import matplotlib.pyplot as plt

import orbitTracker


ISS = orbitTracker.orbitTracker(vNeg = False)
ISS.calibrate(0,0,0)

ax = plt.figure().add_subplot(projection='3d')

r = ISS.alt
inclination = ISS.inclination
# theta = np.linspace(0,2*np.pi, 100)
# x = r * np.cos(theta)
# y = r * np.sin(theta)*np.cos(inclination)
# z = r * np.sin(theta)*np.sin(inclination)
# ax.plot(x, y, z, label='Orbit')


lat = np.linspace(-inclination,inclination, 100)
theta_calc = np.arcsin(np.sin(lat)/np.sin(inclination))
dx = -np.sin(theta_calc)
dy = np.cos(theta_calc)*np.cos(inclination)
dz = np.cos(theta_calc)*np.sin(inclination)
# ax.plot(dx, dy, dz)
ax.quiver(ISS.x[0], ISS.x[1], ISS.x[2], ISS.v[0], ISS.v[1], ISS.v[2], length=100)


ax.legend()

plt.show()