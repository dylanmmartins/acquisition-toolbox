# import acq
from psychopy import monitors

mon1 = monitors.Monitor(name='mon1',
                        width=24,
                        distance=20)

mon1.currentCalib['sizePix'] = (800,600)

print(mon1.getSizePix())