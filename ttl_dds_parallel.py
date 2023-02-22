from artiq.experiment import *

#An example of making TTL pulses and synthesizer waves work in parallel
class TTL_DDS_Parallel(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl8")
        self.setattr_device("urukul0_ch0")

    @kernel
    def run(self):
        self.core.reset()
        self.ttl8.output()
        self.urukul0_ch0.init()

        self.urukul0_ch0.set_att(6*dB)
        self.urukul0_ch0.set(4*MHz,0.0,1.0) #set the (frequence, phase, amplitude)

       #put the TTL control within one sequential block and the synthesizer control within another
       #the with parallel block will run these two control sequences at the same time

        for i in range(10000):
            with parallel:

                with sequential:
                    self.ttl8.on()
                    delay(2*ms)
                    self.ttl8.off()

                with sequential:
                    self.urukul0_ch0.sw.on()
                    delay(5*ms)
                    self.urukul0_ch0.sw.off()

            delay(5*ms) #delay between each period of TTL and DDS on in parallel
