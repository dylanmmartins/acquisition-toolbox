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
        
        np.random.seed(10)

        self.screen_id = screen_id

        self.stim_stack = []
        self.stim_instructions = []

        self.monitor_x = 800
        self.monitor_y = 600  # default, can be changed with set_monitor_pxls() below

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

    def set_monitor_pxls(self, monitor_x=800, monitor_y=600):

        self.monitor_x = monitor_x
        self.monitor_y = monitor_y

    def scale_spatial_freq_to_monitor(self):
        # Probably needs to be adjusted to new monitor

        # Convert cycles/pixel to cycles/deg
        # 77.9 pixels / 1 cm (for diagonal resolution of small monitors)
        # 1 cm / 4 deg (for monitor placed 14.3 cm away from viewer)

        self.sf_list = []
        for sf in self.spatial_freqs:
            self.sf_list.append(sf / (77.9 / 4))
        return self.sf_list

    def log_stim_presentation(self):

        if self.savepath is None:
            print('Select savepath for stimulus log file.')
            savepath = sg.popup_get_file('Save stimulus log file as:', save_as=True)

        if not savepath.endswith('.csv'):
            savepath = savepath + '.csv'

        column_headers = ['ori', 'sf', 'tf', 'onset', 'offset']
        header_string = ",".join(column_headers)    

        np.savetxt(savepath, self.stim_history, delimiter=',', header=header_string)

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
                size=[2*self.monitor_x, 2*self.monitor_y], # for ori
                units = 'pix',
                autoLog=False,
                autoDraw=False
            )

            self.stim_stack.append(_stim_obj)
        
        self.stim_stack_tf = []
        for stim in self.stim_instructions: # takes tf to apply in show()
            self.stim_stack_tf.append(stim["tf"])

        self.stim_history = np.empty([
            len(self.stim_instructions),
            5 # orientation / spatial freq / temporal freq
        ]) * np.nan

        for i, instr in enumerate(self.stim_instructions):
            self.stim_history[i,0] = instr['ori']
            self.stim_history[i,1] = instr['sf']
            self.stim_history[i,2] = instr['tf']
          # self.stim_history[i,3] = will log stimulus onset in show()
          # self.stim_history[i,4] = will log stimulus offset in show()

    def show(self):
        """
        Presents the stimulus stack. Creates a running clock first. Then, each
        element in self.stim_stack is drawn and its phase updated for < the
        specified self.on_time. This makes for drifting, with stim_stack_tf
        specifying Hz. The screen then switches to grey for the specified
        self.off_time.
        
        Stimulus onset is logged before the loop starts, stimulus offset is
        logged just before flipping to gray screen.

        5/7/2024: Logging does not seem entirely temporally precise, but maybe
        it is precise enough for our purposes for now.
        """

        if len(self.stim_stack) == 0:
            print('No generated stimulus to present.')
        
        else:
            history_clock = core.MonotonicClock() # to log stim on/off times
            
            for i, frame in enumerate(self.stim_stack):
                t = 0
                on_time = core.Clock()
                self.stim_history[i,3] = history_clock.getTime(applyZero=True)

                while t < self.on_time:
                    t = on_time.getTime()
                    self.stim_stack[i].phase = t * self.stim_stack_tf[i] # t*Hz
                    frame.draw()
                    self.win.flip()

                else:
                    self.stim_history[i,4] = history_clock.getTime(applyZero=True)
                    frame.clearTextures()
                    self.win.flip()
                    core.wait(self.off_time)

                on_time.reset()
            
            self.win.close()

        self.log_stim_presentation()