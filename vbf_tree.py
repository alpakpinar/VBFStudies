import numpy as np
from array import array

max_num = 1000

#MET information

met = array('f', [0.])
metPhi = array('f', [0.])
genMet = array('f', [0.]) 

#Jet information

nJet = array('i', [0])
minPhi_jetMET = array('f', [0.])
jet_pt = array('f', np.zeros(max_num, dtype=float))
jet_energy = array('f', np.zeros(max_num, dtype=float))
jet_eta = array('f', np.zeros(max_num, dtype=float))
jet_phi = array('f', np.zeros(max_num, dtype=float))

#Electron information

nElectron = array('i', [0])
electron_pt = array('f', np.zeros(max_num, dtype=float))
electron_phi = array('f', np.zeros(max_num, dtype=float))
electron_eta = array('f', np.zeros(max_num, dtype=float))
electron_energy = array('f', np.zeros(max_num, dtype=float))

#Muon information

nMuon = array('i', [0])
muon_pt = array('f', np.zeros(max_num, dtype=float))
muon_phi = array('f', np.zeros(max_num, dtype=float))
muon_eta = array('f', np.zeros(max_num, dtype=float))
muon_energy = array('f', np.zeros(max_num, dtype=float))

#Tau information

nTau = array('i', [0])
tau_pt = array('f', np.zeros(max_num, dtype=float))
tau_phi = array('f', np.zeros(max_num, dtype=float))
tau_eta = array('f', np.zeros(max_num, dtype=float))
tau_energy = array('f', np.zeros(max_num, dtype=float))

#Gen-particles

nParticles = array('i', [0])
pdgId = array('i', np.zeros(max_num, dtype=int))
mothers = array('i', np.zeros(max_num, dtype=int))


def declare_branches(tree):
	
	print('######## Creating branches ########')

	tree.Branch('met', met, 'met/F')
	tree.Branch('metPhi', metPhi, 'metPhi/F')
	tree.Branch('genMet', genMet, 'genMet/F')
	
	tree.Branch('nJet', nJet, 'nJet/I')
	tree.Branch('minPhi_jetMET', minPhi_jetMET, 'minPhi_jetMET/F')
	tree.Branch('jet_pt', jet_pt, 'jet_pt[nJet]/F')
	tree.Branch('jet_energy', jet_energy, 'jet_energy[nJet]/F')
	tree.Branch('jet_eta', jet_eta, 'jet_eta[nJet]/F')
	tree.Branch('jet_phi', jet_phi, 'jet_phi[nJet]/F')
	
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

	print('######## Branches declared ########')


	





 
 


