from artiq.experiment import *
import artiq.coredevice.ad9910 as ad9910
#outputs a constant voltage to the DAC

class DAC(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("zotino0")

    @kernel
    def run(self):
        self.core.reset()
        self.core.break_realtime()
        self.zotino0.init()
        delay(1*ms)
        #self.zotino0.set_leds(0b11111110) #sets the color of the leds on the DAC; useful for error testing. 1 = on; 0 = off
        self.zotino0.write_dac(0,0) #specifies (chanel, voltage) to write to the DAC
        delay(1*ms)
        self.zotino0.load() #Sends the signal out