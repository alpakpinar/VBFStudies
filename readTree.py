import ROOT
from math import sqrt

def deltaR(prt1, prt2):
	
	eta1, eta2 = prt1.eta, prt2.eta
	phi1, phi2 = prt1.phi, prt2.phi
	eta_diff = eta1 - eta2
	phi_diff = phi1 - phi2
	
	return sqrt((eta_diff)**2 + (phi_diff)**2) 
	
def readTree(inputFile):

	f = ROOT.TFile.Open(inputFile)

	event_count_before = 0
	event_count_after = 0

	for event in f.eventTree:
		
		event_count_before += 1
		
		# Reading the branches of eventTree		
		met = event.met
		metPhi = event.metPhi
		
		jet_pt = event.jet_pt
		jet_eta = event.jet_eta
		jet_energy = event.jet_energy
		jet_phi = event.jet_phi

		minPhi_jetMET = event.minPhi_jetMET
	
		nElectron = event.nElectron
		electron_pt = event.electron_pt
		electron_phi = event.electron_phi
		electron_eta = event.electron_eta

		nMuon = event.nMuon
		muon_pt = event.muon_pt
		muon_phi = event.muon_phi
		muon_eta = event.muon_eta
		
		nTau = event.nTau
		tau_pt = event.tau_pt
		tau_phi = event.tau_phi
		tau_eta = event.tau_eta

		nParticles = event.nParticles
		pdgId = event.pdgId
	
		#VBF cuts
		if met < 200: continue

		if not (leadingJetPt > 80 and trailingJetPt > 40): continue

		if minPhi_jetMET < 0.5: continue

		if etaProduct > 0: continue

		if delta_jj < 2.5: continue

		event_count_after += 1
				

if __name__ == '__main__':

	inputFile = 'VBF_HToInv.root'
	readTree(inputFile) 

 
