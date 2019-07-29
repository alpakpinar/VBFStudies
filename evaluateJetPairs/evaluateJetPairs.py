import ROOT

# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events	

def invMassTwoJets(jet1, jet2):
	
	'''
	Calculate invariant mass of any given two jets.
	'''

	total_p4 = jet1.p4() + jet2.p4()

	mjj = total_p4.M()

	return mjj

def invMassJetCombos(jets_):
	
	'''
	Calculates invariant mass of all jet combinations and stores them in a dict.
	Returns the dict.
	'''

	numJets = len(jets_)
	print('Number of jets: {}'.format(numJets))
	mjj_values = {}

	mjj_values['leadingJet_trailingJet'] = invMassTwoJets(jets_[0], jets_[1])
	mjj_values['otherCombos'] = []

	for i in range(numJets):

		for j in range(numJets):

			if not ((i==1 and j==0) or (i==0 and j==1)): 

				if i == j: continue

				invMass = invMassTwoJets(jets_[i], jets_[j])

				mjj_values['otherCombos'].append(invMass)

	print('leadingJet_trailingJet_mjj: {}'.format(mjj_values['leadingJet_trailingJet']))

	if len(mjj_values['otherCombos']) != 0:
		print('max mjj from other combos: {}'.format(max(mjj_values['otherCombos'])))
	else:
		print('max mjj from other combos: None') 


	print('Jet_eta[0]: {}'.format(jets_[0].eta()))
	print('Jet_eta[1]: {}'.format(jets_[1].eta()))
	
	return mjj_values

def getMaxCombo(mjj_values):

	'''
	Given mjj_values dict, containing all possible mjj combos, determines the max mjj and which combo it belongs to.
	'''

	max_mjj = None
	max_mjj_case = None

	mjjMax_leadingCase = True
	
	for mjj_val in mjj_values['otherCombos']:

		if mjj_val > mjj_values['leadingJet_trailingJet']: mjjMax_leadingCase = False

	if mjjMax_leadingCase: return 'Leading+Trailing'

	else: return 'Other Combo'

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
	
	counter_twoLeadingJets = {} #Counts the number of events where mjj is max for the two leading jets
	counter_otherCombos = {} #Counts the number of events where mjj is max for other combinations

	cases = ['twoCentralJets', 'twoForwardJets', 'mixed']		

	for case in cases:
		counter_twoLeadingJets[case] = 0
		counter_otherCombos[case] = 0

	#####################
	#Event loop starts here
	#####################

	for iev, event in enumerate(events):

		if iev == 3: break

		event.getByLabel(jetLabel, jets)

		######################
		#Implementing tight jet ID, 2017 recommendations
		######################
	
		jets_ = jets.product()

		AK4_tightJets = []
		
		for i, jet in enumerate(jets_):

			if abs(jet.eta()) <= 2.7:

				if jet.nConstituents() <= 1: continue

				if jet.neutralHadronEnergyFraction() >= 0.9: continue

				if jet.neutralEmEnergyFraction() >= 0.9: continue
				
				if abs(jet.eta()) <= 2.4:

					if jet.chargedHadronEnergyFraction() <= 0: continue

					if jet.chargedMultiplicity() <= 0: continue

					AK4_tightJets.append(jet)			

				else: AK4_tightJets.append(jet)
					
			if 2.7 < abs(jet.eta()) <= 3.0:

				if not 0.02 < jet.neutralEmEnergyFraction() < 0.99: continue

				if jet.neutralMultiplicity() <= 2: continue

				AK4_tightJets.append(jet)

			if abs(jet.eta()) > 3.0:

				if jet.neutralEmEnergyFraction() > 0.9: continue

				if jet.neutralHadronEnergyFraction() <= 0.02: continue
		
				if jet.neutralMultiplicity() <= 10: continue

				AK4_tightJets.append(jet) 

		nJet = len(AK4_tightJets)
		
		if nJet < 2: continue #Discard the events with number of jets smaller than 2

		mjj_values = invMassJetCombos(AK4_tightJets) #Get all the mjj values for all possible combos

		maxCase = getMaxCombo(mjj_values) #Get the case where maximum mjj happens to be

		print('Event: {0}, maxCase: {1}'.format(iev, maxCase))
	
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
	
		if maxCase == 'Leading+Trailing':
			
			counter_twoLeadingJets[case] += 1	 
		
		elif maxCase == 'Other Combo': 

			counter_otherCombos[case] += 1

	return counter_twoLeadingJets, counter_otherCombos
		
def main():

	counter_twoLeadingJets, counter_otherCombos = count()

	print('*'*10)
	print('RESULTS')
	print('*'*10)
	print('\nTotal number of events with max mjj belonging to two leading jets: {}'.format(counter_twoLeadingJets['mixed'] + counter_twoLeadingJets['twoForwardJets'] + counter_twoLeadingJets['twoCentralJets']))
	print('--- Number of events in two forward jets category                  : {}'.format(counter_twoLeadingJets['twoForwardJets']))
	print('--- Number of events in two central jets category                  : {}'.format(counter_twoLeadingJets['twoCentralJets']))
	print('--- Number of events in mixed category                             : {}'.format(counter_twoLeadingJets['mixed']))

	print('\nTotal number of events with max mjj belonging to other jet combos: {}'.format(counter_otherCombos['mixed'] + counter_otherCombos['twoForwardJets'] + counter_otherCombos['twoCentralJets']))
	print('--- Number of events in two forward jets category                  : {}'.format(counter_otherCombos['twoForwardJets']))
	print('--- Number of events in two central jets category                  : {}'.format(counter_otherCombos['twoCentralJets']))
	print('--- Number of events in mixed category                             : {}'.format(counter_otherCombos['mixed']))

	print('*'*10)

if __name__ == '__main__':

	main()

	




	
	

