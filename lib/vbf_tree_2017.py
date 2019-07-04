from array import array

max_num = 1000

#MET information

met = array('f', [0.])
met_phi = array('f', [0.])
met_eta = array('f', [0.])

#Jet information

nJet = array('i', [0])
minPhi_jetMET = array('f', [0.])
jet_pt = array('f', max_num*[0.]) 
jet_energy = array('f', max_num*[0.]) 
jet_eta = array('f', max_num*[0.]) 
jet_phi = array('f', max_num*[0.])
jet_px = array('f', max_num*[0.])
jet_py = array('f', max_num*[0.])
jet_pz = array('f', max_num*[0.])
jet_btag_CSVv2 = array('f', max_num*[0.])
mjj = array('f', [0.])

#Electron information

nElectron = array('i', [0])
electron_pt = array('f', max_num*[0.]) 
electron_energy = array('f', max_num*[0.]) 
electron_eta = array('f', max_num*[0.]) 
electron_phi = array('f', max_num*[0.])

#Muon information

nMuon = array('i', [0])
muon_pt = array('f', max_num*[0.]) 
muon_energy = array('f', max_num*[0.]) 
muon_eta = array('f', max_num*[0.]) 
muon_phi = array('f', max_num*[0.])

#Tau information

nTau = array('i', [0])
tau_pt = array('f', max_num*[0.]) 
tau_energy = array('f', max_num*[0.]) 
tau_eta = array('f', max_num*[0.]) 
tau_phi = array('f', max_num*[0.])

#Gen-particles

nParticles = array('i', [0])
pdgId = array('i', max_num*[0])

#2017 DiJet Triggers

HLT_DiJet110_35_Mjj650_PFMET110_v2 = array('i', [0])
HLT_DiJet110_35_Mjj650_PFMET120_v2 = array('i', [0])
HLT_DiJet110_35_Mjj650_PFMET130_v2 = array('i', [0])

#2017 MET Triggers

HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v13 = array('i', [0])
HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v13 = array('i', [0])
HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v12 = array('i', [0])
HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v12 = array('i', [0])

#L1 Level Information for jets and MET

L1_nJet = array('i', [0])
L1_jet_pt = array('f', max_num*[0.])
L1_jet_energy = array('f', max_num*[0.]) 
L1_jet_eta = array('f', max_num*[0.]) 
L1_jet_phi = array('f', max_num*[0.])
L1_jet_px = array('f', max_num*[0.])
L1_jet_py = array('f', max_num*[0.])
L1_jet_pz = array('f', max_num*[0.])

L1_met = array('f', [0.])
L1_met_eta = array('f', [0.])
L1_met_phi = array('f', [0.])

#Branch for veto information
containsLepton = array('i', [0]) 
contains_bJet = array('i', [0])

def declare_branches(tree):
	
	print('######## Creating branches ########')

	tree.Branch('met', met, 'met/F')
	tree.Branch('met_phi', met_phi, 'met_phi/F')
	tree.Branch('met_eta', met_eta, 'met_eta/F')
	
	tree.Branch('nJet', nJet, 'nJet/I')
	tree.Branch('minPhi_jetMET', minPhi_jetMET, 'minPhi_jetMET/F')
	tree.Branch('jet_pt', jet_pt, 'jet_pt[nJet]/F')
	tree.Branch('jet_energy', jet_energy, 'jet_energy[nJet]/F')
	tree.Branch('jet_eta', jet_eta, 'jet_eta[nJet]/F')
	tree.Branch('jet_phi', jet_phi, 'jet_phi[nJet]/F')
	tree.Branch('jet_px', jet_px, 'jet_px[nJet]/F')	
	tree.Branch('jet_py', jet_py, 'jet_py[nJet]/F')	
	tree.Branch('jet_pz', jet_pz, 'jet_pz[nJet]/F')	
	tree.Branch('jet_btag_CSVv2', jet_btag_CSVv2, 'jet_btag_CSVv2[nJet]/F')	
	tree.Branch('mjj', mjj, 'mjj/F')	

	tree.Branch('nElectron', nElectron, 'nElectron/I')
	tree.Branch('electron_pt', electron_pt, 'electron_pt[nElectron]/F')
	tree.Branch('electron_phi', electron_phi, 'electron_phi[nElectron]/F')	
	tree.Branch('electron_eta', electron_eta, 'electron_eta[nElectron]/F')
	tree.Branch('electron_energy', electron_energy, 'electron_energy[nElectron]/F')
	
	tree.Branch('nMuon', nMuon, 'nMuon/I')
	tree.Branch('muon_pt', muon_pt, 'muon_pt[nMuon]/F')
	tree.Branch('muon_phi', muon_phi, 'muon_phi[nMuon]/F')
	tree.Branch('muon_eta', muon_eta, 'muon_eta[nMuon]/F')
	tree.Branch('muon_energy', muon_energy, 'muon_energy[nMuon]/F')

	tree.Branch('nTau', nTau, 'nTau/I')
	tree.Branch('tau_pt', tau_pt, 'tau_pt[nTau]/F')
	tree.Branch('tau_phi', tau_phi, 'tau_phi[nTau]/F')
	tree.Branch('tau_eta', tau_eta, 'tau_eta[nTau]/F')
	tree.Branch('tau_energy', tau_energy, 'tau_energy[nTau]/F')

	tree.Branch('nParticles', nParticles, 'nParticles/I')
	tree.Branch('pdgId', pdgId, 'pdgId[nParticles]/I')

	tree.Branch('HLT_DiJet110_35_Mjj650_PFMET110_v2', HLT_DiJet110_35_Mjj650_PFMET110_v2, 'HLT_DiJet110_35_Mjj650_PFMET110_v2/I')
	tree.Branch('HLT_DiJet110_35_Mjj650_PFMET120_v2', HLT_DiJet110_35_Mjj650_PFMET120_v2, 'HLT_DiJet110_35_Mjj650_PFMET120_v2/I')
	tree.Branch('HLT_DiJet110_35_Mjj650_PFMET130_v2', HLT_DiJet110_35_Mjj650_PFMET130_v2, 'HLT_DiJet110_35_Mjj650_PFMET130_v2/I')
	tree.Branch('HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v13', HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v13, 'HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v13/I')
	tree.Branch('HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v13', HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v13, 'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v13/I')
	tree.Branch('HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v12', HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v12, 'HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v12/I')
	tree.Branch('HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v12', HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v12, 'HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v12/I')
	
	tree.Branch('L1_nJet', L1_nJet, 'L1_nJet/I')
	tree.Branch('L1_jet_pt', L1_jet_pt, 'L1_jet_pt[L1_nJet]/F')
	tree.Branch('L1_jet_energy', L1_jet_energy, 'L1_jet_energy[L1_nJet]/F')
	tree.Branch('L1_jet_eta', L1_jet_eta, 'L1_jet_eta[L1_nJet]/F')
	tree.Branch('L1_jet_phi', L1_jet_phi, 'L1_jet_phi[L1_nJet]/F')
	tree.Branch('L1_jet_px', L1_jet_px, 'L1_jet_px[L1_nJet]/F')	
	tree.Branch('L1_jet_py', L1_jet_py, 'L1_jet_py[L1_nJet]/F')	
	tree.Branch('L1_jet_pz', L1_jet_pz, 'L1_jet_pz[L1_nJet]/F')	

	tree.Branch('L1_met', L1_met, 'L1_met/F')
	tree.Branch('L1_met_eta', L1_met_eta, 'L1_met_eta/F')
	tree.Branch('L1_met_phi', L1_met_phi, 'L1_met_phi/F')
	
	tree.Branch('containsLepton', containsLepton, 'containsLepton/I')
	tree.Branch('contains_bJet', contains_bJet, 'contains_bJet/I')

	print('######## Branches declared ########')


	





 
 


