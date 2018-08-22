from __future__ import division
import numpy as np
import matplotlib.pyplot as pyplot
import matplotlib.animation as animation

"""First attempt at a plot which shows time evolution of Jupiter-Sun system.
   I don't expect this to work.

   It works. I am actually a genius.
   Just one problem: it's real slow.
   Image updates ~5x/second. I have 7,000 timesteps. Help.
   Tidying up code won't help; all 'anime' does is read from arrays.
   Only plotting Jupiter's motion speeds things up by ~10%. Still real slow.

   Not sure where bottleneck is. CPU usage peaks at ~25%. RAM not an issue.
   Crackpot theory: Python doesn't natively support multicore CPUs
                    Pi 3B has a quad-core processor. 100%/4 = 25%
   So to speed up, I would need to figure out how to multiprocess (not likely!)

   Could split up xOne.append, xTwo.append etc. to separate cores
   Similarly split mass1.set_data, mass2.set_data

   But plotting is probably the bottleneck - no idea how you'd split that

   Achieved substantial speedup (~35 FPS) by setting blit = True.
   Still a little slow, but much more palatable now.
   Would be faster with a CPU with higher clock speed, I assume.

   One weird quirk: plot disappears if you zoom in after animation finishes.
   

"""

m1 = 1.8982 * (10 ** 27) # Jupiter mass
m2 = 1.9885 * (10 ** 30) # Sun mass
G = 6.67 * (10 ** -11)
dt = 51240 # Don't ask. It made sense at the time.
n = 7305 # Update for 1 Jovian yr

x1 = np.zeros(n)
x1[0] = -7.4052 * (10 ** 11) # Jupiter at perihelion
y1 = np.zeros(n)

x2 = np.zeros(n)
x2[0] = 7.0687 * (10 ** 8) # Sun at pericentre
y2 = np.zeros(n)

vx1 = 0
vy1 = 1.3712 * (10 ** 4) # Jupiter's velocity at perihelion

vx2 = 0
vy2 = - 13.089 # Sun's velocity at pericentre - calculated using momentum cons.

ax1 = 0
ay1 = 0

ax2 = 0
ay2 = 0

Fx1 = 0
Fy1 = 0

Fx2 = 0
Fy2 = 0

F = 0

theta = 0

for i in range(n-1):
    
    x1[i+1] = x1[i] + vx1 * dt # Update positions using last timestep's vel.
    y1[i+1] = y1[i] + vy1 * dt

    x2[i+1] = x2[i] + vx2 * dt
    y2[i+1] = y2[i] + vy2 * dt

    F = G * m1 * m2 / ( (x1[i+1] - x2[i+1])**2 + (y1[i+1] - y2[i+1])**2 )

    theta = np.arctan2(y2[i+1] - y1[i+1], x2[i+1] - x1[i+1])

    Fx1 = F * np.cos(theta) # Resolve force along components
    Fy1 = F * np.sin(theta)

    Fx2 = - Fx1
    Fy2 = - Fy1

    ax1 = Fx1 / m1
    ay1 = Fy1 / m1

    ax2 = Fx2 / m2
    ay2 = Fy2 / m2

    vx1 = vx1 + ax1 * dt # Updating velocities using this timestep's accel.
    vy1 = vy1 + ay1 * dt

    vx2 = vx2 + ax2 * dt
    vy2 = vy2 + ay2 * dt

"""This bit is all the weird 'getting a plot to update' stuff.
   I need new arrays because FuncAnimation won't accept arrays as arguments
   So I need a function that basically returns the arrays I already have
   And this is infinitely simpler than fixing the rest of the code."""


fig = pyplot.figure() # Make a figure first, with axes that don't autoscale
ax = pyplot.axes(xlim = (-1 * 10 ** 12, 1 * 10 ** 12), ylim = (-1 * 10 ** 12, 1 * 10 ** 12))

xOne = [] # These arrays will just hold the same values as x1, x2 etc
xTwo = []
yOne = []
yTwo = []

mass1, = ax.plot(xOne, yOne) # Examples online are very insistent on the commas.
mass2, = ax.plot(xTwo, yTwo) # Don't really know why.

def anime(q): # q is just a dummy variable, and I've already used i and n
    xOne.append(x1[q]) # Appending here lets me stick my old arrays in 'anime'
    xTwo.append(x2[q])
    yOne.append(y1[q])
    yTwo.append(y2[q])

    mass1.set_data(xOne, yOne)
    mass2.set_data(xTwo, yTwo)

    return mass1, mass2

simulation = animation.FuncAnimation(fig, anime, frames = 7305, interval = 0, repeat = False, blit = True)

pyplot.show()
