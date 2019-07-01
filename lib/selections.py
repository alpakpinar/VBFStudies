import ROOT
from math import sqrt

def applyVBFSelections(event):

	'''
	Applies VBF selections for a given event.
	Returns True if event passes the cuts, otherwise returns False.
	'''
		
	if event.met < 200: return False

	if not (event.jet_pt[0] > 80 and event.jet_pt[1] > 40): return False

	if event.minPhi_jetMET < 0.5: return False

	if event.jet_eta[0] * event.jet_eta[1] > 0: return False

	if abs(event.jet_eta[0] - event.jet_eta[1]) < 2.5: return False

	num_bJets = 0

	for val in event.jet_btag_CSVv2:
		
		if val > 0.8484: #2017 requirements			
			num_bJets += 1	

	if num_bJets != 0: return False #b-jet veto

	totalEnergy = event.jet_energy[0] + event.jet_energy[1]
	totalPx = event.jet_px[0] + event.jet_px[1]			
	totalPy = event.jet_py[0] + event.jet_py[1]			
	totalPz = event.jet_pz[0] + event.jet_pz[1]			
	
	mjj = sqrt(totalEnergy**2 - totalPx**2 - totalPy**2 - totalPz**2) #Invariant mass of two leading jets

	if mjj < 500: return False

	return True

def applyL1Selection(event):
	
	'''
	Applies L1 selection to a given event.
	Returns True if event passes the L1 trigger, otherwise returns False.
	'''

	if event.L1_nJet < 2: return False

	else:
		
		L1_totalEnergy = event.L1_jet_energy[0] + event.L1_jet_energy[1]
		L1_totalPx = event.L1_jet_px[0] + event.L1_jet_px[1]			
		L1_totalPy = event.L1_jet_py[0] + event.L1_jet_py[1]			
		L1_totalPz = event.L1_jet_pz[0] + event.L1_jet_pz[1]			
		
		L1_mjj = sqrt(L1_totalEnergy**2 - L1_totalPx**2 - L1_totalPy**2 - L1_totalPz**2) #Invariant mass of two leading jets at L1 level

		if not (event.L1_jet_pt[0] > 115 and event.L1_jet_pt[1] > 40 and L1_mjj > 620): return False #Simulating the L1 trigger

	return True

def applyHLTSelection(event, HLT_path):

	'''
	Applies L1 + HLT trigger selections for a given event.
	Returns True if event passes the L1 trigger and HLT trigger specified, otherwise returns False.
	'''
	
	if applyL1Selection(event):
	
		if getattr(event, HLT_path) == 1: return True

		else: return False
	
	return False

def applyAllSelections(event, HLT_path):

	'''
	Applies L1 + HLT + VBF selections for a given event and HLT_path.
	Returns True if event passes all the selections, otherwise returns False.
	'''

	return applyHLTSelection(event, HLT_path) and applyVBFSelections(event)
	
