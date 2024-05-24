from psychopy import visual, core
import psychopy_visionscience # for NoiseStim
import numpy as np

# https://psychopy.github.io/psychopy-visionscience/coder/NoiseStim/#psychopy_visionscience.noise.NoiseStim.setNoiseFilterLower
# https://pythonnumericalmethods.studentorg.berkeley.edu/notebooks/chapter24.01-The-Basics-of-waves.html

win1 = visual.Window(
    size=[800,600],
    checkTiming=False,
    fullscr=False,
    screen=3,
    monitor='testMonitor'
    )

noise = visual.NoiseStim(
    win=win1,
    units='pix',
    noiseType='White',
    size=[1024,1024] # requires square powers of two
)

Hz = 0.5 # contrast cycles [-1;1] per second
clock = core.Clock()
t = 0

while t < 10:
    t = clock.getTime()
    sine = np.sin(2 * np.pi * Hz * t)
    noise.contrast = sine
    noise.draw()
    win1.flip()

win1.close()