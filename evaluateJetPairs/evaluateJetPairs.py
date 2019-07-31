import ROOT
import numpy as np
from lib.defineHistos import define2DHistos
from lib.helperFunctions import *

# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events	

def getFracOfEvents_mjj():

	'''
	Constructs the graph showing the fraction of events where leading jet pair coincides with highest mjj pair.
	Also takes into account two seperate categories:
	--Two central jets
	--Mixed (one central, one forward jet)
	'''
	#No stat box in the histograms
	
	ROOT.gStyle.SetOptStat(0)
	
	jets, jetLabel = Handle('std::vector<pat::Jet>'), 'slimmedJets'

	events = Events('root://cmsxrootd.fnal.gov///store/mc/RunIIFall17MiniAODv2/VBF_HToInvisible_M125_13TeV_TuneCP5_powheg_pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/00000/14347E60-56F2-E811-81F4-24BE05C6C7E1.root')

	#######################
	#Defining relevant histograms
	#######################

	mjj_array = np.arange(500., 2500., 50.)

	mjj_histWithAllEvents_twoCentralJets = ROOT.TH1F('mjj_histWithAllEvents_twoCentralJets', 'mjj_histWithAllEvents_twoCentralJets', len(mjj_array)-1, mjj_array)
	mjj_histWithAllEvents_mixed = ROOT.TH1F('mjj_histWithAllEvents_mixed', 'mjj_histWithAllEvents_mixed', len(mjj_array)-1, mjj_array)

	#These histograms only contain the events with highest mjj pair coinciding with the leading jet pair
	mjj_histWithSelectedEvents_twoCentralJets = ROOT.TH1F('mjj_histWithSelectedEvents_twoCentralJets', 'mjj_histWithSelectedEvents_twoCentralJets', len(mjj_array)-1, mjj_array)
	mjj_histWithSelectedEvents_mixed = ROOT.TH1F('mjj_histWithSelectedEvents_mixed', 'mjj_histWithSelectedEvents_mixed', len(mjj_array)-1, mjj_array)

	#######################
	#Event loop starts here
	#######################

	for iev, event in enumerate(events):

		#if iev == 1000: break #For testing

		if iev % 1000 == 0:
			print('Working on event {}'.format(iev))

		event.getByLabel(jetLabel, jets)

		######################
		#Implementing tight jet ID, 2017 recommendations
		######################
	
		jets_ = jets.product()

		AK4_tightJets = []
		
		for jet in jets_:

			if isTightJet(jet):			
	
				AK4_tightJets.append(jet) 

		nJet = len(AK4_tightJets)

		if nJet < 2: continue #Discard the events with number of jets smaller than 2
		
		mjj_values = invMassJetCombos(AK4_tightJets) #Get all the mjj values for all possible combos

		maxCombo = getMaxCombo(mjj_values) #Get the jet pair for which the maximum mjj happens to be

		jet_geometry = getJetGeometry(AK4_tightJets[0], AK4_tightJets[1]) #Determine the geometry of two leading jets

		if jet_geometry == 'Two Central Jets':
		
			mjj_histWithAllEvents_twoCentralJets.Fill(mjj_values['leadingJet_trailingJet'])
		
			if maxCombo == (0,1) or maxCombo == (1,0):

				mjj_histWithSelectedEvents_twoCentralJets.Fill(mjj_values['leadingJet_trailingJet'])

		elif jet_geometry == 'Mixed':
			
			mjj_histWithAllEvents_mixed.Fill(mjj_values['leadingJet_trailingJet'])
			
			if maxCombo == (0,1) or maxCombo == (1,0):

				mjj_histWithSelectedEvents_mixed.Fill(mjj_values['leadingJet_trailingJet'])

	########################
	#Construct the histograms containing ratios of the events
	########################
	
	ratioHist_twoCentralJets = mjj_histWithSelectedEvents_twoCentralJets.Clone()
	ratioHist_twoCentralJets.Divide(mjj_histWithAllEvents_twoCentralJets) #Divide the two histograms
	ratioHist_twoCentralJets.GetXaxis().SetTitle('mjj (GeV)')
	ratioHist_twoCentralJets.GetYaxis().SetTitle('Ratio of Events')

	ratioHist_mixed = mjj_histWithSelectedEvents_mixed.Clone()
	ratioHist_mixed.Divide(mjj_histWithAllEvents_mixed) #Divide the two histograms
	ratioHist_mixed.GetXaxis().SetTitle('mjj (GeV)')
	ratioHist_mixed.GetYaxis().SetTitle('Ratio of Events')

	printHisto(ratioHist_twoCentralJets)
	printHisto(ratioHist_mixed) 	

def fill2DHistos(histo_dict):

	'''
	Given the dict containing all histograms, fills the histograms by doing an event loop.
	'''
	#No stat box in the histograms
	
	ROOT.gStyle.SetOptStat(0)

	mjj_histo = histo_dict['mjj_histo']
	leadJetPt_histo = histo_dict['leadJetPt_histo']
	trailJetPt_histo = histo_dict['trailJetPt_histo']
	leadJetEta_histo = histo_dict['leadJetEta_histo']
	trailJetEta_histo = histo_dict['trailJetEta_histo']

	jets, jetLabel = Handle('std::vector<pat::Jet>'), 'slimmedJets'

	events = Events('root://cmsxrootd.fnal.gov///store/mc/RunIIFall17MiniAODv2/VBF_HToInvisible_M125_13TeV_TuneCP5_powheg_pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/00000/14347E60-56F2-E811-81F4-24BE05C6C7E1.root')

	#######################
	#Event loop starts here
	#######################

	for iev, event in enumerate(events):

		#if iev == 1000: break #For testing

		if iev % 1000 == 0:
			print('Working on event {}'.format(iev))

		event.getByLabel(jetLabel, jets)

		######################
		#Implementing tight jet ID, 2017 recommendations
		######################
	
		jets_ = jets.product()

		AK4_tightJets = []
		
		for jet in jets_:

			if isTightJet(jet):			
	
				AK4_tightJets.append(jet) 

		nJet = len(AK4_tightJets)

		if nJet < 2: continue #Discard the events with number of jets smaller than 2
		
		mjj_values = invMassJetCombos(AK4_tightJets) #Get all the mjj values for all possible combos

		maxCombo = getMaxCombo(mjj_values) #Get the jet pair for which the maximum mjj happens to be

		#################################
		#In the following, max_ variables stand for "the pair with highest mjj"
		#In contrast, leadingPair_ stands for "the highest pt jet pair"
		#################################
		
		leadingPair_mjj = mjj_values['leadingJet_trailingJet']
		leadingPair_leadJetPt = AK4_tightJets[0].pt()
		leadingPair_trailJetPt = AK4_tightJets[1].pt()
		leadingPair_leadJetEta = AK4_tightJets[0].eta()
		leadingPair_trailJetEta = AK4_tightJets[1].eta()

		if maxCombo == (0, 1):
		
			max_mjj = leadingPair_mjj 
			max_leadJetPt = leadingPair_leadJetPt 
			max_trailJetPt = leadingPair_trailJetPt 
			max_leadJetEta = leadingPair_leadJetEta 
			max_trailJetEta = leadingPair_trailJetEta 

		else:
			
			max_mjj = mjj_values['otherCombos'][maxCombo]
			
			#Identify the jet with larger pt in the max mjj combo

			idx_jetWithLargerPt, idx_jetWithSmallerPt = sortJets(AK4_tightJets, maxCombo)

			max_leadJetPt = AK4_tightJets[idx_jetWithLargerPt].pt()
			max_trailJetPt = AK4_tightJets[idx_jetWithSmallerPt].pt()
			max_leadJetEta = AK4_tightJets[idx_jetWithLargerPt].eta()
			max_trailJetEta = AK4_tightJets[idx_jetWithSmallerPt].eta()

		mjj_histo.Fill(max_mjj, leadingPair_mjj)
		leadJetPt_histo.Fill(max_leadJetPt, leadingPair_leadJetPt)
		trailJetPt_histo.Fill(max_trailJetPt, leadingPair_trailJetPt)
		leadJetEta_histo.Fill(max_leadJetEta, leadingPair_leadJetEta)
		trailJetEta_histo.Fill(max_trailJetEta, leadingPair_trailJetEta)

	#Plot the histograms and save them
	
	for hist in histo_dict.values():

		print2DHisto(hist)


def count():

	'''
	Counts the number of events where one of two scenarios occur:
	--- Max mjj is for two leading jets
	--- Max mjj is for other jet combos
	Counts the number of events for three cases for leading two jets:
	--- Two central jets
	--- Two forward jets
	--- Mixed (one central, one forward jet)
	'''
	
	jets, jetLabel = Handle('std::vector<pat::Jet>'), 'slimmedJets'

	events = Events('root://cmsxrootd.fnal.gov///store/mc/RunIIFall17MiniAODv2/VBF_HToInvisible_M125_13TeV_TuneCP5_powheg_pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/00000/14347E60-56F2-E811-81F4-24BE05C6C7E1.root')

	mother_dict = {}
	
	counter_twoLeadingJets = {} #Counts the number of events where mjj is max for the two leading jets
	counter_otherCombos = {} #Counts the number of events where mjj is max for other combinations

	mjjValues_leadingPair = [] #Stores max mjj for the case where max mjj comes from leading two pairs
	mjjValues_otherMaxPair = [] #Stores max mjj for the case where max mjj comes from other combos

	ptValues1_leadingPair = [] #Stores jet_pt[0] for the case where max mjj comes from leading two pairs 
	ptValues2_leadingPair = [] #Stores jet_pt[1] for the case where max mjj comes from leading two pairs 

	leadingJetPtValues_otherMaxPair = [] #Stores jet_pt[0] for the case where max mjj comes from other combos
	trailingJetPtValues_otherMaxPair = [] #Stores jet_pt[1] for the case where max mjj comes from other combos
	ptValues1_otherMaxPair = [] #Stores jet_pt of jet with larger pt in the case where this pair have the max mjj 
	ptValues2_otherMaxPair = [] #Stores jet_pt of jet with smaller pt in the case where this pair have the max mjj 

	cases = ['twoCentralJets', 'twoForwardJets', 'mixed']		

	for case in cases:
		counter_twoLeadingJets[case] = 0
		counter_otherCombos[case] = 0

	mother_dict['counter_twoLeadingJets'] = counter_twoLeadingJets
	mother_dict['counter_otherCombos'] = counter_otherCombos
	mother_dict['mjjValues_leadingPair'] = mjjValues_leadingPair
	mother_dict['mjjValues_otherMaxPair'] = mjjValues_otherMaxPair
	mother_dict['ptValues1_leadingPair'] = ptValues1_leadingPair
	mother_dict['ptValues2_leadingPair'] = ptValues2_leadingPair
	mother_dict['leadingJetPtValues_otherMaxPair'] = leadingJetPtValues_otherMaxPair
	mother_dict['trailingJetPtValues_otherMaxPair'] = trailingJetPtValues_otherMaxPair
	mother_dict['ptValues1_otherMaxPair'] = ptValues1_otherMaxPair	
	mother_dict['ptValues2_otherMaxPair'] = ptValues2_otherMaxPair	

	#####################
	#Event loop starts here
	#####################

	for iev, event in enumerate(events):

		#if iev == 10: break #For testing

		if iev % 1000 == 0:
			print('Working on event {}'.format(iev))

		event.getByLabel(jetLabel, jets)

		######################
		#Implementing tight jet ID, 2017 recommendations
		######################
	
		jets_ = jets.product()

		AK4_tightJets = []
		
		for jet in jets_:

			if isTightJet(jet):			
	
				AK4_tightJets.append(jet) 

		nJet = len(AK4_tightJets)

		if nJet < 2: continue #Discard the events with number of jets smaller than 2

		mjj_values = invMassJetCombos(AK4_tightJets) #Get all the mjj values for all possible combos

		maxCombo = getMaxCombo(mjj_values) #Get the jet pair for which the maximum mjj happens to be

		#print('Event: {0}, maxCombo: {1}'.format(iev, maxCombo))
	
		####################
		#Counting the number of cases
		####################

		leadJetEta = AK4_tightJets[0].eta()
		trailJetEta = AK4_tightJets[1].eta()

		if abs(leadJetEta) > 2.5 and abs(trailJetEta) > 2.5: 
			case = 'twoForwardJets'
		elif abs(leadJetEta) <= 2.5 and abs(trailJetEta) <= 2.5: 
			case = 'twoCentralJets'
		else: 
			case = 'mixed'
	
		if maxCombo == (0, 1): 
			
			counter_twoLeadingJets[case] += 1	 
			mjjValues_leadingPair.append(mjj_values['leadingJet_trailingJet'])			
			ptValues1_leadingPair.append(AK4_tightJets[0].pt()) 			
			ptValues2_leadingPair.append(AK4_tightJets[1].pt()) 			

		else:

			counter_otherCombos[case] += 1
			mjjValues_otherMaxPair.append(mjj_values['otherCombos'][maxCombo])

			leadingJetPtValues_otherMaxPair.append(AK4_tightJets[0].pt())
			trailingJetPtValues_otherMaxPair.append(AK4_tightJets[1].pt())

			jet_idx1, jet_idx2 = maxCombo[0], maxCombo[1]
			
			if AK4_tightJets[jet_idx1].pt() > AK4_tightJets[jet_idx2].pt():
				
				ptValues1_otherMaxPair.append(AK4_tightJets[jet_idx1].pt())
				ptValues2_otherMaxPair.append(AK4_tightJets[jet_idx2].pt())
		
			else:

				ptValues2_otherMaxPair.append(AK4_tightJets[jet_idx1].pt())
				ptValues1_otherMaxPair.append(AK4_tightJets[jet_idx2].pt())
	

	return mother_dict 
		
def main():

	#mother_dict = count()
	
	#Get the dictionary containing the definitions of 2D histograms
	#histo_dict = define2DHistos()

	#fill2DHistos(histo_dict)

	getFracOfEvents_mjj()

#	counter_twoLeadingJets = mother_dict['counter_twoLeadingJets']
#	counter_otherCombos = mother_dict['counter_otherCombos']
#	mjjValues_leadingPair = mother_dict['mjjValues_leadingPair']
#	mjjValues_otherMaxPair = mother_dict['mjjValues_otherMaxPair']
#	ptValues1_leadingPair = mother_dict['ptValues1_leadingPair']
#	ptValues2_leadingPair = mother_dict['ptValues2_leadingPair']
#	leadingJetPtValues_otherMaxPair = mother_dict['leadingJetPtValues_otherMaxPair']
#	trailingJetPtValues_otherMaxPair = mother_dict['trailingJetPtValues_otherMaxPair']
#	ptValues1_otherMaxPair = mother_dict['ptValues1_otherMaxPair']
#	ptValues2_otherMaxPair = mother_dict['ptValues2_otherMaxPair']
#
#	print('*'*10)
#	print('RESULTS')
#	print('*'*10)
#	print('\nTotal number of events with max mjj belonging to two leading jets  : {}'.format(counter_twoLeadingJets['mixed'] + counter_twoLeadingJets['twoForwardJets'] + counter_twoLeadingJets['twoCentralJets']))
#	print('--- Number of events in two forward jets category                  : {}'.format(counter_twoLeadingJets['twoForwardJets']))
#	print('--- Number of events in two central jets category                  : {}'.format(counter_twoLeadingJets['twoCentralJets']))
#	print('--- Number of events in mixed category                             : {}'.format(counter_twoLeadingJets['mixed']))
#
#	print('\nTotal number of events with max mjj belonging to other jet combos  : {}'.format(counter_otherCombos['mixed'] + counter_otherCombos['twoForwardJets'] + counter_otherCombos['twoCentralJets']))
#	print('--- Number of events in two forward jets category                  : {}'.format(counter_otherCombos['twoForwardJets']))
#	print('--- Number of events in two central jets category                  : {}'.format(counter_otherCombos['twoCentralJets']))
#	print('--- Number of events in mixed category                             : {}'.format(counter_otherCombos['mixed']))
#
#	print('*'*10)

if __name__ == '__main__':

	main()

	




	
	

