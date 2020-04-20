# TAModel.py
# Defines the TaModel and supporting classes.
#
# Change history:
#	20200408:KDT - Original.

from math import exp
import numpy as np 

# p2oSat
# Return the saturation ph2o for the temperature argument.
# Temperature units are degC.
# Note that this is at the module level, so others can use it.
def ph2oSat(T) :
	return 610.78 * exp((T * 17.2684) / (T + 238.3)) #T in C

# TaData
# Defines the data that is stored on each cycle for debug purposes.
class TaData :
	def __init__(self, count, Tcc, ph2oCC, pco2CC, Tsc, ph2oSC, pco2SC, Tdp, ph2oDP, pco2DP, wgt) :
		self.count = count
		self.Tcc = Tcc
		self.ph2oCC= ph2oCC
		self.pco2CC = pco2CC
		self.Tsc = Tsc
		self.ph2oSC = ph2oSC
		self.pco2SC = pco2SC
		self.Tdp = Tdp
		self.ph2oDP = ph2oDP
		self.pco2DP = pco2DP
		self.Wgt = wgt

# DPG
# Dew point generator model.  The DPG generator sets the pH2Osat at the DPG,
# The circulating flow exposes the air in the CC (and SC when not bypassed) to that
# that water vapor, and the whole system reaches equilibrium.  The evaporation (and
# condensation) is modeled using the method described in "The Engineering Toolbox"
# (https://wwww.engineeringtoolbox.com/evaporation-water-surface-d_690.html).
class DPG :
	def __init__(self, cfg) :
		self.cfg = cfg
		self.TDP = cfg.Tamb
		self.TDPprev = cfg.Tamb
		self.TauTDP = cfg.TauTDP
		self.TDPfactor = exp(-cfg.deltaT/cfg.TauTDP)
		self.TDPset = cfg.Tamb
		self.ph2oDP = ph2oSat(self.TDP)
		self.pco2DP = cfg.pco2Init
		self.ph2oFLprev = self.ph2oDP

	# cycle
	# Update the TDP, ph2oDP, and return the updated ph2oFL.
	def cycle(self, args) :
		TFL = args[0]
		ph2oFL = args[1]
		pco2FL = args[2]

		# Update
		self.TDP = self.TDPset + (self.TDP - self.TDPset) * self.TDPfactor
		self.ph2oDP = ph2oSat(self.TDP)
		ph2oMax = ph2oSat(TFL)
		if ph2oFL < ph2oMax :
			ph2oFL = self.ph2oDP + (ph2oFL - self.ph2oDP) * self.TDPfactor
		rVals = [TFL, ph2oFL, pco2FL, self.TDP]
		return rVals

# CC - Conditioning Chamber
class CC() :
	def __init__(self, cfg) :
		self.cfg = cfg
		self.TCC = cfg.Tamb
		self.TCCprev = cfg.Tamb
		self.TCCset = cfg.Tamb
		self.TCCfactor = exp(-cfg.deltaT/cfg.TauTCC)
		self.ph2oCC = ph2oSat(self.TCC) * self.cfg.rhInit / 100
		self.ph2oCCprev = self.ph2oCC
		self.pco2CC = cfg.pco2Init
		self.pco2CCprev = self.pco2CC
		self.DV = cfg.deltaT * cfg.Flow / 60	# ml
		self.volInj = 0.0						# Injected amounts
		self.pco2Inj = 0.0

	# cycle
	# Update values for a cycle
	def cycle(self, args) :
		TFL = args[0]
		ph2oFL = args[1]
		pco2FL = args[2]

		# Update the temperature
		self.TCCprev = self.TCC
		self.TCC = self.TCCset + (self.TCCprev - self.TCCset) * self.TCCfactor
		dTCCFL = self.DV * (TFL - self.TCCprev) / self.cfg.VolCC
		self.TCC += dTCCFL

		# Update the pco2CC
		self.pco2CCprev = self.pco2CC
		dpco2FL = self.DV * (pco2FL - self.pco2CCprev) / self.cfg.VolCC
		dpco2Inj = 0.0
		if not self.volInj == 0 :
			dpco2Inj = \
				(self.volInj * self.pco2Inj + self.pco2CCprev * self.cfg.VolCC) / self.cfg.VolCC
			self.VolInj = 0.0
			self.pco2Inj = 0.0
		self.pco2CC = self.pco2CCprev + dpco2FL + dpco2Inj

		# Update the ph2oCC
		# self.ph2oCC = self.ph2oCCprev
		dph2oFL = self.DV * (ph2oFL - self.ph2oCC) / self.cfg.VolCC
		self.ph2oCC = self.ph2oCC + dph2oFL

		# Done return the previous values
		return (self.TCC, self.ph2oCC, self.pco2CC)

# SC - Sample Chamber
class SC :
	def __init__(self, cfg) :
		self.cfg = cfg
		self.TSC = cfg.Tamb
		self.TSCprev = cfg.Tamb
		self.TSCset = cfg.Tamb
		self.TSCfactor = exp(-cfg.deltaT/cfg.TauTSC)
		self.ph2oSC = ph2oSat(self.TSC) * self.cfg.rhInit / 100
		self.ph2oSCprev = self.ph2oSC
		self.pco2SC = cfg.pco2Init
		self.pco2SCprev = self.pco2SC
		self.DV = cfg.deltaT * cfg.Flow	 / 60		# ml
		self.bBypass = False

	def cycle(self, args) :
		TFL = args[0]
		ph2oFL = args[1]
		pco2FL = args[2]

		# Check for bypass, and update if not
		if not self.bBypass :
			# Update the temperature
			self.TSCprev = self.TSC
			self.TSC = self.TSCset + (self.TSCprev - self.TSCset) * self.TSCfactor
			dTSCFL = self.DV * (TFL - self.TSCprev) / self.cfg.VolSC
			self.TSC += dTSCFL

			# Update the pco2SC
			self.pco2SCprev = self.pco2SC
			dpco2FL = self.DV * (pco2FL - self.pco2SC) / self.cfg.VolSC
			self.pco2SC = self.pco2SC + dpco2FL

			# Update the ph2oSC
			# self.ph2oSC = self.ph2oSCprev
			dph2oFL = self.DV * (ph2oFL - self.ph2oSC) / self.cfg.VolSC
			self.ph2oSC = self.ph2oSC + dph2oFL
			rVals = [self.TSC, self.ph2oSC, self.pco2SC]
		else :
			rVals = args

		return rVals

# Scale
# Placeholder, can't do any updates until the sorbent model is created and 
# integrated
class Scale :
	def __init__(self, cfg) :
		self.cfg = cfg
		self.wgt = self.cfg.wgt				# Init from cfg

# TaModel
class TaModel :
	def __init__(self, cfg) :
		self.cfg = cfg
		self.cc = CC(cfg)
		self.sc = SC(cfg)
		self.dpg = DPG(cfg)
		self.scale = Scale(cfg)
		self.count = 0
		self.idx = 0
		self.bufSize = int(60 / cfg.deltaT)
		self.data = np.zeros(self.bufSize, dtype=object, order='C')
		dRec = \
			TaData(self.count, self.cc.TCC, self.cc.ph2oCC, self.cc.pco2CC, \
					self.sc.TSC, self.sc.ph2oSC, self.sc.pco2SC, \
					self.dpg.TDP, self.dpg.ph2oDP, self.dpg.pco2DP, self.scale.wgt)
		self.data[self.idx] = dRec
		print(f'Count: {self.count} T: {self.count * self.cfg.deltaT} ph2o: {self.data[self.idx].ph2oSC}')

	def cycle(self) :
		dRec = self.data[self.idx]				# Last record stored
		args = [dRec.Tdp, dRec.ph2oDP, dRec.pco2DP]
		rValsCC = self.cc.cycle(args)			# Cycle cc
		rValsSC = self.sc.cycle(rValsCC)		# Cycle sc
		rValsDPG = self.dpg.cycle(rValsSC)		# Cycle dpg

		# Adjust count and data index
		self.count += 1
		self.idx += 1
		self.idx %= self.bufSize

		# Build the data record and store it
		dRecUPD = \
			TaData(self.count, rValsCC[0], rValsCC[1], rValsCC[2], \
					rValsSC[0], rValsSC[1], rValsSC[2], \
					rValsDPG[0], rValsDPG[1], rValsDPG[2], self.scale.wgt)
		self.data[self.idx] = dRecUPD
		if (self.count % self.bufSize) == 0 :
			print(f'Count: {self.count} T: {self.count * self.cfg.deltaT} ph2o: {self.data[self.idx].ph2oSC}')



		



	




