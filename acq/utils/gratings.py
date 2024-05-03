

import numpy as np
import PySimpleGUI as sg
from psychopy import visual, core

sg.theme('Default1')


class DriftingGratings(): # at some point class DriftingGratings(acq.BaseStimulus):

    def __init__(self, stim_props, screen_id=2, savepath=None):
        """
        Parameters
        ----------
        stim_props : dict
            Dictionary of stimulus properties.
        """

        # acq.BaseStimulus.__init__(self, stim_props, screen_id, savepath)
        
        np.random.seed(10) # why is this here?

        self.screen_id = screen_id

        self.stim_stack = []
        self.stim_instructions = []

        self.monitor_x = 1360
        self.monitor_y = 768  # default, can be changed with set_monitor_pxls() below

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

        self.props = stim_props

        self.num_orientations = stim_props['num_orientations']
        self.orientations = np.linspace(0, 360, self.num_orientations, endpoint=False)
        self.spatial_freqs = stim_props['sf_list']
        self.temporal_freqs = stim_props['tf_list']
    
        self.doShuffle = stim_props['shuffle']
        self.num_repeats = stim_props['num_repeats']

        self.on_time = stim_props['on_time']
        self.off_time = stim_props['off_time']

        self.n_frames = len(self.orientations) * len(self.spatial_freqs) * len(self.temporal_freqs) * self.num_repeats
        
        self.stim_history = np.zeros([
            self.n_frames,
            3,  # orientation / spatial freq / temporal freq
            2   # start time / stop time
        ])

    def set_monitor_pxls(self, monitor_x=1360, monitor_y=768):

        self.monitor_x = monitor_x
        self.monitor_y = monitor_y

    def scale_spatial_freq_to_monitor(self):
        # Convert cycles/pixel to cycles/deg
        # 77.9 pixels / 1 cm (for diagonal resolution of small monitors)
        # 1 cm / 4 deg (for monitor placed 14.3 cm away from viewer)

        self.sf_list = []
        for sf in self.spatial_freqs:
            self.sf_list.append(sf / (77.9 / 4))
        return self.sf_list

    def log_stim_instructions(self):

        if self.savepath is None:
            print('Select savepath for stimulus log file.')
            savepath = sg.popup_get_file('Save stimulus log file as:', save_as=True)

        if not savepath.endswith('.csv'):
            savepath = savepath + '.csv'

        np.savetxt(savepath, self.stim_history, delimiter=',')

    def make_stim_stack(self):

        self.spatial_freqs = self.scale_spatial_freq_to_monitor()

        self.stim_instructions = []

        for ori in self.orientations:
            for sf in self.sf_list:
                for tf in self.temporal_freqs:
                    self.stim_instructions.append({
                        'ori': ori,
                        'sf': sf,
                        'tf': tf,
                    })

        if self.doShuffle is True:
            np.random.shuffle(self.stim_instructions)

        self.stim_stack = []

        for s in self.stim_instructions:

            _stim_obj = visual.GratingStim(
                self.win,
                tex='sin',
                ori=s['ori'],
                sf=s['sf'],
                # tf=s['tf'],        # not a possible argument for visual.GratingStim
                                     # (figure out how to move gratings later)
                size=[self.monitor_x, self.monitor_y],           # adjust stimulus size to monitor size
                units = 'pix',
                autoLog=False,
                autoDraw=False
            )

            self.stim_stack.append(_stim_obj)

        self.stim_history = np.empty([
            len(self.stim_instructions),
            5 # orientation / spatial freq / temporal freq
        ]) * np.nan

        for i, instr in enumerate(self.stim_instructions):
            self.stim_history[i,0] = instr['ori']
            self.stim_history[i,1] = instr['sf']
            self.stim_history[i,2] = instr['tf']

    def show(self):

        # Make sure the stimulus stack is ready
        if len(self.stim_stack) == 0:
            print('No generated stimulus to present.')
        

        # The following works but is not super temporally precise
        # (on and off intervals are not consistent throughout).

        else:
            clock = core.MonotonicClock()

            for i, frame in enumerate(self.stim_stack):
                # I think this is where the while statement for
                # moving gratings should go
                frame.draw()
                self.win.flip()
                self.stim_history[i,3] = clock.getTime(applyZero=True)
                core.wait(self.on_time)

                frame.clearTextures()
                self.win.flip()
                self.stim_history[i,4] = clock.getTime(applyZero=True)
                core.wait(self.off_time)
            
            self.win.close()


        # This one also works but is also not completely precise
        # (the on intervals are not consistent throughout).

        # else:
        #     clock = core.MonotonicClock()

        #     for i, frame in enumerate(self.stim_stack):
        #         self.stim_history[i,3] = round(
        #             clock.getTime(applyZero=True),
        #             ndigits=1
        #             )
        #         on_timer = core.CountdownTimer(self.on_time)
        #         while on_timer.getTime() > 0:
        #             frame.draw()
        #             self.win.flip()
                
        #         else:
        #             self.stim_history[i,4] = round(
        #                 clock.getTime(applyZero=True),
        #                 ndigits=1
        #                 )
        #             off_timer = core.CountdownTimer(self.off_time)
        #             while off_timer.getTime() > 0:
        #                 frame.clearTextures()
        #                 self.win.flip()
            
        #     self.win.close()


        self.log_stim_instructions() # AttributeError: 'DriftingGratings' object has no attribute 'savepath'

