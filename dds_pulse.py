#sends sine wave pulses out of the synthesizer. Send a wave at one frequency. Turn off. Send a wave at a different frequency.
from artiq.experiment import *
import numpy as np

class DDS_Pulse(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("urukul0_ch0")

    @kernel
    def run(self):
        self.core.reset()
        self.urukul0_ch0.init()
        self.urukul0_ch0.set_att(6*dB) #set the attenuation


        for i in range(1000):
            self.urukul0_ch0.sw.on()
            self.urukul0_ch0.set(80*MHz,0.0,1.0) #sets the (frequency, phase, amplitude)
            delay(100*us) #the delay is the duration of the signal
            self.urukul0_ch0.sw.off()

            delay(100*us) #delay, how long the DDS should be off for

            self.urukul0_ch0.sw.on()
            self.urukul0_ch0.set(90*MHz,0.0,1.0) #sets the (frequency, phase, amplitude)
            delay(100*us) #the delay is the duration of the signal
            self.urukul0_ch0.sw.off()