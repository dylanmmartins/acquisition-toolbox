# previously in acq.utils

import numpy as np
from psychopy import visual


class BaseStimulus():

    def __init__(self, screen_id=2, savepath=None):
        """
        All parameters that are shared between stimulus classes,
        and all methods that apply to all stimulus classes.
        """
        
        np.random.seed(10)

        self.screen_id = screen_id

        self.monitor_x = 800
        self.monitor_y = 600  # default

        self.win = visual.Window(
            [self.monitor_x, self.monitor_y],
            checkTiming=False,
            fullscr=True,
            units='pix',
            color=[0,0,0],
            screen=self.screen_id
        )

        self.set_monitor_pxls()

        self.savepath = savepath

    def set_monitor_pxls(self, monitor_x=800, monitor_y=600):

        self.monitor_x = monitor_x
        self.monitor_y = monitor_y