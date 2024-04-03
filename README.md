# Acquisition toolbox

## Plans

[] Play gratings stimulus, make sure it looks normal. Don’t worry about triggering, loging data, etc.
[] Add timestamps for when each stimulus starts and stops. In self.stim_history, add float values to index 3 and 4 of axis 1. Want this done inside of the self.show() method
[] Stimulus class needs to send a TTL signal output. Write this as a separate function (not part of the class). Add to the file ttl.py, it will use the package nidaqmx (https://nidaqmx-python.readthedocs.io/en/latest/)
[] Test TTL triggering and make sure the output is being generated how we expect. Should square wave that raises from 0 V to 3.3V and then returns to 0 V or can stay at 3.3 V. Install DAQ software on your computer. Wire/code Arduino: flash button and buzzer when TTL received.
[] Now, rename DriftingGratings to BaseStimulus. Move all of the gratings-specific methods/attributes to a new class that inherits generic code from BaseStimulus
[] Now, make a new stimuli:
    [] Reversing checkerboard
    [] Contrast-modulated white noise
    [] Natural movie presentation (from an array we load in)
    [] “” for natural images
    [] Flashed sparse noise (dark and light spots)
[] Test function to wait for TTL input (to be used by camera code) func wait_for_trig() in ttl.py
[] Camera class: make sure frames and timestamps get saved out as expected, start on trigger works. Also check that there isn’t a delay between TTL input received and first frame logged.

