import ROOT
from math import pi

def minJetMETPhi(jets_, mets_):

	'''
	Calculates the minimum phi difference between four leading jets and MET.
	If there are less than four jets in the event, it calculates the minimum phi difference by looking at all the jets.
	'''

	phiDiffList = []	
	met = mets_[0]

	if len(jets_) <= 4:
		for j in jets_:

			if j.pt() < 30: continue
			phi_diff = abs(j.phi() - met.phi())
			
			if phi_diff <= pi:
				phiDiffList.append(phi_diff)

			else:
				phiDiffList.append(2*pi - phi_diff)

	else:
		for i in range(4): #Take only the first four leading jets

			if jets_[i].pt() < 30: continue
			phi_diff = abs(jets_[i].phi() - met.phi())
			
			if phi_diff <= pi:
				phiDiffList.append(phi_diff)

			else:
				phiDiffList.append(2*pi - phi_diff)

	if phiDiffList:

		return min(phiDiffList)

	return -1.0 #These events will not pass 	

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
	mjj_values = {}

	mjj_values['leadingJet_trailingJet'] = invMassTwoJets(jets_[0], jets_[1])
	mjj_values['otherCombos'] = {}

	for i in range(numJets):

		for j in range(numJets):

			if not ((i==1 and j==0) or (i==0 and j==1)): 

				if i == j: continue

				if ((i,j) in mjj_values['otherCombos'].keys() or (j, i) in mjj_values['otherCombos'].keys()): continue 

				invMass = invMassTwoJets(jets_[i], jets_[j])

				mjj_values['otherCombos'][(i, j)] = invMass

	return mjj_values

def getMaxCombo(mjj_values):

	'''
	Given mjj_values dict, containing all possible mjj combos, determines the max mjj and which combo it belongs to.
	'''
	mjjMax_jetCombo = (0, 1) #By default, the two leading jets
	max_mjj = mjj_values['leadingJet_trailingJet']

	try:
		
		for key, mjj_value in mjj_values['otherCombos'].items():

			if mjj_value > max_mjj: 

				mjjMax_jetCombo = key 
				max_mjj = mjj_value

		#print(mjjMax_jetCombo)

		return mjjMax_jetCombo
	
	except IndexError:

		return mjjMax_jetCombo

def sortJets(jets_list, combo):
	
	'''
	Given the list of jets and indices of two jets in combo, sorts the jets with respect to pt and returns the indices.
	Larger index is returned first.
	'''
	
	if jets_list[combo[0]].pt() > jets_list[combo[1]].pt():

		idx_jetWithLargerPt, idx_jetWithSmallerPt = combo[0], combo[1]
	
	else:
		
		idx_jetWithLargerPt, idx_jetWithSmallerPt = combo[1], combo[0]

	return idx_jetWithLargerPt, idx_jetWithSmallerPt

def printHisto(hist):

	'''
	Given 1D histogram, crates a canvas and plots the histogram.
	It then saves the file as a png.
	'''

	canv = ROOT.TCanvas('canv')

	hist.Draw()
	
	geometry = hist.GetName().split('_')[-1]
	fileName = 'ratioPlot_' + geometry + '.png'

	canv.Print(fileName)

def print2DHisto(hist):

	'''
	Given the histogram, creates a canvas and plots the histogram as a 2D colormap. 
	It then saves the file as a png.
	'''

	canv = ROOT.TCanvas('canv')
	
	hist.Draw('COLZ')
	canv.SetLogz(1)
	histo_variable = hist.GetName().split('_')[0]

	fileName = histo_variable + '.png'	

	canv.Print(fileName)

def getJetGeometry(jet1, jet2):

	'''
	Given the leading two jets, determines whether:
	--Both of them are central
	--One is central and one is forward
	--Both of them are forward
	Returns a string that contains information about the jet geometry.
	'''

	if abs(jet1.eta()) <= 2.5 and abs(jet2.eta()) <= 2.5: return 'Two Central Jets'

	elif abs(jet1.eta()) > 2.5 and abs(jet2.eta()) > 2.5: return 'Two Forward Jets'

	else: return 'Mixed'


def isTightJet(jet):

	'''
	Returns True if the given jet passes the tight ID requirements (2017).
	Otherwise, returns False.
	'''
	if abs(jet.eta()) <= 2.7:

		if jet.nConstituents() <= 1: return False

		if jet.neutralHadronEnergyFraction() >= 0.9: return False

		if jet.neutralEmEnergyFraction() >= 0.9: return False
		
		if abs(jet.eta()) <= 2.4:

			if jet.chargedHadronEnergyFraction() <= 0: return False

			if jet.chargedMultiplicity() <= 0: return False

	if 2.7 < abs(jet.eta()) <= 3.0:

		if not 0.02 < jet.neutralEmEnergyFraction() < 0.99: return False

		if jet.neutralMultiplicity() <= 2: return False

	if abs(jet.eta()) > 3.0:

		if jet.neutralEmEnergyFraction() > 0.9: return False

		if jet.neutralHadronEnergyFraction() <= 0.02: return False

		if jet.neutralMultiplicity() <= 10: return False

	return True
