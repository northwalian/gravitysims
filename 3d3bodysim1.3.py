from __future__ import division
import numpy as np
import matplotlib.pyplot as pyplot
import mpl_toolkits.mplot3d.axes3d as p3
import math

"""First attempt at a working 3D plot. The updating version is weird as hell.

   v1.0: They all seem to be flying away from each other. Will test further.
   v1.1: They are definitely all flying away from each other.
         Maths must be wrong.
   v1.2: I buggered up the maths. That would explain it. Fixed it now, get expected motion in x-y plane.
   v1.3: Added some motion in the z-axis.

"""

m1 = 1.8982 * (10 ** 28) # I reserve the right to change these.
m2 = 3.9885 * (10 ** 28)
m3 = 7.4622 * (10 ** 28)
G = 6.67 * (10 ** -11)
dt = 51240 # These figures aren't arbitrary, I promise
n = 7305 # Number of timesteps

x1, y1, z1 = np.zeros(n), np.zeros(n), np.zeros(n)
x1[0] = -7.4052 * (10 ** 10) # All positions subject to change.
y1[0] = 2.5694 * (10 **10)

x2, y2, z2 = np.zeros(n), np.zeros(n), np.zeros(n)
x2[0] = 7.0687 * (10 ** 10)
z2[0] = 0.8033 * (10 ** 10)

x3, y3, z3 = np.zeros(n), np.zeros(n), np.zeros(n)
x3[0] = 1.9457 * (10 ** 10)
y3[0] = -6.5370 * (10 ** 10)
z3[0] = -0.3421 * (10 ** 10)

vx1 = 0 # Velocities also subject to change.
vy1 = 3.3712 * (10 ** 3)
vz1 = 0

vx2 = 1.2555 * (10 ** 3)
vy2 = - 1.3089 * (10 **4)
vz2 = 1.6421 * (10 ** 3)

vx3 = 0
vy3 = 0
vz3 = 0

ax1, ay1, az1 = 0, 0, 0

ax2, ay2, az2 = 0, 0, 0

ax3, ay3, az3 = 0, 0, 0

Fx12, Fy12, Fz12 = 0, 0, 0 # F12 = Force on m1 due to m2.

Fx23, Fy23, Fz23 = 0, 0, 0

Fx13, Fy13, Fz13 = 0, 0, 0

F12, F23, F13 = 0, 0, 0

theta12, theta23, theta13 = 0, 0, 0 #theta12 = angle associated with F12 in xy plane
phi12, phi23, phi13 = 0, 0, 0 #phi12 = zenith angle associated with F12 from +z axis

for i in range(n-1):
    
    x1[i+1] = x1[i] + vx1 * dt # Update positions based on last timestep's vel.
    y1[i+1] = y1[i] + vy1 * dt
    z1[i+1] = z1[i] + vz1 * dt

    x2[i+1] = x2[i] + vx2 * dt
    y2[i+1] = y2[i] + vy2 * dt
    z2[i+1] = z2[i] + vz2 * dt

    x3[i+1] = x3[i] + vx3 * dt
    y3[i+1] = y3[i] + vy3 * dt
    z3[i+1] = z3[i] + vz3 * dt

    F12 = G * m1 * m2 / ( (x1[i+1] - x2[i+1])**2 + (y1[i+1] - y2[i+1])**2 + (z1[i+1] - z2[i+1])**2)
    F23 = G * m3 * m2 / ( (x3[i+1] - x2[i+1])**2 + (y3[i+1] - y2[i+1])**2 + (z3[i+1] - z2[i+1])**2)
    F13 = G * m1 * m3 / ( (x1[i+1] - x3[i+1])**2 + (y1[i+1] - y3[i+1])**2 + (z1[i+1] - z3[i+1])**2)

    theta12 = np.arctan2(y2[i+1] - y1[i+1], x2[i+1] - x1[i+1])
    theta23 = np.arctan2(y3[i+1] - y2[i+1], x3[i+1] - x2[i+1])
    theta13 = np.arctan2(y3[i+1] - y1[i+1], x3[i+1] - x1[i+1])
    
    # zenith angle = arccos(z/r)
    phi12 = math.acos((z2[i+1]-z1[i+1]) / ( (x1[i+1] - x2[i+1])**2 + (y1[i+1] - y2[i+1])**2 + (z1[i+1] - z2[i+1])**2) ** 0.5)
    phi23 = math.acos((z3[i+1]-z2[i+1]) / ( (x3[i+1] - x2[i+1])**2 + (y3[i+1] - y2[i+1])**2 + (z3[i+1] - z2[i+1])**2) ** 0.5)
    phi13 = math.acos((z3[i+1]-z1[i+1]) / ( (x1[i+1] - x3[i+1])**2 + (y1[i+1] - y3[i+1])**2 + (z1[i+1] - z3[i+1])**2) ** 0.5)

    Fx12 = F12 * np.cos(theta12) * np.sin(phi12) # Resolving forces along components
    Fy12 = F12 * np.sin(theta12) * np.sin(phi12)
    Fz12 = F12 * np.cos(phi12)

    Fx23 = F23 * np.cos(theta23) * np.sin(phi23)
    Fy23 = F23 * np.sin(theta23) * np.sin(phi23)
    Fz23 = F23 * np.cos(phi23)

    Fx13 = F13 * np.cos(theta13) * np.sin(phi13)
    Fy13 = F13 * np.sin(theta13) * np.sin(phi13)
    Fz13 = F13 * np.cos(phi13)

    ax1 = (Fx12 + Fx13) / m1
    ay1 = (Fy12 + Fy13) / m1
    az1 = (Fz12 + Fz13) / m1

    ax2 = (Fx23 - Fx12) / m2 # Minus since Fx21 = - Fx12
    ay2 = (Fy23 - Fy12) / m2
    az2 = (Fz23 + Fz12) / m1

    ax3 = - (Fx13 + Fx23) / m3
    ay3 = - (Fy13 + Fy23) / m3
    az3 = - (Fz13 + Fz23) / m3

    vx1 = vx1 + ax1 * dt # Updating velocities based on current accel.
    vy1 = vy1 + ay1 * dt
    vz1 = vz1 + az1 * dt

    vx2 = vx2 + ax2 * dt
    vy2 = vy2 + ay2 * dt
    vz2 = vz2 + az2 * dt

    vx3 = vx3 + ax3 * dt
    vy3 = vy3 + ay3 * dt
    vz3 = vz3 + az3 * dt



fig = pyplot.figure()
ax = fig.add_subplot(111, projection = '3d')
mass1, = ax.plot(x1, y1, z1, label = 'm1')
mass2, = ax.plot(x2, y2, z2, label = 'm2')
mass3, = ax.plot(x3, y3, z3, label = 'm3')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

pyplot.legend(loc = 'upper left')
pyplot.show()
