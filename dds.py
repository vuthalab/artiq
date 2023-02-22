#Simple DDS test, outputs a sine wave
from artiq.experiment import *
import numpy as np

class DDS(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("urukul0_ch2")

    @kernel
    def run(self):
        self.core.reset()
        self.urukul0_ch2.init()
        self.urukul0_ch2.set_att(6.*dB) #set the attenuation
        self.urukul0_ch2.set(80*MHz,0.0,1.0) # set the (frequency, phase, amplitude), amplitude relative to ASF

        self.urukul0_ch2.sw.on()
        delay(50*s) #sets the duration of the signal
        self.urukul0_ch2.sw.off()