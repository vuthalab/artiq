from artiq.experiment import *
import numpy as np

"""
This code is written to allow you to control the ARTIQ from a different python script, which is useful if the ARTIQ is to be used in conjunction with other experiment control software / hardware. Set the parameters (timings of TTL pulses and amplitude, frequency, and phase of DDS) in the larger python script.

active_channels : a list of the channels to use, channels in quotes and using their proper names.
    ex. active_channels = ["ttl8", "ttl11", "urukul0_ch2", "urukul0_ch3"]

delay_array : np.array of the timings for the TTL channels in us. Each row should be the times for a channel. All rows must have the same length, so fill extra spots with zeroes

dds_parameters : np.array of the parameters for each DDS channel. Each row corresponds to one channel.
    Amplitude (float) relative to ASF, ex. 0.7
    Frequency (int) in kHz, ex. 5000
    Phase (float), ex. 0.5
    Attenuation (float) in dB, ex. 6.0
"""

#for testing purposes the following parameters were used
active_channels = ["ttl8", "ttl12", "urukul0_ch1", "urukul0_ch2"]
delay_array = np.array([[1,1,1,1],[2,2,2,2]])
dds_parameters = np.array([[1.0, 5000, 0.0, 6.], [1.0, 7000, 0.0, 6.]])


#creates lists of the TTL and DDS channels we will use to iterate through later
active_ttl = []
active_dds = []

for i in active_channels:
    if "ttl" in i:
        active_ttl.append(i)
    elif "urukul" in i:
        active_dds.append(i)

#translates the delay array into a list of lists. ARTIQ does not support slicing in two dimensions. You cannot look for position i,j in an array, but can look for position i,j in a list of lists
delay_lists = delay_array.tolist()

times_needed = [] #list of the amount of time each TTL channel will need to complete its part of the sequence; max of this is t_sequence
for i in range(len(delay_lists)):
    times_needed.append(sum(delay_lists[i]))

t_sequence = float(max(times_needed))


#translate DDS params into because ARTIQ does not support multi-dimensional slicing
dds_params = dds_parameters.tolist()


class Sequence(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        for i in active_channels:
            self.setattr_device(i)

        #Store the devices we are using in a list. This allows us to write self.ttls[0] to use the first TTL channel, whatever it may be
        self.ttls = [self.get_device(f'{i}') for i in active_ttl]
        self.dds = [self.get_device(f'{j}') for j in active_dds]

    @kernel
    def run(self):
        self.core.reset()

        #note: each for loop uses a different variable to iterate through
        #ARTIQ may get confused and throw an error if you try to iterate over the same variable in two different loops

        #set the TTLs to output mode
        for i in self.ttls:
            i.output()

        #intialize the DDS channels
        for j in self.dds:
            j.init()

        #set the parameters of the DDS channels, do this before they are turned on to avoid RTIO underflow
        for q in range(len(active_dds)):
            self.dds[q].set_att(dds_params[q][3] *dB)
            self.dds[q].set(dds_params[q][1]*kHz, dds_params[q][2], dds_params[q][0])

        #delay to prevent RTIO underflow
        delay(1.*s)

        #allows us to have all devices begin their part of the sequence at the same time
        t_begin = now_mu()
        t_end = t_begin + self.core.seconds_to_mu(t_sequence)

        #iterate through each TTL channel at t_begin, and have them execute their sequence of turning on and off
        for p in range(len(active_ttl)):
            at_mu(t_begin)
            r = 0
            while r < len(delay_lists[p]):
                delay(delay_lists[p][r]*us)
                self.ttls[p].pulse(delay_lists[p][r+1]*us)
                r += 2

        #iterate through the DDS channels, turning them on at the start of the sequence
        for b in range(len(active_dds)):
            at_mu(t_begin)
            self.dds[b].sw.on()

        #iterate through the DDS channels, turning them off at the end of the sequence
        for t in range(len(active_dds)):
            at_mu(t_end)
            self.dds[t].sw.off()

