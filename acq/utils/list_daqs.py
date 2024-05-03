# see API: https://nidaqmx-python.readthedocs.io/en/latest/device.html#module-nidaqmx.system.device

from nidaqmx import system

# Create a system object
sys = system.System.local()

# Print information about each device
for device in sys.devices:
    print(f'Product Type: {device.product_type}')
    print(f'Device Name: {device.name}')
    print(f'Serial Number: {device.serial_num}')
    print(f'Analog Input Channels: {device.ai_physical_chans.channel_names}')
    print(f'Analog Output Channels: {device.ao_physical_chans.channel_names}')
    