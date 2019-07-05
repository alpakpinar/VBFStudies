from __future__ import division
import ROOT
import argparse
from math import sqrt
from array import array

from lib.histos import declareHistos
from lib.selections import *

def getFileType():

	parser = argparse.ArgumentParser()
	parser.add_argument('-y', '--year', help = 'The production year for MiniAOD file (2017 or 2018)', type = int)
	parser.add_argument('-t', '--test', help = 'Run over the test file', action = 'store_true')
	parser.add_argument('-s', '--shortTest', help = 'Run over the short test file', action = 'store_true')
	parser.add_argument('-c', '--clean', help = 'Clean the ROOT file by deleting all previous histograms', action = 'store_true')
	args = parser.parse_args()

	return args

def cleanROOTFile(inputFile, histos):
	
	'''
	Removes the first ten versions of the histograms from the ROOT file.
	Called only if -c option is specified while running the script.
	'''
	print('Cleaning the ROOT file')

	f = ROOT.TFile(inputFile, 'UPDATE')

	for histo in histos.keys():

		for i in range(10):
			
			hist = histo + ';' + str(i+1)
			ROOT.gDirectory.Delete(hist)	
		
	f.Close()
	
	print('Cleaning done')

def deltaR(prt1, prt2):
	
	eta1, eta2 = prt1.eta, prt2.eta
	phi1, phi2 = prt1.phi, prt2.phi
	eta_diff = eta1 - eta2
	phi_diff = phi1 - phi2
	
	return sqrt((eta_diff)**2 + (phi_diff)**2) 

###########################

def drawTriggerEff_MET(inputFile, trigger):

	'''
	Constructs the trigger efficiency graph for a given trigger, as a function of MET.
	'''
	
	f = ROOT.TFile.Open(inputFile, 'UPDATE')

	met_array = array('f', [100., 120., 140., 170., 200., 240., 290., 350., 420., 500.]) 

	met_hist = ROOT.TH1F('met_hist', 'met_hist', len(met_array)-1, met_array)
	histos['met_hist'] = met_hist

	met_hist_afterVBFCuts = ROOT.TH1F('met_hist_afterVBFCuts', 'met_hist_afterVBFCuts', len(met_array)-1, met_array)	
	histos['met_hist_afterVBFCuts'] = met_hist_afterVBFCuts

	met_hist_afterVBFCutsAndTrigger = ROOT.TH1F('met_hist_afterVBFCutsAndTrigger', 'met_hist_afterVBFCutsAndTrigger', len(met_array)-1, met_array)	
	histos['met_hist_afterVBFCutsAndTrigger'] = met_hist_afterVBFCutsAndTrigger

	vbfCuts = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && met > 200 && jet_pt[0] > 80 && jet_pt[1] > 40 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && mjj > 500 && absEtaDiff_leadingTwoJets > 2.5'

	vbfAndTriggerCuts = vbfCuts + ' && ' + trigger + ' == 1'

	f.eventTree.Draw('met>>met_hist')
	f.eventTree.Draw('met>>met_hist_afterVBFCuts', vbfCuts, '')
	f.eventTree.Draw('met>>met_hist_afterVBFCutsAndTrigger', vbfAndTriggerCuts, '')
	
	#Check if the two histograms are consistent

	if ROOT.TEfficiency.CheckConsistency(met_hist_afterVBFCutsAndTrigger, met_hist_afterVBFCuts):

		eff_graph = ROOT.TEfficiency(met_hist_afterVBFCutsAndTrigger, met_hist_afterVBFCuts)

		eff_graph.Write('eff_graph_' + trigger + '_MET')

		print('Efficiency graph for MET is constructed!')
	
	f.Write()
	f.Close()

def drawTriggerEff_mjj(inputFile, trigger):

	'''
	Constructs the trigger efficiency graph for a given trigger, as a function of invariant mass of two leading jets, mjj.
	'''
	
	f = ROOT.TFile.Open(inputFile, 'UPDATE')

	mjj_array = array('f', [500., 530., 560., 600., 640., 680., 730., 790., 880., 1000.]) 

	mjj_hist = ROOT.TH1F('mjj_hist', 'mjj_hist', len(mjj_array)-1, mjj_array)
	histos['mjj_hist'] = mjj_hist

	mjj_hist_afterVBFCuts = ROOT.TH1F('mjj_hist_afterVBFCuts', 'mjj_hist_afterVBFCuts', len(mjj_array)-1, mjj_array)	
	histos['mjj_hist_afterVBFCuts'] = mjj_hist_afterVBFCuts
	
	mjj_hist_afterVBFCutsAndTrigger = ROOT.TH1F('mjj_hist_afterVBFCutsAndTrigger', 'mjj_hist_afterVBFCutsAndTrigger', len(mjj_array)-1, mjj_array)
	histos['mjj_hist_afterVBFCutsAndTrigger'] = mjj_hist_afterVBFCutsAndTrigger

	vbfCuts = 'containsLepton == 0 && contains_bJet == 0 && met > 200 && jet_pt[0] > 80 && jet_pt[1] > 40 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && mjj > 500 && absEtaDiff_leadingTwoJets > 2.5'

	vbfAndTriggerCuts = vbfCuts + ' && ' + trigger + ' == 1'

	f.eventTree.Draw('mjj>>mjj_hist')
	f.eventTree.Draw('mjj>>mjj_hist_afterVBFCuts', vbfCuts, '')
	f.eventTree.Draw('mjj>>mjj_hist_afterVBFCutsAndTrigger', vbfAndTriggerCuts, '')
	
	#Check if the two histograms are consistent

	if ROOT.TEfficiency.CheckConsistency(mjj_hist_afterVBFCutsAndTrigger, mjj_hist_afterVBFCuts):

		eff_graph = ROOT.TEfficiency(mjj_hist_afterVBFCutsAndTrigger, mjj_hist_afterVBFCuts)

		eff_graph.Write('eff_graph_' + trigger + '_mjj')

		print('Efficiency graph for mjj is constructed!')
	
	f.Write()
	f.Close()

#############################

def readTree(inputFile):

	f = ROOT.TFile.Open(inputFile, 'UPDATE')
	
	event_count_before = 0
	event_count_afterL1 = 0
	event_count_afterL1HLT = 0
	event_count_afterVBF = 0
	event_count_afterALL = 0

	for event in f.eventTree:
		
		event_count_before += 1
		
		# Reading the branches of eventTree		
		nJet = event.nJet		
		jet_pt = event.jet_pt
		jet_eta = event.jet_eta
		jet_energy = event.jet_energy
		jet_phi = event.jet_phi
		jet_px = event.jet_px
		jet_py = event.jet_py
		jet_pz = event.jet_pz

		histos['nJets_hist'].Fill(nJet)
		histos['leadingJetPt_hist'].Fill(jet_pt[0])
		histos['trailingJetPt_hist'].Fill(jet_pt[1])

		if nJet > 1:
		
			totalEnergy = jet_energy[0] + jet_energy[1]
			totalPx = jet_px[0] + jet_px[1]			
			totalPy = jet_py[0] + jet_py[1]			
			totalPz = jet_pz[0] + jet_pz[1]			
			
			mjj = sqrt(totalEnergy**2 - totalPx**2 - totalPy**2 - totalPz**2) #Invariant mass of two leading jets

			histos['mjj_hist'].Fill(mjj)

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

		if applyL1Selection(event): #L1 selection only

			event_count_afterL1 += 1
		
		if applyHLTSelection(event, 'HLT_DiJet110_35_Mjj650_PFMET110_v2'): #L1 + HLT selection
			
			event_count_afterL1HLT += 1
		
		if applyVBFSelections(event): #VBF selections only
	
			event_count_afterVBF += 1
	
		if applyAllSelections(event, 'HLT_DiJet110_35_Mjj650_PFMET110_v2'):
			
			event_count_afterALL += 1

	histos['nJets_hist'].Write('nJets_hist')
	histos['mjj_hist'].Write('mjj_hist')
	histos['leadingJetPt_hist'].Write('leadingJetPt_hist')
	histos['trailingJetPt_hist'].Write('trailingJetPt_hist')

	f.Close()

	print('\n')			
	print('*******************')
	print('Event Yield Results')
	print('*******************\n')
	print('Total number of events read                              : {0:6d}'.format(event_count_before))
	print('Total number of events passed L1 seed                    : {0:6d}        Passing Ratio: {1:6.2f}%'.format(event_count_afterL1, event_count_afterL1*100/event_count_before))
	print('Total number of events passed L1 seed + HLT              : {0:6d}        Passing Ratio: {1:6.2f}%'.format(event_count_afterL1HLT, event_count_afterL1HLT*100/event_count_before))
	print('Total number of events passed VBF selections             : {0:6d}        Passing Ratio: {1:6.2f}%'.format(event_count_afterVBF, event_count_afterVBF*100/event_count_before)) 
	print('Total number of events passed L1 + HLT + VBF selections  : {0:6d}        Passing Ratio: {1:6.2f}%\n'.format(event_count_afterALL, event_count_afterALL*100/event_count_before)) 
	print('Job finished')


if __name__ == '__main__':

	file_type = getFileType()
	
	if file_type.test:

		inputFile = 'inputs/VBF_HToInv_' + str(file_type.year) + '_test.root'
		print('Starting job')
		print('File: {}'.format(inputFile))

	elif file_type.shortTest:
		
		inputFile = 'inputs/VBF_HToInv_' + str(file_type.year) + '_shortTest.root'
		print('Starting job')
		print('File: {}'.format(inputFile))
	
	else:
 
		inputFile = 'inputs/VBF_HToInv_' + str(file_type.year) + '.root'
		print('Starting job')
		print('File: {}'.format(inputFile))
	
	#Define the histograms

	histos = declareHistos()

	#Clean the ROOT file if needed

	if file_type.clean:

		cleanROOTFile(inputFile, histos)

	#inputFile = 'inputs/VBF_HToInv_2017_test.root'

	#readTree(inputFile) 

	trigger = 'HLT_DiJet110_35_Mjj650_PFMET110_v2'

	drawTriggerEff_mjj(inputFile, trigger)

	drawTriggerEff_MET(inputFile, trigger)

 
