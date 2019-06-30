from __future__ import division
import ROOT
import argparse
from math import sqrt

from lib.histos import declareHistos

def getFileType():

	parser = argparse.ArgumentParser()
	parser.add_argument('-y', '--year', help = 'The production year for MiniAOD file (2017 or 2018)', type = int)
	parser.add_argument('-t', '--test', help = 'Run over the test file', action = 'store_true')
	args = parser.parse_args()

	return args

def deltaR(prt1, prt2):
	
	eta1, eta2 = prt1.eta, prt2.eta
	phi1, phi2 = prt1.phi, prt2.phi
	eta_diff = eta1 - eta2
	phi_diff = phi1 - phi2
	
	return sqrt((eta_diff)**2 + (phi_diff)**2) 
	
def readTree(inputFile):

	f = ROOT.TFile.Open(inputFile, 'UPDATE')
	
	#Define the histograms

	histos = declareHistos()
	
	print('Histograms declared')

	event_count_before = 0
	event_count_after = 0
	event_count_afterL1 = 0

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
		jet_btag_CSVv2 = event.jet_btag_CSVv2

		histos['nJets_hist'].Fill(nJet)

		if nJet > 1:
		
			totalEnergy = jet_energy[0] + jet_energy[1]
			totalPx = jet_px[0] + jet_px[1]			
			totalPy = jet_py[0] + jet_py[1]			
			totalPz = jet_pz[0] + jet_pz[1]			
			
			mjj = sqrt(totalEnergy**2 - totalPx**2 - totalPy**2 - totalPz**2) #Invariant mass of two leading jets

			histos['mjj_hist'].Fill(mjj)

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
		L1_met_phi = event.L1_met_phi

		L1_nJet = event.L1_nJet
		L1_jet_pt = event.L1_jet_pt
		L1_jet_energy = event.L1_jet_energy
		L1_jet_eta = event.L1_jet_eta
		L1_jet_phi = event.L1_jet_phi
		L1_jet_px = event.L1_jet_px
		L1_jet_py = event.L1_jet_py	
		L1_jet_pz = event.L1_jet_pz
	
		if L1_nJet > 1:
		
			L1_totalEnergy = L1_jet_energy[0] + L1_jet_energy[1]
			L1_totalPx = L1_jet_px[0] + L1_jet_px[1]			
			L1_totalPy = L1_jet_py[0] + L1_jet_py[1]			
			L1_totalPz = L1_jet_pz[0] + L1_jet_pz[1]			
			
			L1_mjj = sqrt(L1_totalEnergy**2 - L1_totalPx**2 - L1_totalPy**2 - L1_totalPz**2) #Invariant mass of two leading jets at L1 level
		
			#L1 seed selection
		
			if not jet_pt[0] > 115 and jet_pt[1] > 40 and L1_mjj > 620: continue

			event_count_afterL1 += 1
		
		#VBF cuts
		
		if met < 200: continue

		if not (jet_pt[0] > 80 and jet_pt[1] > 40): continue

		if minPhi_jetMET < 0.5: continue

		if jet_eta[0] * jet_eta[1] > 0: continue

		if abs(jet_eta[0] - jet_eta[1]) < 2.5: continue
	
		num_bJets = 0

		for val in jet_btag_CSVv2:
			
			if val > 0.8484: #2017 requirements			
				num_bJets += 1	

		if num_bJets != 0: continue #b-jet veto

		#Add mjj > 500 selection here!
		event_count_after += 1
	
	histos['nJets_hist'].Write('nJets_hist')
	histos['mjj_hist'].Write('mjj_hist')
	
	f.Close()

	print('\n')			
	print('*******************')
	print('Event Yield Results')
	print('*******************\n')
	print('Total number of events read                  : {0:6d}'.format(event_count_before))
	print('Total number of events passed L1 seed        : {0:6d}        Passing Ratio: {1:6.2f}%'.format(event_count_afterL1, event_count_afterL1*100/event_count_before))
	print('Total number of events passed VBF selections : {0:6d}        Passing Ratio: {1:6.2f}%\n'.format(event_count_after, event_count_after*100/event_count_before)) 
	print('Job finished')


if __name__ == '__main__':

	file_type = getFileType()
	
	if file_type.test:

		inputFile = 'inputs/VBF_HToInv_' + str(file_type.year) + '_test.root'
		print('Starting job')
		print('File: {}'.format(inputFile))

	else:
 
		inputFile = 'inputs/VBF_HToInv_' + str(file_type.year) + '.root'
		print('Starting job')
		print('File: {}'.format(inputFile))


	#inputFile = 'inputs/VBF_HToInv_2017_test.root'

	readTree(inputFile) 

 
