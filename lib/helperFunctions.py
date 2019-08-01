import ROOT
from math import pi

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

def invMassTwoJets(jets_):
	
	'''
	Calculates the invariant mass of two leading jets in the event.
	'''
	
	leadingJet = jets_[0]
	trailingJet = jets_[1]
	
	total_p4 = leadingJet.p4() + trailingJet.p4()

	mjj = total_p4.M()

	return mjj


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
