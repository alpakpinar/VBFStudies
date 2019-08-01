import ROOT
import numpy as np
from lib.defineHistos import defineMET_mjjHistos 
from lib.helperFunctions import *
from lib.veto import *

# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events	

def fill_mjjMETHisto(fileName, MET_mjjHistos):

	'''
	Constructs a 2D histogram with mjj values coming from leading 2 jets and MET in the event.
	Saves the plot as a png file.
	'''
	#No stat box in the histograms
	
	ROOT.gStyle.SetOptStat(0)
	
	electrons, electronLabel = Handle('std::vector<pat::Electron>'), 'slimmedElectrons'
	muons, muonLabel = Handle('std::vector<pat::Muon>'), 'slimmedMuons'
	taus, tauLabel = Handle('std::vector<pat::Tau>'), 'slimmedTaus'
	photons, photonLabel = Handle('std::vector<pat::Photon>'), 'slimmedPhotons'
	jets, jetLabel = Handle('std::vector<pat::Jet>'), 'slimmedJets'
	mets, metLabel = Handle('std::vector<pat::MET>'), 'slimmedMETs'

	events = Events(fileName)

	#######################
	#Event loop starts here
	#######################

	for iev, event in enumerate(events):

		#if iev == 1000: break #For testing

		if iev % 1000 == 0:
			print('Working on event {}'.format(iev))

		event.getByLabel(electronLabel, electrons)
		event.getByLabel(muonLabel, muons)
		event.getByLabel(tauLabel, taus)
		event.getByLabel(photonLabel, photons)
		event.getByLabel(jetLabel, jets)
		event.getByLabel(metLabel, mets)

		######################
		#Implementing tight jet ID, 2017 recommendations
		######################
	
		mets_ = mets.product()

		met = mets_[0].pt()
		met_phi = mets_[0].phi()

		jets_ = jets.product()

		AK4_tightJets = []
		
		for jet in jets_:

			if isTightJet(jet):			
	
				AK4_tightJets.append(jet) 

		nJet = len(AK4_tightJets)
		
		if nJet < 2: continue #Discard the events with number of jets smaller than 2
		
		#######################
		#Apply VBF cuts
		#######################

		if containsLeptonOrPhoton(electrons, muons, taus, photons): continue #Lepton-photon veto

		if contains_bJet(AK4_tightJets): continue #b-jet veto
	
		minPhi_jetMET = minJetMETPhi(AK4_tightJets, mets_)

		if minPhi_jetMET <= 0.5: continue

		absEtaDiff_twoLeadingJets = abs(AK4_tightJets[0].eta() - AK4_tightJets[1].eta())
	
		if absEtaDiff_twoLeadingJets <= 2.5: continue

		if AK4_tightJets[0].eta() * AK4_tightJets[1].eta() > 0: continue

		#Leading jet pt cuts
		if not (AK4_tightJets[0].pt() > 100 and AK4_tightJets[1].pt() > 30): continue

		#########################
		#VBF cuts end here
		#########################

		mjj_values = invMassJetCombos(AK4_tightJets) #Get all the mjj values for all possible combos

		maxCombo = getMaxCombo(mjj_values) #Get the jet pair for which the maximum mjj happens to be

		jet_geometry = getJetGeometry(AK4_tightJets[0], AK4_tightJets[1]) #Determine the geometry of two leading jets

		mjj_leadingTrailingJet = mjj_values['leadingJet_trailingJet']

		if jet_geometry == 'Two Central Jets':
		
			MET_mjjHistos['mjjMETHisto_twoCentralJets'].Fill(mjj_leadingTrailingJet, met) 

		elif jet_geometry == 'Mixed':
			
			MET_mjjHistos['mjjMETHisto_mixed'].Fill(mjj_leadingTrailingJet, met) 
			
def main():

	MET_mjjHistos = defineMET_mjjHistos()

	for hist in MET_mjjHistos.values():

		hist.SetDirectory(0)

	f = file('inputs/MiniAOD_files2017.txt', 'r')

	for numFile, fileName in enumerate(f.readlines()):

		print('Working on file {}'.format(numFile+1))
		
		if numFile == 2: break #For testing

		fill_mjjMETHisto(fileName, MET_mjjHistos)

	#Draw and save the histograms

	print2DHisto(MET_mjjHistos['mjjMETHisto_twoCentralJets'])
	print2DHisto(MET_mjjHistos['mjjMETHisto_mixed'])
	
if __name__ == '__main__':

	main()








	

