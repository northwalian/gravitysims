from __future__ import division
import numpy as np
import matplotlib.pyplot as pyplot

"""First attempt at a 3-body sim.
   Need to add m3, x3, y3, vx3, vy3, ax3, ay3.
   Rename forces. F1 -> F12 (force on m1 due to m2). Also need F23, F13, etc.
   Calculate forces separately, then combine at the acceleration calculation.
   Rename theta -> theta12

   It works. It's super chaotic, very sensitive to initial pos/vel.
   Might need an updating figure to fully appreciate how system develops.
   

"""

m1 = 1.8982 * (10 ** 28) # I reserve the right to change these.
m2 = 3.9885 * (10 ** 28)
m3 = 7.4622 * (10 ** 28)
G = 6.67 * (10 ** -11)
dt = 10248 # These figures aren't arbitrary, I promise
n = 36525 # Number of timesteps

x1 = np.zeros(n)
x1[0] = -7.4052 * (10 ** 10) # All positions subject to change.
y1 = np.zeros(n)
y1[0] = 2.5694 * (10 **10)

x2 = np.zeros(n)
x2[0] = 7.0687 * (10 ** 10)
y2 = np.zeros(n)

x3 = np.zeros(n)
x3[0] = 1.9457 * (10 ** 10)
y3 = np.zeros(n)
y3[0] = -6.5370 * (10 **10)

vx1 = 0 # Velocities also subject to change.
vy1 = 3.3712 * (10 ** 3)

vx2 = 1.2555 * (10 ** 3)
vy2 = - 1.3089 * (10 **4)

vx3 = 0
vy3 = 0

ax1 = 0
ay1 = 0

ax2 = 0
ay2 = 0

ax3 = 0
ay3 = 0

Fx12 = 0 # Force on m1 due to m2.
Fy12 = 0

Fx23 = 0
Fy23 = 0

Fx13 = 0
Fy13 = 0

F12 = 0
F23 = 0
F13 = 0

theta12 = 0 # Angle associated with F12.
theta23 = 0
theta13 = 0

for i in range(n-1):
    
    x1[i+1] = x1[i] + vx1 * dt # Update positions based on last timestep's vel.
    y1[i+1] = y1[i] + vy1 * dt

    x2[i+1] = x2[i] + vx2 * dt
    y2[i+1] = y2[i] + vy2 * dt

    x3[i+1] = x3[i] + vx3 * dt
    y3[i+1] = y3[i] + vy3 * dt

    F12 = G * m1 * m2 / ( (x1[i+1] - x2[i+1])**2 + (y1[i+1] - y2[i+1])**2 )
    F23 = G * m3 * m2 / ( (x3[i+1] - x2[i+1])**2 + (y3[i+1] - y2[i+1])**2 )
    F13 = G * m1 * m3 / ( (x1[i+1] - x3[i+1])**2 + (y1[i+1] - y3[i+1])**2 )

    theta12 = np.arctan2(y2[i+1] - y1[i+1], x2[i+1] - x1[i+1])
    theta23 = np.arctan2(y3[i+1] - y2[i+1], x3[i+1] - x2[i+1])
    theta13 = np.arctan2(y3[i+1] - y1[i+1], x3[i+1] - x1[i+1])

    Fx12 = F12 * np.cos(theta12) # Resolving forces along components
    Fy12 = F12 * np.sin(theta12)

    Fx23 = F23 * np.cos(theta23)
    Fy23 = F23 * np.sin(theta23)

    Fx13 = F13 * np.cos(theta13)
    Fy13 = F13 * np.sin(theta13)

    ax1 = (Fx12 + Fx13) / m1
    ay1 = (Fy12 + Fy13) / m1

    ax2 = (Fx23 - Fx12) / m2 # Minus since Fx21 = - Fx12
    ay2 = (Fy23 - Fy12) / m2

    ax3 = - (Fx13 + Fx23) / m3
    ay3 = - (Fy13 + Fy23) / m3

    vx1 = vx1 + ax1 * dt # Updating velocities based on current accel.
    vy1 = vy1 + ay1 * dt

    vx2 = vx2 + ax2 * dt
    vy2 = vy2 + ay2 * dt

    vx3 = vx3 + ax3 * dt
    vy3 = vy3 + ay3 * dt



pyplot.figure()
pyplot.plot(x1, y1, label = 'm1')
pyplot.plot(x2, y2, label = 'm2')
pyplot.plot(x3, y3, label = 'm3')
pyplot.legend(loc = 'upper left')
pyplot.show()
