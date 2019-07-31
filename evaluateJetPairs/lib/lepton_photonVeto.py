import ROOT

def containsLooseElectron(electrons_):

	'''
	Returns True if there is at least one electron that passes 2017 loose ID requirements in the given electrons_ set.
	Otherwise, returns False.
	'''

	looseElectron = False

	for el in electrons_:

		if el.electronID('cutBasedElectronID-Spring15-25ns-V1-standalone-loose') == 1. and el.pt() > 10 and abs(el.eta()) < 2.5:

			looseElectron = True

	return looseElectron

def containsLooseMuon(muons_):
	
	'''
	Returns True if there is at least one muon that passes 2017 loose ID requirements in the given muons_ set.
	Otherwise, returns False.
	'''
	
	looseMuon = False

	for mu in muons_:

		if (mu.isGlobalMuon() or mu.isTrackerMuon()) and mu.isPFMuon() and mu.pt() > 5: 

			looseMuon = True

	return looseMuon

def containsLooseTau(taus_):
	
	'''
	Returns True if there is at least one tau that passes 2017 loose ID requirements in the given taus_ set.
	Otherwise, returns False.
	'''

	looseTau = False

	for tau in taus_:

		if tau.pt() > 20 and abs(tau.eta()) < 2.3:
	
			looseTau = True

	return looseTau

def containsLoosePhoton(photons_):

	'''
	Returns True if there is at least one photon that passes 2017 loose ID requirements in the given photons_ set.
	Otherwise, returns False.
	'''
	
	loosePhoton = False

	for ph in photons_:

		if ph.photonID('PhotonCutBasedIDLoose') == 1 and abs(ph.eta()) < 2.5 and ph.pt() > 15:
	
			loosePhoton = True

	return loosePhoton

def containsLeptonOrPhoton(electrons, muons, taus, photons):

	'''
	Wrapper function to apply lepton and photon veto to an event, given the relevant sets of objects.
	Returns True if there are no loose photon/leptons found in the event, otherwise returns False.
	'''

	electrons_ = electrons.product()
	muons_ = muons.product()
	taus_ = taus.product()
	photons_ = photons.product()
 
	contains_lepton_photon = containsLooseElectron(electrons_) and containsLooseMuon(muons_) and containsLooseTau(taus_) and containsLoosePhoton(photons_)

	return contains_lepton_photon


 
