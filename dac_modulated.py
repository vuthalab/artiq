#ouput an increasing voltage on the DAC
from artiq.experiment import *                                

class DAC_Modulated(EnvExperiment):
    def build(self):
        self.setattr_device("core")                            
        self.setattr_device("zotino0")                         

    @kernel
    def run(self):
        self.core.reset()                                       
        voltages = [0.1,0.2,0.3,0.4,0.5] #write the actual voltages in volts
        
        self.core.break_realtime()
                                                                
        self.zotino0.init()                                    
        delay(1*ms)                                           

        while True:                                               
            for voltage in voltages:                        
                self.zotino0.write_dac(0, voltage)           
                self.zotino0.load()                            
                delay(1000*us) #the step time between each voltage                                                                             