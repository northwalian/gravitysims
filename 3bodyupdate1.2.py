from __future__ import division
import numpy as np
import matplotlib.pyplot as pyplot
import matplotlib.animation as animation

"""First attempt at a 3-body sim that updates.
   I've gotten a 2-body sim to update, and I've gotten a 3-body sim to work.
   So there is literally no way this doesn't work.

   Fewer timesteps than the other 3-body sim so it shouldn't take forever to run

   v1.1: Just tidying the code a little bit
   v1.2: Tidying up a little more by tweaking how the axes work

"""

m1 = 1.8982 * (10 ** 28) # I reserve the right to change these.
m2 = 3.9885 * (10 ** 28)
m3 = 7.4622 * (10 ** 28)
G = 6.67 * (10 ** -11)
dt = 51240 # These figures aren't arbitrary, I promise
n = 7305 # Number of timesteps

x1, y1 = np.zeros(n), np.zeros(n)
x1[0] = -7.4052 * (10 ** 10) # All positions subject to change.
y1[0] = 2.5694 * (10 **10)

x2, y2 = np.zeros(n), np.zeros(n)
x2[0] = 7.0687 * (10 ** 10)

x3, y3 = np.zeros(n), np.zeros(n)
x3[0] = 1.9457 * (10 ** 10)
y3[0] = -6.5370 * (10 **10)

vx1 = 0 # Velocities also subject to change.
vy1 = 3.3712 * (10 ** 3)

vx2 = 1.2555 * (10 ** 3)
vy2 = - 1.3089 * (10 **4)

vx3 = 0
vy3 = 0

ax1, ay1 = 0, 0

ax2, ay2 = 0, 0

ax3, ay3 = 0, 0

Fx12, Fy12 = 0, 0 # F12 = Force on m1 due to m2.

Fx23, Fy23 = 0, 0

Fx13, Fy13 = 0, 0

F12, F23, F13 = 0, 0, 0

theta12, theta23, theta13 = 0, 0, 0 #Theta12 = Angle associated with F12.

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

"""This bit is all the weird 'getting a plot to update' stuff.
   I need new arrays because FuncAnimation won't accept arrays as arguments
   So I need a function that basically returns the arrays I already have
   And this is infinitely simpler than fixing the rest of the code.

   Axes may need tweaking."""


fig = pyplot.figure() # Make figure with axes that don't autoscale.
ax = pyplot.axes(xlim = (min(min(x1), min(x2), min(x3)), max(max(x1), max(x2), max(x3))), ylim = (min(min(y1), min(y2), min(y3)), max(max(y1), max(y2), max(y3))))

xOne, xTwo, xThree = [], [], [] # These arrays will just hold the same values as x1, x2 etc
yOne, yTwo, yThree = [], [], []

mass1, = ax.plot(xOne, yOne, label = 'm1') # Examples online are very insistent on the commas.
mass2, = ax.plot(xTwo, yTwo, label = 'm2') # Don't really know why.
mass3, = ax.plot(xThree, yThree, label = 'm3')

def anime(q): # q is just a dummy variable, and I've already used i and n
    xOne.append(x1[q]) # Appending here lets me stick my old arrays in 'anime'
    xTwo.append(x2[q])
    xThree.append(x3[q])
    yOne.append(y1[q])
    yTwo.append(y2[q])
    yThree.append(y3[q])

    mass1.set_data(xOne, yOne)
    mass2.set_data(xTwo, yTwo)
    mass3.set_data(xThree, yThree)

    return mass1, mass2, mass3

simulation = animation.FuncAnimation(fig, anime, frames = 7305, interval = 0, repeat = False, blit = True)

pyplot.legend(loc = 'upper left')
pyplot.show()
