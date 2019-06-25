import numpy as np

max_num = 1000

#MET information

met = np.zeros(1, dtype=float)
metPhi = np.zeros(1, dtype=float)
genMet = np.zeros(1, dtype=float)

#Jet information

nJet = np.zeros(1, dtype=int)
leadingJetPt = np.zeros(1, dtype=float)
trailingJetPt = np.zeros(1,dtype=float) 
leadingJetEta = np.zeros(1, dtype=float)
trailingJetEta = np.zeros(1, dtype=float)
leadingJetPhi = np.zeros(1, dtype=float)
trailingJetPhi = np.zeros(1, dtype=float)
minPhi_jetMET = np.zeros(1, dtype=float)
etaProduct = np.zeros(1, dtype=float)
delta_jj = np.zeros(1, dtype=float)

#Electron information

nElectron = np.zeros(1, dtype=int)
electron_pt = np.zeros(max_num, dtype=float)
electron_phi = np.zeros(max_num, dtype=float)
electron_eta = np.zeros(max_num, dtype=float)

#Muon information

nMuon = np.zeros(1, dtype=int)
muon_pt = np.zeros(max_num, dtype=float)
muon_phi = np.zeros(max_num, dtype=float)
muon_eta = np.zeros(max_num, dtype=float)

#Tau information

nTau = np.zeros(1, dtype=int)
tau_pt = np.zeros(max_num, dtype=float)
tau_phi = np.zeros(max_num, dtype=float)
tau_eta = np.zeros(max_num, dtype=float)

#Gen-particles

pdgId = np.zeros(max_num, dtype=int)
mothers = np.zeros(max_num, dtype=int)

def declare_branches(tree):

	print('######## Creating branches ########')

	tree.branch('met', met, 'met/F')
	tree.branch('metPhi', metPhi, 'metPhi/F')
	tree.branch('genMet', genMet, 'genMet/F')
	
	tree.branch('nJet', nJet, 'nJet/I')
	tree.branch('leadingJetPt', leadingJetPt, 'leadingJetPt/F')
	tree.branch('trailingJetPt', trailingJetPt, 'trailingJetPt/F')
	tree.branch('leadingJetEta', leadingJetEta, 'leadingJetEta/F')
	tree.branch('trailingJetEta', trailingJetEta, 'trailingJetEta/F')
	tree.branch('leadingJetPhi', leadingJetPhi, 'leadingJetPhi/F')
	tree.branch('trailingJetPhi', trailingJetPhi, 'trailingJetPhi/F')
	tree.branch('minPhi_jetMET', minPhi_jetMET, 'minPhi_jetMET/F')
	tree.branch('delta_jj', delta_jj, 'delta_jj/F')

	tree.branch('nElectron', nElectron, 'nElectron/I')
	tree.branch('electron_pt', electron_pt, 'electron_pt[nElectron]/F')
	tree.branch('electron_phi', electron_phi, 'electron_phi[nElectron]/F')	
	tree.branch('electron_eta', electron_eta, 'electron_eta[nElectron]/F')
	
	tree.branch('nMuon', nMuon, 'nMuon/I')
	tree.branch('muon_pt', muon_pt, 'muon_pt[nMuon]/F')
	tree.branch('muon_phi', muon_phi, 'muon_phi[nMuon]/F')
	tree.branch('muon_eta', muon_eta, 'muon_eta[nMuon]/F')

	tree.branch('nTau', nTau, 'nTau/I')
	tree.branch('tau_pt', tau_pt, 'tau_pt[nTau]/F')
	tree.branch('tau_phi', tau_phi, 'tau_phi[nTau]/F')
	tree.branch('tau_eta', tau_eta, 'tau_eta[nTau]/F')
	
	print('######## Branches declared ########')


	





 
 


