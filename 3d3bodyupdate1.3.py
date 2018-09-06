from __future__ import division
import numpy as np
import matplotlib.pyplot as pyplot
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3
import math

"""First attempt at a 3-body, 3D sim that updates.
   I've gotten a 2D sim to work.
   Issues:
          1) Need to add third coordinate for pos, vel, accel, force component
          2) Need to add new angles phi for the xz plane
          3) Modify force components in the usual spherical-polar way

   Code needed a serious revamp for 3D plotting.

   v1.2: Success! Just don't really understand how to rotate the plot.
         Or how to get the plot not to disappear if you try to manipulate it after animation finishes
   v1.3: Tidying up the axes a little bit.

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

    # zenith angle = arccos(z/r). Yes, I know it's very long and I'm sorry.
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

"""This bit is all the weird 'getting a plot to update' stuff.
   I need new arrays because FuncAnimation won't accept arrays as arguments
   So I need a function that basically returns the arrays I already have
   And this is infinitely simpler than fixing the rest of the code.

   Axes may need tweaking."""


fig = pyplot.figure()
ax = fig.add_subplot(111, projection = '3d')

xOne, xTwo, xThree = [], [], [] # These arrays will just hold the same values as x1, x2 etc
yOne, yTwo, yThree = [], [], []
zOne, zTwo, zThree = [], [], []

mass1, = ax.plot(xOne, yOne, zOne, label = 'm1') # Examples online are very insistent on the commas.
mass2, = ax.plot(xTwo, yTwo, zTwo, label = 'm2') # Don't really know why.
mass3, = ax.plot(xThree, yThree, zThree, label = 'm3')

def anime(q): # q is just a dummy variable, and I've already used i and n
    xOne.append(x1[q]) # Appending here lets me stick my old arrays in 'anime'
    xTwo.append(x2[q])
    xThree.append(x3[q])
    yOne.append(y1[q])
    yTwo.append(y2[q])
    yThree.append(y3[q])
    zOne.append(z1[q])
    zTwo.append(z2[q])
    zThree.append(z3[q])

    mass1.set_data(xOne, yOne) # set_data only seems to accept two arguments
    mass1.set_3d_properties(zOne) # need this thing to add the third dimension
    mass2.set_data(xTwo, yTwo)
    mass2.set_3d_properties(zTwo)
    mass3.set_data(xThree, yThree)
    mass3.set_3d_properties(zThree)

    return mass1, mass2, mass3

ax.set_xlim3d([min(min(x1), min(x2), min(x3)), max(max(x1), max(x2), max(x3))])
ax.set_xlabel('x')

ax.set_ylim3d([min(min(y1), min(y2), min(y3)), max(max(y1), max(y2), max(y3))])
ax.set_ylabel('y')

ax.set_zlim3d([min(min(z1), min(z2), min(z3)), max(max(z1), max(z2), max(z3))])
ax.set_zlabel('z')

simulation = animation.FuncAnimation(fig, anime, frames = 7305, interval = 0, repeat = False, blit = True)

pyplot.legend(loc = 'upper left')
pyplot.show()
