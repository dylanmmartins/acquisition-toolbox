import acq
import numpy as np
import PySimpleGUI as sg
from psychopy import visual, core, monitors

sg.theme('Default1')

class BaseStimulus():

    def __init__(self, screen_id, savepath=None):
        """
        All parameters that are shared between stimulus classes,
        and all methods that apply to all stimulus classes.
        """
        
        np.random.seed(10)

        # self.monitor = monitor # this will be an argument for __init__ I think

        self.screen_id = screen_id

        self.monitor_x = 800
        self.monitor_y = 600  # default

        self.mon = monitors.Monitor(name='mon1',
                                    width=24,
                                    distance=40)
        self.mon.currentCalib['sizePix'] = (800,600)

        self.win = visual.Window(
            [self.monitor_x, self.monitor_y],
            checkTiming=False,
            fullscr=True,
            units='deg',
            color=[0,0,0],
            monitor = self.mon, # will be populated by calibrated monitor arg in stim.py 
            screen=self.screen_id
        )

        self.set_monitor_pxls()

        self.savepath = savepath

    def set_monitor_pxls(self, monitor_x=800, monitor_y=600):

        self.monitor_x = monitor_x
        self.monitor_y = monitor_y

class DriftingGratings(BaseStimulus):

    def __init__(self, screen_id):
        """
        All attributes and methods specific to drifting gratings.
        Inherits all attributes and methods from BaseStimulus.
        """

        super().__init__(screen_id)

        self.props = {
            'num_orientations': 3,
            'sf_list': [0.5], # [0.01, 0.02, 0.04],
            'tf_list': [0.5, 2], # temporal frequency in Hz
            'shuffle': False,
            'num_repeats': 1,
            'on_time': 2,
            'off_time': 0.5
        }

        self.orientations = np.linspace(0, 360, self.props['num_orientations'], endpoint=False)

    def scale_spatial_freq_to_monitor(self):
        # Will become redundant once psychopy monitor calibration is implemented
        # 
        # Convert cycles/pixel to cycles/deg
        # 77.9 pixels / 1 cm (for diagonal resolution of small monitors)
        # 1 cm / 4 deg (for monitor placed 14.3 cm away from viewer)

        self.sf_list = []
        for sf in self.props['sf_list']:
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

        self.sf_list = self.scale_spatial_freq_to_monitor()

        self.stim_instructions = []

        for ori in self.orientations:
            for sf in self.sf_list:
                for tf in self.props['tf_list']:
                    self.stim_instructions.append({
                        'ori': ori,
                        'sf': sf,
                        'tf': tf
                    })

        if self.props['shuffle'] is True:
            np.random.shuffle(self.stim_instructions)

        self.stim_stack = []

        for s in self.stim_instructions:

            _stim_obj = visual.GratingStim(
                self.win,
                tex='sin',
                units = 'deg',
                size=[2*self.monitor_x, 2*self.monitor_y], # for ori
                ori=s['ori'],
                sf=s['sf']
            )

            self.stim_stack.append(_stim_obj)
        
        # Here we create a new list of tf's from the (shuffled or not)
        # stim_instructions. Necessary to be able to apply them to show().
        # (Visual.GratingStim does not have a tf parameter.)

        self.stim_stack_tf = []
        for s in self.stim_instructions:
            self.stim_stack_tf.append(s['tf'])

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
        specified self.props['on_time']. This makes for drifting, with stim_stack_tf
        specifying Hz. The screen then switches to grey for the specified
        self.off_time.
        
        Stimulus onset is logged before the loop starts, stimulus offset is
        logged just before flipping to gray screen.

        5/7/2024: Logging does not seem entirely temporally precise, but maybe
        it is precise enough for our purposes for now.
        """

        if len(self.stim_stack) == 0:
            print('Stim stack is empty.')
        
        else:
            history_clock = core.MonotonicClock() # to log stim on/off times
            
            for i, frame in enumerate(self.stim_stack):
                t = 0
                on_time = core.Clock()
                self.stim_history[i,3] = history_clock.getTime(applyZero=True)

                while t < self.props['on_time']:
                    t = on_time.getTime()
                    self.stim_stack[i].phase = t * self.stim_stack_tf[i] # t*Hz
                    frame.draw()
                    self.win.flip()

                else:
                    self.stim_history[i,4] = history_clock.getTime(applyZero=True)
                    frame.clearTextures()
                    self.win.flip()
                    core.wait(self.props['off_time'])

                on_time.reset()
            
            self.win.close()

        self.log_stim_presentation()

class Checkerboard(BaseStimulus):

    def __init__(self, screen_id):
        """
        All attributes and methods specific to checkerboard stimuli.
        Inherits all attributes and methods from BaseStimulus.
        """

        super().__init__(screen_id)

        self.props = {
            'sf_list': [1],
            'tf_list': [2], # reversals per sec
            'shuffle': True,
            'num_repeats': 1,
            'on_time': 4,
            'off_time': 1
        }

    def log_stim_presentation(self):
        if self.savepath is None:
            print('Select savepath for stimulus log file.')
            savepath = sg.popup_get_file('Save stimulus log file as:', save_as=True)

        if not savepath.endswith('.csv'):
            savepath = savepath + '.csv'

        column_headers = ['sf', 'tf', 'onset', 'offset']
        header_string = ",".join(column_headers)    

        np.savetxt(savepath, self.stim_history, delimiter=',', header=header_string)

    def make_stim_stack(self):
        # at some point apply scale_spatial_freq_to_monitor here (from BaseStimulus?)
        self.stim_instructions = []

        for sf in self.props['sf_list']:
            for tf in self.props['tf_list']:
                self.stim_instructions.append({
                    'sf': sf,
                    'tf': tf
                })

        if self.props['shuffle'] is True:
            np.random.shuffle(self.stim_instructions)

        self.stim_stack = []

        for s in self.stim_instructions:
            _stim_obj = visual.GratingStim(
                self.win,
                tex='sqrXsqr',
                units='deg',
                size=[self.monitor_x, self.monitor_y],
                sf=s['sf']
            )

            self.stim_stack.append(_stim_obj)
        
        # Here we create a new list of tf's from the (shuffled or not)
        # stim_instructions. Necessary to be able to apply them to show().
        # (Visual.GratingStim does not have a tf parameter.)

        self.stim_stack_tf = []
        for s in self.stim_instructions:
            self.stim_stack_tf.append(s['tf'])
        
        self.stim_history = np.empty([
            len(self.stim_instructions),
            4 # spatial freq / temporal freq / start time / stop time
        ]) * np.nan

        for i, instr in enumerate(self.stim_instructions):
            self.stim_history[i,0] = instr['sf']
            self.stim_history[i,1] = instr['tf']
          # self.stim_history[i,2] = will log stimulus onset in show()
          # self.stim_history[i,3] = will log stimulus offset in show()

    def show(self):

        if len(self.stim_stack) == 0:
            print('Stim stack is empty.')
        
        else:
            history_clock = core.MonotonicClock() # to log stim on/off times
            
            for i, frame in enumerate(self.stim_stack):
                t = 0
                on_time = core.Clock()

                while t < self.props['on_time']:
                    t = on_time.getTime()
                    self.stim_history[i,2] = history_clock.getTime(applyZero=True)
                    frame.draw()
                    self.win.flip()
                    core.wait(1/self.stim_stack_tf[i])
                    frame.phase = (0.5, 0.0)
                    frame.draw()
                    self.win.flip()
                    core.wait(1/self.stim_stack_tf[i])
                    frame.phase = (0.0, 0.0)
            
                else:
                    self.stim_history[i,3] = history_clock.getTime(applyZero=True)
                    frame.clearTextures()
                    self.win.flip()
                    core.wait(self.props['off_time'])
                
                on_time.reset()

            self.win.close()

        self.log_stim_presentation()