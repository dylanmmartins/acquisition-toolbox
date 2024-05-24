
import time
import numpy as np
import nidaqmx
from nidaqmx import stream_readers

nidaq_reader: stream_readers.AnalogMultiChannelReader = None

# https://stackoverflow.com/questions/73419239/ni-daqmx-how-to-start-collecting-signals-when-the-amplitude-of-the-wave-crosse

def callback_fn(task_handle, every_n_samples_event_type, pretrigger_samples, callback_data):
    try:

        data = np.empty(pretrigger_samples)
        
        # Read the acquired samples
        number_of_samples_read = nidaq_reader.read_many_sample(data, pretrigger_samples)

    except Exception as e:
        print(f'Something went wrong reading samples: {e}')

    else:
        return 0

    finally:
        # Always needed by nidaqmx to return 0
        print('Did not receve input in the allotted wait time... ending scan.')
        quit()


def wait_for_trig(dev_num=0, input_line=0):
      
    sampleRate = 2e5   # Sample rate in Hz
    secsToAcquire = 60    # Number of seconds over which to acquire data
    numberOfSamples = int(secsToAcquire * sampleRate)
    
    pretrigger_samples = 10000

    with nidaqmx.Task('hardwareFiniteVoltage') as task:
        
        task.ai_channels.add_ai_voltage_chan(
            'Dev{}/ai{}'.format(dev_num, input_line)\
        )

        task.timing.cfg_samp_clk_timing(
            sampleRate,
            sample_mode=nidaqmx.constants.AcquisitionType(10178),
            samps_per_chan=numberOfSamples
        )
        
        task.triggers.reference_trigger.cfg_anlg_edge_ref_trig(
            'Dev{}/ai{}'.format(dev_num, input_line),
            pretrigger_samples,
            trigger_level=0.1
        )
        
        # Here you register your callback into nidaqmx event loop
        task.register_every_n_samples_acquired_into_buffer_event(numberOfSamples, callback_fn)
        
        # Initialize the stream_readers nidaq_reader to be used by your callback to get your actual data
        #  global nidaq_reader
        nidaq_reader = stream_readers.AnalogSingleChannelReader(task.in_stream)
                                
        task.start()

def send_trig():
    pass