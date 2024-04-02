

import numpy as np
from psychopy import visual, core



class DriftingGratings:

    def __init__(self, stim_props):
        """
        
        Parameters
        ----------
        stim_props : dict
            Dictionary of stimulus properties.
        """

        self.orientations = stim_props['ori_list']
        self.spatial_freqs = stim_props['sf_list']
        self.temporal_freqs = stim_props['tf_list']
    
        self.doShuffle = stim_props['shuffle']
        self.num_repeats = stim_props['num_repeats']

        self.on_time = stim_props['on_time']
        self.off_time = stim_props['off_time']

        self.n_frames = len(self.orientations) * len(self.spatial_freqs) * len(self.temporal_freqs) * self.num_repeats

        np.random.seed(10)

        self.stim_stack = []
        self.stim_instructions = []
        self.stim_history = np.zeros([
            self.n_frames,
            3,  # orientation / spatial freq / temporal freq
            2   # start time / stop time
        ])

        self.win = visual.Window(
            [1360, 768],
            fullscr=False,
            units='pix',
            color=[0,0,0]
        )


    def scale_spatial_freq_to_monitor(self, sf_list):

        




        

    def make_stim_stack(self):

        self.spatial_freqs = self.scale_spatial_freq_to_monitor(self.spatial_freqs)

        self.stim_instructions = []

        for ori in self.orientations:
            for sf in self.spatial_freqs:
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

            _stim_obj = visual.GratingsStim(
                self.win,
                tex='sin',
                mask='gauss',
                ori=s['ori'],
                sf=s['sf'],
                tf=s['tf'],
                autoLog=False
            )

            self.stim_stack.append(_stim_obj)

        for i, instr in enumerate(self.stim_instructions):
            self.stim_history[i,0] = instr['ori']
            self.stim_history[i,1] = instr['sf']
            self.stim_history[i,2] = instr['tf']

        

    def show(self):

        clock = core.Clock()

        # Make sure the stimulus stack is ready
        if len(self.stim_stack) == 0:
            print('No generated stimulus to present.')

        for f_i, frame in enumerate(self.stim_stack):

            while clock.getTime() < self.on_time:

                if 


            



    def log_stim_instructions(self, savepath):

        _instr = np.array(self.stim_history)

        np.save(savepath, _instr)
