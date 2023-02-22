from artiq.experiment import *
#sends simple pulses out of the TTL ports; this is done sequentially
#minimum pulse width = 5ns
class TTL_Output(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl12")
        self.setattr_device("ttl8")

    @kernel
    def run(self):
        self.core.reset()
        self.ttl12.output()
        self.ttl8.output()

        delay(2*ms) #delay to prevent RTIO underflow
        for i in range(1000):
            delay(3*us)
            self.ttl12.pulse(3*us)
            self.ttl8.pulse(2*us)


