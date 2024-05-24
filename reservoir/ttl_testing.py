import nidaqmx
import time

# with nidaqmx.Task() as task:
#     task.ao_channels.add_ao_voltage_chan("Dev1/ao1")

#     print("1 Channel 1 Sample Write: ")
#     print(task.write(2))
#     time.sleep(5)
#     task.write(0) # making sure no voltage sent to DAQ after task stops
#     task.stop()

with nidaqmx.Task() as task:
    task.ao_channels.add_ao_voltage_chan('Dev1/ao1',
                                         min_val=0,
                                         max_val=5)

    # run for 12 seconds, starting with V = 3
    end_time = time.time() + 12
    voltage = 3

    while time.time() < end_time:
        task.write(voltage, auto_start=True)
        time.sleep(3)
        voltage = 0 if voltage == 3 else 3 # if V = 3, flip to 0, and vice versa

    task.write(0)
    task.stop()