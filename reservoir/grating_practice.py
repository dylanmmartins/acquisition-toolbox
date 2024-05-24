from psychopy import visual, core

win1 = visual.Window(size=[800,600],
                      checkTiming=False,
                      fullscr=False,
                      screen=3,
                      monitor='testMonitor'
                      )

grating = visual.GratingStim(win=win1, tex='sqr', units='pix',
                             size=[1200,1200],
                             sf=0.02, ori=0,
                             phase=(0.0,0.0))

# confusing ori * tf interaction:
# ori = 0:   left to right
# ori = 1:   left to right
# ori = 45:  left to right
# ori = 90:  down to up
# ori = 135: right to left
# ori = 180: right to left

drift_Hz = 1
clock = core.Clock()
t = 0

while t < 3:
    t = clock.getTime()
    grating.phase = t * drift_Hz
    grating.draw()
    win1.flip()

win1.close()