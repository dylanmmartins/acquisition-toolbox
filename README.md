# Acquisition toolbox

## Plans

[X] Play gratings stimulus, make sure it looks normal. Don’t worry about triggering, logging data, etc.
[X] - kind of. Timing is not consistent for some reason. Add timestamps for when each stimulus starts and stops. In self.stim_history, add float values to index 3 and 4 of axis 1. Want this done inside of the self.show() method
[X] Stimulus class needs to send a TTL signal output. Write this as a separate function (not part of the class). Add to the file ttl.py, it will use the package nidaqmx (https://nidaqmx-python.readthedocs.io/en/latest/)
[X] Test TTL triggering and make sure the output is being generated how we expect. Should square wave that raises from 0 V to 3.3V and then returns to 0 V or can stay at 3.3 V. Install DAQ software on your computer. Wire/code Arduino: flash button and buzzer when TTL received. // Note: Arduino flashes as expected, have not visualized square wave.
[] Now, make new stimuli:
    [X] Reversing checkerboard
    ([] Contrast-modulated white noise)
    [] Natural movie presentation (from an array we load in)
    [] “” for natural images
    [] Flashed sparse noise (dark and light spots)
[X] Now, rename DriftingGratings to BaseStimulus. Move all of the gratings-specific methods/attributes to a new class that inherits generic code from BaseStimulus
[] Test function to wait for TTL input (to be used by camera code) func wait_for_trig() in ttl.py
[] Camera class: make sure frames and timestamps get saved out as expected, start on trigger works. Also check that there isn’t a delay between TTL input received and first frame logged.

extra points:
[] Create a monitor calibration for psychopy (keeps saying 'monitor specification not found').
[] Write some kind of monitor calibration function that lets you enter monitor parameters (resolution, diagonal length, viewing distance etc.) and save them with a name. Monitor calibration should be accessible by BaseStimulus. Calibration name should become a parameter for stim() / stim_from_arg().
[] Make scale_spatial_freq_to_monitor() a method of BaseStimulus that is used and called upon presentation by all stimulus classes that have a spatial frequency parameter.
[] Create docstrings for all the functions.
[] Make sure all lines are <= 79 characters (PEP8).

smaller to-dos:
[X] make it close the window after finishing stimobj.show()
[X] self.savepath for DriftingGratings class
[X] make stimulus fill out whole screen, even when it is tilted
[X] make stimulus in gratings.py move (see your stim_practice.py file)
[X] make stimulus log start and stop times correctly
[X] make sure that when shuffle=True, the tfs are appropriately lined up with the ori*sf combinations
[X] add column headers to the saved log csv file
[] make num_repeats functional (not implemented yet) - will also require adding an extra column 'repeat' to the csv file