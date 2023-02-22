from artiq.experiment import *

#runs multiple TTL channels in parallel
class TTL_Parallel(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl4")
        self.setattr_device("ttl15")

    @kernel
    def run(self):
        self.core.reset()
        self.ttl4.output()
        self.ttl15.output()
        for i in range(1000):
        	delay(2*ms)
        	with parallel:
        		self.ttl4.pulse(2*ms)
        		self.ttl15.pulse(2*ms)
