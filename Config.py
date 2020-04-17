# Config.py
# configuration values for the tasim program.
# Change history:
#	20200408:KDT - Original issue.

import configparser as cp
import numpy as np
import re

class Config :
    def __init__(self) :
        # General
        self.Patm = 0.0                     # Atmosphereic pressure (Pa)
        self.Tamb = 0.0                     # Ambient temperature (degC)
        self.pco2Init = 0.0                 # Inital pco2 (Pa)
        self.rhInit = 0.0                   # Initial relative humidiy (percent)
        self.Flow = 0.0                     # Recirculating flow (ml/m)
        self.deltaT = 0.0                   # Simulation deltaT (sec)

        # Conditioning chamber
        self.VolCC = 0.0                    # Chamber volume (liter)
        self.TauTCC = 0.0                   # Chamber heater time constant (sec)
        
        # Sample chamber
        self.VolCC = 0.0                    # Chamber volume (liter)
        self.TauSC = 0.0                    # Chamber heater time constant (sec)

        # Dew Point Generator
        self.ResArea = 0.0                  # Exposed DPG area
        self.TauTDP = 0.0                   # DPG heater time constant (sec)

		# Sorbent parameters
        self.Vsorb = 0.0
        self.density = 0.0                  # Sorbent density						
        self.Capacity = 0.0                 # Capacity mole/liter
        self.COH = 1.0
        self.CHCO3 = 1.0
        self.CCO3 = 1.0
        self.CH2O = 1.0
        self.density = 0.0
        self.wgt = 0.0

        # EqConstants
        self.K1 = 0.0					    # Equilibrium constant OH + CO2 <> HCO3
        self.ka = 0.0					    # H2O Henry constant
        self.kC = 0.0					    # Vsorb/Vair ration
        self.kp = 0.0	    			    # K2 base
        self.p = 0.0                        # K2 power
     
        # Comment strip
        self.pattern = None


    # ReadConfig
    # Read and fill it the values listed above from a .ini file.
    def ReadConfig(self, fName) :
        cfg = cp.ConfigParser()
        cfg.read(fName)
        self.pattern = re.compile("[ \t]")
        sc = self.stripComment

        s = 'General'
        self.Patm = float(sc(cfg[s]['Patm']))
        self.Tamb = float(sc(cfg[s]['Tamb']))
        self.pco2Init = float(sc(cfg[s]['pco2Init']))
        self.rhInit = float(sc(cfg[s]['rhInit']))
        self.Flow = float(sc(cfg[s]['Flow']))
        self.deltaT = float(sc(cfg[s]['deltaT']))

        s = 'CC'
        self.VolCC = float(sc(cfg[s]['VolCC']))
        self.TauTCC = float(sc(cfg[s]['TauTCC']))
        
        # Sample chamber
        s = 'SC'
        self.VolSC = float(sc(cfg[s]['VolSC']))
        self.TauTSC = float(sc(cfg[s]['TauTSC']))

        # Dew Point Generator
        s = 'DPG'
        self.ResArea = float(sc(cfg[s]["ResArea"]))
        self.TauTDP = float(sc(cfg[s]['TauTDP']))

        # Sorbent
        s = 'Sorbent'
        self.Vsorb = float(sc(cfg[s]['Vsorb']))
        self.Capacity = float(sc(cfg[s]['Capacity']))
        self.COH = float(sc(cfg[s]['COH']))
        self.CHCO3 = float(sc(cfg[s]['CHCO3']))
        self.CCO3 = float(sc(cfg[s]['CCO3']))
        self.CH2O = float(sc(cfg[s]['CH2O']))
        self.density = float(sc(cfg[s]['density']))
        self.wgt = float(sc(cfg[s]['Weight']))

        # EqConstants
        s = 'EqConstants'
        self.K1 = float(sc(cfg[s]['K1']))
        self.ka = float(sc(cfg[s]['ka']))
        self.kp = float(sc(cfg[s]['kp']))
        self.p = float(sc(cfg[s]['p']))

    def stripComment(self, s) :
        m = self.pattern.search(s)
        if m :
            s = s[:m.span()[0]]
        return s



