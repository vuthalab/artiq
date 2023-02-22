#Demonstrates how to use the ADC. In order to save data and not just read it in the terminal, you will need to use the ARTIQ dashboard
from artiq.experiment import *
import numpy as np

class Sampler(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("sampler0")

    @kernel
    def run(self):
        self.core.reset()
        self.sampler0.init()
        self.sampler0.set_gain_mu(7,0) #sets the attenuation
        self.core.break_realtime()

        n_samples = 100
        self.set_dataset("sampler_test", np.full(n_samples, np.nan), archive = True)
        #fills a dataset "sampler_test"; broadcast = True means data is sent in real time

        data = [0.0] * 2 #creates an empty list of floating point numbers to be filled later; important: list must have even length
        self.core.break_realtime()


        for i in range(n_samples):
            self.sampler0.sample(data) #takes a set of samples and writes them into the list "data"
            print(data[1]) #prints the data in terminal
            self.mutate_dataset("sampler_test",i,data[1]) #writes the data into the ith spot in "sampler_test"
            delay(100*ms) #sets the delay, i.e. the sampling rate

