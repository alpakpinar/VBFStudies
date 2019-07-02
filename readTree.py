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

def invMassTwoJets(event):
	
	totalEnergy = event.jet_energy[0] + event.jet_energy[1]
	totalPx = event.jet_px[0] + event.jet_px[1]			
	totalPy = event.jet_py[0] + event.jet_py[1]			
	totalPz = event.jet_pz[0] + event.jet_pz[1]			
	
	mjj = sqrt(totalEnergy**2 - totalPx**2 - totalPy**2 - totalPz**2) #Invariant mass of two leading jets

	return mjj

def calculateTriggerEff_leadingJetEta(inputFile, trigger, eta_lowerBound, eta_upperBound):

	'''
	Calculates the efficiency (acceptance) of a given trigger as a function of eta.
	'''
	f = ROOT.TFile.Open(inputFile, 'UPDATE')

	event_count_afterVBF = 0
	event_count_afterALL = 0 

	for event in f.eventTree:

		leadingJetEta = event.jet_eta[0]

		if eta_lowerBound < leadingJetEta < eta_upperBound:
			
			if applyVBFSelections(event): #VBF selections only
		
				event_count_afterVBF += 1
		
			if applyAllSelections(event, trigger): #VBF + L1 + HLT selections
				
				event_count_afterALL += 1

	f.Close()

	print(event_count_afterVBF, event_count_afterALL)

	try:
		
		eff = event_count_afterALL/event_count_afterVBF

	except ZeroDivisionError:

		eff = 0.0

	return eff 

def drawTriggerEff_leadingJetEta(inputFile, trigger, eta_range = [0., 2.4], eta_step = 0.1):

	'''
	Draws the efficiency graph of a given trigger as a function of leading jet eta.
	Eta values in the given eta_range will be considered. By default, this interval is [0, 2.4]
	Efficiencies will be calculated with a eta jump of 0.1 by default, this can be changed by specifying eta_step option while calling this function.
	'''
	eta_values = array('f', [])
	efficiencies = array('f', [])

	for eta in range(eta_range[0], eta_range[1]+eta_step, eta_step):

		eta_values.append(eta)

		eff = calculateTriggerEff_leadingJetEta(inputFile, trigger, eta, eta + eta_step)

		efficiencies.append(eff)

	n = len(eta_values)

	f = ROOT.TFile.Open(inputFile, 'UPDATE')

	c = ROOT.TCanvas('c', 'c', 800, 600)
	c.SetGrid()
	
	eff_graph = ROOT.TGraph(n, eta_values, efficiencies)

	eff_graph.SetLineColor(4)
	eff_graph.SetMarkerStyle(20)
	eff_graph.SetTitle(trigger)
	eff_graph.GetXaxis().SetTitle('#Eta (GeV)')
	eff_graph.GetYaxis().SetTitle('Acceptance')

	eff_graph.Draw('ACP')

	c.SaveAs('TriggerEff_leadingJetEta.png')

	f.Write()
	f.Close()
	

def calculateTriggerEff_MET(inputFile, trigger, MET_lowerBound, MET_upperBound):
	
	'''
	Calculates and returns the efficiency (acceptance) of given trigger as a function of MET.
	'''
	f = ROOT.TFile.Open(inputFile, 'UPDATE')

	event_count_afterVBF = 0
	event_count_afterALL = 0 

	for event in f.eventTree:

		met = event.met
	
		if MET_lowerBound < met < MET_upperBound:
			
			if applyVBFSelections(event): #VBF selections only
		
				event_count_afterVBF += 1
		
			if applyAllSelections(event, trigger): #VBF + L1 + HLT selections
				
				event_count_afterALL += 1

	f.Close()

	print(event_count_afterVBF, event_count_afterALL)

	try:
		
		eff = event_count_afterALL/event_count_afterVBF

	except ZeroDivisionError:

		eff = 0.0

	return eff 


def drawTriggerEff_MET(inputFile, trigger, MET_range = [75, 200], MET_step=5):

	'''
	Draws the efficiency graph of a given trigger as a function of MET.
	MET values in the given MET_range will be considered. By default, this interval is [75,200]. 
	Efficiencies will be calculated with a MET jump of 5 by default, this can be changed by specifying MET_step option while calling this function.
	'''

	MET_values = array('f', [])
	efficiencies = array('f', [])

	for met in range(MET_range[0], MET_range[1] + MET_step, MET_step):

		MET_values.append(met)
		
		eff = calculateTriggerEff_MET(inputFile, trigger, met, met + MET_step)

		efficiencies.append(eff)

	n = len(MET_values)

	f = ROOT.TFile.Open(inputFile, 'UPDATE')

	c = ROOT.TCanvas('c', 'c', 800, 600)
	c.SetGrid()
	
	eff_graph = ROOT.TGraph(n, MET_values, efficiencies)

	eff_graph.SetLineColor(4)
	eff_graph.SetMarkerStyle(20)
	eff_graph.SetTitle(trigger)
	eff_graph.GetXaxis().SetTitle('MET (GeV)')
	eff_graph.GetYaxis().SetTitle('Acceptance')

	eff_graph.Draw('ACP')

	c.SaveAs('TriggerEff_MET.png')

	f.Write()
	f.Close()

def calculateTriggerEff_mjj(inputFile, trigger, mjj_lowerBound, mjj_upperBound):

	'''
	Calculates and returns the efficiency (acceptance) of given trigger as a function of invariant mass of two leading jets, mjj.
	'''

	f = ROOT.TFile.Open(inputFile, 'UPDATE')

	event_count_afterVBF = 0
	event_count_afterALL = 0 

	for event in f.eventTree:

		mjj = invMassTwoJets(event) 

		if mjj_lowerBound < mjj < mjj_upperBound:

			if applyVBFSelections(event): #VBF selections only
		
				event_count_afterVBF += 1
		
			if applyAllSelections(event, trigger): #VBF + L1 + HLT selections
				
				event_count_afterALL += 1

	f.Close()

	print(event_count_afterVBF, event_count_afterALL)

	try:
		
		eff = event_count_afterALL/event_count_afterVBF

	except ZeroDivisionError:

		eff = 0.0

	return eff 

def drawTriggerEff_mjj(inputFile, trigger, mjj_range = [500, 800], mjj_step=20):

	'''
	Draws the efficiency graph of a given trigger as a function of invariant mass of two leading jets. 
	Mjj values in the given mjj_range will be considered. By default, this interval is [500, 800].
	Efficiencies will be calculated with a mjj jump of 20 by default, this can be changed by specifying mjj_step option while calling this function.
	'''

	mjj_values = array('f', [])
	efficiencies = array('f', [])

	for mjj in range(mjj_range[0], mjj_range[1]+mjj_step, mjj_step):

		mjj_values.append(float(mjj))
		
		eff = calculateTriggerEff_mjj(inputFile, trigger, mjj, mjj + mjj_step)

		efficiencies.append(eff)

	n = len(mjj_values)

	f = ROOT.TFile.Open(inputFile, 'UPDATE')

	c = ROOT.TCanvas('c', 'c', 800, 600)
	c.SetGrid()
	
	eff_graph = ROOT.TGraph(n, mjj_values, efficiencies)

	eff_graph.SetLineColor(4)
	eff_graph.SetMarkerStyle(20)
	eff_graph.SetTitle(trigger)
	eff_graph.GetXaxis().SetTitle('M_{jj} (GeV)')
	eff_graph.GetYaxis().SetTitle('Acceptance')

	eff_graph.Draw('ACP')

	c.SaveAs('TriggerEff_mjj.png')

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

	drawTriggerEff_MET(inputFile, trigger)
	drawTriggerEff_leadingJetEta(inputFile, trigger)
	drawTriggerEff_mjj(inputFile, trigger)



 
