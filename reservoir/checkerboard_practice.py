from psychopy import visual, core

win1 = visual.Window(
    size=[800,600],
    checkTiming=False,
    fullscr=False,
    screen=2,
    monitor='testMonitor'
    )

checkerboard = visual.GratingStim(win=win1,
                                  tex='sqrXsqr',
                                  units='pix',
                                  size=[800,600],
                                  sf=0.01)
                             
rev_s = 0.5 # reversals per second
clock = core.Clock()
t = 0

while t < 5:
    t = clock.getTime()
    checkerboard.draw()
    win1.flip()
    core.wait(1/rev_s)
    checkerboard.phase = (0.5, 0.0)
    checkerboard.draw()
    win1.flip()
    core.wait(1/rev_s)
    checkerboard.phase = (0.0, 0.0)

win1.close()