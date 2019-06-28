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
		met_phi = event.met_phi
		met_eta = event.met_eta

		nJet = event.nJet		
		jet_pt = event.jet_pt
		jet_eta = event.jet_eta
		jet_energy = event.jet_energy
		jet_phi = event.jet_phi
		jet_px = event.jet_px
		jet_py = event.jet_py
		jet_pz = event.jet_pz

		if nJet > 1:
		
			totalEnergy = jet_energy[0] + jet_energy[1]
			totalPx = jet_px[0] + jet_px[1]			
			totalPy = jet_py[0] + jet_py[1]			
			totalPz = jet_pz[0] + jet_pz[1]			
			
			mjj = sqrt(totalEnergy**2 - totalPx**2 - totalPy**2 - totalPz**2) #Invariant mass of two leading jets

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

		#Getting L1 level information

		L1_met = event.L1_met
		L1_met_eta = event.L1_met_eta
		L1_met_phi = event.L1_met_phii

		L1_nJet = event.L1_nJet
		L1_jet_pt = event.L1_jet_pt
		L1_jet_energy = event.L1_jet_energy
		L1_jet_eta = event.L1_jet_eta
		L1_jet_phi = event.L1_jet_phi
		L1_jet_px = event.L1_jet_px
		L1_jet_py = event.L1_jet_py	
		L1_jet_pz = event.L1_jet_pz
	
		#VBF cuts
		
		if met < 200: continue

		if not (leadingJetPt > 80 and trailingJetPt > 40): continue

		if minPhi_jetMET < 0.5: continue

		if jet_eta[0] * jet_eta[1] > 0: continue

		if abs(jet_eta[0] - jet_eta[1]) < 2.5: continue

		event_count_after += 1
				

if __name__ == '__main__':

	inputFile = 'VBF_HToInv.root'
	readTree(inputFile) 

 
