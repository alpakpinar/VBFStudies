import ROOT
import numpy as np
from lib.defineHistos import define2DHistos, defineHistosForRatioPlot
from lib.helperFunctions import *
from lib.veto import *

# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events	

def getFractionPlot_mjj(fileName, mjj_histos): 

	'''
	Constructs the graph showing the fraction of events where leading jet pair coincides with highest mjj pair.
	Also takes into account two seperate categories:
	--Two central jets
	--Mixed (one central, one forward jet)
	Returns a dictionary containing ratio histograms.
	'''
	#No stat box in the histograms
	
	ROOT.gStyle.SetOptStat(0)
	
	#mjjHistWithAllEvents_twoCentralJets = mjj_histos['mjjHistWithAllEvents_twoCentralJets']
	#mjjHistWithAllEvents_mixed = mjj_histos['mjjHistWithAllEvents_mixed']
	#mjjHistWithSelectedEvents_twoCentralJets = mjj_histos['mjjHistWithSelectedEvents_twoCentralJets']
	#mjjHistWithSelectedEvents_mixed = mjj_histos['mjjHistWithSelectedEvents_mixed'] 
	
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

		if jet_geometry == 'Two Central Jets':
		
			mjj_histos['mjjHistWithAllEvents_twoCentralJets'].Fill(mjj_values['leadingJet_trailingJet'])
		
			if maxCombo == (0,1) or maxCombo == (1,0):

				mjj_histos['mjjHistWithSelectedEvents_twoCentralJets'].Fill(mjj_values['leadingJet_trailingJet'])

		elif jet_geometry == 'Mixed':
			
			mjj_histos['mjjHistWithAllEvents_mixed'].Fill(mjj_values['leadingJet_trailingJet'])
			
			if maxCombo == (0,1) or maxCombo == (1,0):

				mjj_histos['mjjHistWithSelectedEvents_mixed'].Fill(mjj_values['leadingJet_trailingJet'])


def main():

	#Define the necessary histograms for ratio plots
	mjj_histos = defineHistosForRatioPlot()

	for hist in mjj_histos.values():

		hist.SetDirectory(0)

	f = file('inputs/MiniAOD_files2017.txt', 'r')

	for numFile, fileName in enumerate(f.readlines()):

		print('Working on file {}'.format(numFile+1))
		
		#if numFile == 2: break #For testing

		getFractionPlot_mjj(fileName, mjj_histos)

	constructRatioPlot(mjj_histos['mjjHistWithSelectedEvents_twoCentralJets'], mjj_histos['mjjHistWithAllEvents_twoCentralJets'])

if __name__ == '__main__':

	main()



