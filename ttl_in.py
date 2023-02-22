from artiq.experiment import *                  

#reads in voltages from a TTL port. Returns 0 if voltage is low, 1 if voltage is high
class TTL_Input(EnvExperiment):
    def build(self): 
        self.setattr_device("core")             
        self.setattr_device("ttl3")            
        
    @kernel 
    def run(self):                              
        self.core.reset()                      
        self.ttl3.input()                   
        self.core.break_realtime()              
        
        self.ttl3.sample_input()              
        input = self.ttl3.sample_get()          
        print(input)                        