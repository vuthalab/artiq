from artiq.experiment import *
import numpy as np

"""
This is an alternative way to achieve the artiq_sequence.py for a fixed number of devices. This script is written for 2 TTL channels and 1 DDS channel.
This code has never been run. It is a better idea to use the artiq_sequence.py script, although this code demonstrates a use of renaming devices.
"""

active_channels = ["ttl8", "ttl12", "urukul0_ch1"]
dds_parameters = np.array([[1.0, 5000, 0.0, 6.]])
delay_matrix = np.matrix('1 1 1 1 ; 2 2 2 2')

active_ttl = []

for i in active_channels:
    if "ttl" in i:
        active_ttl.append(i)
timing = dict(zip(active_ttl, np.transpose(delay_matrix).tolist()))

t_start = np.min(delay_matrix, axis = 1)[0].item()
t_begin = self.core.seconds_to_mu(t_start)

t_seq = np.sum(delay_matrix, axis = 0).max()
t_sequence = self.core.seconds_to_mu(t_seq)

#translate DDS params into because ARTIQ does not support multi-dimensional slicing
dds_params = dds_parameters.tolist()


class Sequence(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        for i in range(len(active_channels)):
            self.setattr_device_name(f"dev{i}", i) #now we have that self.dev0 = self.ttli if ttli is the first element of active_channels
            #this is valuable because we can, for instance, change ttl4 to ttl5 and not have to change any code

    @kernel
    def run(self): #assume we have the 3 devices, 2 TTL and one DDS
        self.core.reset()
        self.dev1.output()
        self.dev2.output()
        self.dev3.init()

        i_1 = 0
        i_2 = 0

        at_mu(t_begin)
        with parallel:
            with sequential: #what device 1 should be doing (TTL)
               while i_1 < len(timing[dev1]):
                    delay(timing[dev1][i_1])
                    self.dev1.pulse(timing[dev1][i_1+1])

                    i_1 += 2

            with sequential: #what device 2 should be doing (TTL)
               while i_2 < len(timing[dev2]):
                    delay(timing[dev2][i_2])
                    self.dev2.pulse(timing[dev2][i_2+1])

                    i_2 += 2

            with sequential: #what device 3 should be doing (DDS)
                self.dev3.set_att(dds_params[1][3])
                self.dev3.set(dds_params[1][2], dds_params[1][3], dds_params[1][1])
                self.dev3.sw.on()
                delay(t_sequence)
                self.dev3.sw.off()