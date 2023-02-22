#allows you to modulate the frequency or amplitude of ad9910
from artiq.experiment import *
import numpy as np
from artiq.coredevice import ad9910

class DDS_Modulated(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("urukul0_ch0")
        self.setattr_device("cpld0")
        self.dds = self.urukul0_ch0
    
    def prepare(self):
        #what we want the quantity to be in actual numbers (for frequency) or relative to ASF (for amplitude)
        self.x  =[] #this list will be read backwards
        self.x_ram = [0] * len(self.x) #empty list that will end up carrying the above but translated into RAM profile data
    
    @kernel
    def init_dds(self, dds):
        #initializes the DDS and CPLD CFG RF switch state, sets attenuation
        self.core.break_realtime()
        dds.init()
        dds.sw.on()
        dds.set_att(6.*dB)
        dds.cfg_sw(True)
   
    @kernel
    def configure_ram_mode(self, dds):
        self.core.break_realtime()

        self.dds.set_cfr1(ram_enable=0) #must set ram_enable to 0 when writing RAM; cfr1 = Control Function Register 1
        self.cpld0.io_update.pulse_mu(8) #pulse the cpld to enact RAM changes
        self.cpld0.set_profile(0)  

        self.dds.set_profile_ram(start=0, end=len(self.asf_ram)-1,step=100, profile=0, mode=ad9910.RAM_MODE_CONT_RAMPUP) 
        #gives start and end adresses of where to look within the RAM
        #step length, i.e. how long to run each element of the list. 1 step = 4ns
        
        self.cpld0.io_update.pulse_mu(8) 
        
        #change the line below to self.frequency_to_ram or self.amplitude_to_ram
        self.dds.x_to_ram(self.x, self.x_ram) #converts the quantity we gave it into RAM profile data. Fill up the empty list we defined earlier
        self.dds.write_ram(self.x_ram) #writes this data into the RAM
        self.core.break_realtime()
        
        self.dds.set() #Input parameters in the order (frequency = , phase = , amplitude = ) 
        #for the constant parameter just put the number. For the changing parameter put ram_destination = ad9910.RAM_DEST_ASF (for amplitude modulation) or ad9910.RAM_DEST_FTW (for frequency modulation)

        #must set the control function register ram_enable to 1 to enable ram playback
        #self.dds.set_cfr1(ram_enable=1, ram_destination=RAM_DEST_ASF)   #for amplitude modulation
        self.dds.set_cfr1(internal_profile=0, ram_enable = 1, ram_destination=ad9910.RAM_DEST_FTW, manual_osk_external=0, osk_enable=1, select_auto_osk=0) #for frequency modulation
        
        self.cpld0.io_update.pulse_mu(8)

    
    @kernel
    def run(self):
        self.core.reset()
        self.core.break_realtime()
        self.cpld0.init()
        self.init_dds(self.urukul0_ch0) 
        self.configure_ram_mode(self.urukul0_ch0)

        