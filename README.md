
# ARTIQ (Advanced Real-Time Infrastructure for Quantum physics)

## Useful Resources
- Manual: https://m-labs.hk/artiq/manual/
- Forum: https://forum.m-labs.hk/
- Device Datasheets: https://m-labs.hk/experiment-control/sinara-core/
- ARTIQ GitHub: https://github.com/m-labs/artiq
- Birmingham: https://github.com/cnourshargh/Bham-ARTIQ-examples 
(Repository of basic ARTIQ code from the University of Birmingham. Much of our testing code is based upon Birmingham's code)

## Our System
- Operating System: Ubuntu 18.04.6
- FPGA: Sinara 1124 Carrier "Kasli"
- TTL: 2x Sinara 2128 (SMA) 8-Channel isolated TTL cards
- DDS: 1x Sinara 4410 (AD9910), 1x Sinara 4412 (AD9912)
- ADC: Sinara 5108 Sampler
- DAC: Sinara 5432 DAC "Zotino"
- ARTIQ: Release-7

## Installing ARITQ
The manual recommends that you use the ARTIQ on Linux and using the Nix virtual environment. We have found Nix to be rather complicated, and that Conda works fine. To install the virtual environment, first make sure you have Conda installed, then, in terminal, run
```console
conda config --prepend channels https://conda.m-labs.hk/artiq
conda config --append channels conda-forge
conda create -n artiq7 artiq
```

For our system, we had to navigate to ~/anaconda3/envs/artiq7/lib/python3.10/site-packages/artiq/coredevice/core.py and on line 75 change `rv32g` to `rv32ima`. This fixed the error "artiq.coredevice.comm_kernel.LoadError: cannot load kernel: parse error: not a shared library for current architecture". 

To activate the environment, in terminal run `conda activate artiq7`. To deactivate run `conda deactivate`. The ARTIQ came with IP address 192.168.1.75, and this can be changed with `artiq_coremgmt -D 192.168.1.75 config write -s ip [new ip]`. You must reboot the ARTIQ (unplug and replug) for this to take effect.

## ARITQ Overview
When you download ARTIQ you are downloading multiple things:
1. The ARTIQ Language, in /artiq/language/core.py and /artiq/language/environment.py
2. The ARTIQ Devices, in /artiq/coredevice
3. ARTIQ Master and Dashboard

We found this ARTIQ folder in ~/anaconda3/envs/artiq7/lib/python3.10/site-packages. 

The ARTIQ Language is the device-unspecific functionality of the ARTIQ. It includes the classes that our experiments will inherit from as well as the basic commands we can use (for example, run(), build(), and with parallel). 

The ARTIQ Devices are all of the header files for the devices we have on the ARTIQ. This is all of the low level code that communicates with the device. The device's header file is the best place to see what you can do with a device. Along with the devices is a device database, a file called device\_db<span>.py. You need to make this file, which lists the IP address of the core device and all of the details of each device. An example of this can be found at ~/artiq/examples/kasli. Use this file, altering what you need to set up your device.

ARTIQ Master and Dashboard is the GUI that M-Labs designed. If you would like to use it, do the following:
1. Create a folder ~/artiq-master. Within it, put the device\_db.py as well as a /repository subfolder. Save your script to ~/artiq-master/repository. 
2. In one terminal window, run `cd ~/artiq-master` and `artiq_master`. 
3. In a second terminal window, run `cd ~` and `artiq_dashboard`. 

The dashboard should appear. We encountered the error, "artiq.dashboard.moninj: failed to connect to moning. Is aqctl\_moning_proxy running?". This was fixed by running artiq\_ctlmgr in a seperate terminal window. In the dashboard you should see a list of all of your experiments in the Explorer tab. Note that the names you see in this tab are the names of the classes, not the file names. So, if you have a file named abc<span>.py but in the file you have "class xyz(EnvExperiment)", xyz will be in the Explorer tab. From here you can select a file, click submit to run, and your data will be saved within ~/artiq-master. 

We do not use the dashboard. Our code is meant to integrate with other python scripts and is executed using `artiq_run`. 

The outline of a basic ARTIQ program is as follows: 
```Python
from artiq.experiment import * #imports the artiq language and devices

class Name(EnvExperiment): #creates your sequence, named "Name"
	def build(self):
		self.setattr_device("core") #sets the core as an attribute
		self.setattr_device(device) #sets the device we're using as an attribute

	@kernel
	def run(self):
		self.core.reset(): #reset the device, importantly this resets the clock
		self.device.init() #initialize the device you wish to use; This command will vary depending on the device

```
Then, within the `run` method, after initializing your device, you can specify what you wish the device to do. To see a simple example of how this might look, see dds<span>.py, ttl_out.py, or dac<span>.py.

## Miscellaneous Facts
1. The modes (input and output) of the TTLs are set on the boards. To change them, you must take out the board, locate the switch, and flip it. The TTLs are set in blocks of four. 
2. AD9910 is capable of amplitude and frequency modulation (independently and at the same time). AD9912 cannot do either. You can use a simple form of modulation (i.e. a loop where you iterate through amplitude / frequency values) if the step size is large enough. If you want the steps between amplitudes or frequencies to be small you must write the data to RAM beforehand. 

## File Directory
Below is the list of files we wrote to test the ARTIQ and learn how to use it:
1) ttl_out.py sends pulses out of the TTLs
2) ttl_in.py reads in voltages from the TTLs
3) dds<span>.py sends a simple sine wave out of the DDS
4) dds_pulse.py sends a signal out of the DDS, turns it off, and turns it back on
5) dds_modulated.py code to modulate (using RAM), the amplitude and/or frequency of the AD9910
6) dac<span>.py sends a voltage out of the DAC
7) dac_modulted.py ramps the voltage out of the DAC. Note this has a slow step time as the DAC has no RAM
8) parallel_ttl.py an example of running the TTLs in parallel
9) ttl\_dds\_parallel<span>.py an example of running the TTLs and DDS in parallel
10) sampler<span>.py an example of taking data using the ADC (requires us to use the Dashboard)
11) set\_attr\_device\_name.py an example of how we may rename a device
12) artiq_sequence.py a generic script that allows us to use as many TTL and DDS channels as we want on some predetermined parameters
13) artiq\_sequence\_fixed_devices.py an alternative to artiq\_sequence.py for a fixed number of devices (never tested, you should just use artiq\_sequence.py)

