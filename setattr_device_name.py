from artiq.experiment import *

"""
We modified environment.py, giving us a new method, setattr_device_name which allows us to set a device as an attribute and name it at the same time.
It is defined

    def setattr_device_name(self, string_val, key):
        setattr(self, string_val, self.get_device(key))
        kernel_invariants = getattr(self, "kernel_invariants", set())
        self.kernel_invariants = kernel_invariants | {key}
        self.kernel_invariants = kernel_invariants | {string_val}

Which is only different from set_attr_device in the line setattr(self, string_val, self.get_device(key)).

The regular setattr_device forces the device name and attribute name to be the same thing. This method gives us more flexibility. See artiq_sequence_fixed_devices.py to see how this could be used.

"""

#In this script, we name "ttl4" "ttl5"; this might be useful if you want to rename devices as something important, not just a differnet number

class setattr_device_name(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device_name("ttl5", "ttl4") #(new name for the device, actual device name)


    @kernel
    def run(self):
        self.core.reset()
        self.ttl5.output()
        self.ttl5.on()
        delay(10*s)
        self.ttl5.off()