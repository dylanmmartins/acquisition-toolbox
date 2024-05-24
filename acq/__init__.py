from .utils.ttl import wait_for_trig

from .utils.camera import Camera

from .utils.stimuli import (
    BaseStimulus,
    DriftingGratings,
    Checkerboard
)

from .stim import (
    stim,
    stim_from_arg
)

# imports from previous structure
# from .utils.base_stimulus import BaseStimulus
# from .utils.gratings import DriftingGratings
# from .utils.base_stimulus import BaseStimulus # at some point want to import this