import ROOT
from math import sqrt

def applyVBFSelections(tree):

	'''
	Applies VBF selections and tracks the number of events throughout each cut.
	Returns the dictionary of event counts at different stages in the cut flow.
	'''
	keys = ['total', 'METCut', 'LeadingJetPtCut', 'TrailingJetPtCut', 'MinPhiJetMETCut', 'NegEtaProductCut', 'EtaDiffCut', 'bJetCut', 'LeptonVeto', 'PhotonVeto', 'mjjCut']

 	eventCounter = {key:0 for key in keys}

	for event in tree:

		eventCounter['total'] += 1
	
		if event.met < 200: continue

		eventCounter['METCut'] += 1

		if event.jet_pt[0] < 80: continue

		eventCounter['LeadingJetPtCut'] += 1

		if event.jet_pt[1] < 40: continue
		
		eventCounter['TrailingJetPtCut'] += 1

		if event.minPhi_jetMET < 0.5: continue

		eventCounter['MinPhiJetMETCut'] += 1

		if event.jet_eta[0] * event.jet_eta[1] > 0: continue

		eventCounter['NegEtaProductCut'] += 1

		if abs(event.jet_eta[0] - event.jet_eta[1]) < 2.5: continue

		eventCounter['EtaDiffCut'] += 1

		if event.contains_bJet != 0: continue

		eventCounter['bJetCut'] += 1

		if event.containsLepton != 0: continue

		eventCounter['LeptonVeto'] += 1

		if event.containsPhoton != 0: continue

		eventCounter['PhotonVeto'] += 1
		
		if event.mjj < 500: continue

		eventCounter['mjjCut'] += 1

	return eventCounter

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
	
