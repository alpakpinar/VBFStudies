import ROOT
import time
import argparse
import os 
from math import pi 

from lib.vbf_tree_2017 import * 

# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events	
	
def invMassTwoJets(jets_):
	
	'''
	Calculates the invariant mass of two leading jets in the event.
	If there are less than two jets in the event, returns 0. 
	'''

	try:
	
		leadingJet = jets_[0]
		trailingJet = jets_[1]
		
		total_p4 = leadingJet.p4() + trailingJet.p4()

		mjj = total_p4.M()

		return mjj

	except IndexError:
		
		print('Event has less than 2 jets!')
		
		return 0

def minJetMETPhi(jets, mets):

	'''
	Calculates the minimum phi difference between four leading jets and MET.
	If there are less than four jets in the event, it calculates the minimum phi difference by looking at all the jets.
	'''

	jets_ = jets.product()
	met = mets.product()[0]
	phiDiffList = []	

	if len(jets_) <= 4:
		for j in jets_:
			phi_diff = abs(j.phi() - met.phi())
			
			if phi_diff <= pi:
				phiDiffList.append(phi_diff)

			else:
				phiDiffList.append(2*pi - phi_diff)

	else:
		for i in range(4): #Take only the first four leading jets
			phi_diff = abs(jets_[i].phi() - met.phi())
			
			if phi_diff <= pi:
				phiDiffList.append(phi_diff)

			else:
				phiDiffList.append(2*pi - phi_diff)

	return min(phiDiffList)


def writeTree(inputFile, tree, args):
	
	electrons, electronLabel = Handle('std::vector<pat::Electron>'), 'slimmedElectrons'
	muons, muonLabel = Handle('std::vector<pat::Muon>'), 'slimmedMuons'
	taus, tauLabel = Handle('std::vector<pat::Tau>'), 'slimmedTaus'
	photons, photonLabel = Handle('std::vector<pat::Photon>'), 'slimmedPhotons'
	jets, jetLabel = Handle('std::vector<pat::Jet>'), 'slimmedJets'
	mets, metLabel = Handle('std::vector<pat::MET>'), 'slimmedMETs'
	genParticles, genParticlesLabel = Handle('std::vector<reco::GenParticle>'), 'prunedGenParticles'

	triggerBits, triggerBitLabel = Handle("edm::TriggerResults"), ("TriggerResults","","HLT")
	filters, filterLabel = Handle("edm::TriggerResults"), 'TriggerResults' 

	triggerObjects, triggerObjectLabel  = Handle("std::vector<pat::TriggerObjectStandAlone>"), "slimmedPatTrigger"
	triggerPrescales, triggerPrescaleLabel  = Handle("pat::PackedTriggerPrescales"), "patTrigger"
	l1Jets, l1JetLabel  = Handle("BXVector<l1t::Jet>"), "caloStage2Digis:Jet"
	l1EtSums, l1EtSumLabel  = Handle("BXVector<l1t::EtSum>"), "caloStage2Digis:EtSum"

	events = Events(inputFile)

	print('Took the input file successfully')

	t1 = time.time()

	for numEvent, event in enumerate(events):

		if args.shortTest:
			
			if numEvent == 100: break

		event.getByLabel(electronLabel, electrons)
		event.getByLabel(muonLabel, muons)
		event.getByLabel(tauLabel, taus)
		event.getByLabel(photonLabel, photons)
		event.getByLabel(jetLabel, jets)
		event.getByLabel(metLabel, mets)
		event.getByLabel(genParticlesLabel, genParticles)

		event.getByLabel(triggerBitLabel, triggerBits)
		event.getByLabel(filterLabel, filters)
		event.getByLabel(triggerObjectLabel, triggerObjects)
		event.getByLabel(triggerPrescaleLabel, triggerPrescales)
		event.getByLabel(l1JetLabel, l1Jets)
		event.getByLabel(l1EtSumLabel, l1EtSums)

		t2 = time.time()

#		if numEvent % 100 == 0 and numEvent != 0:		
#			print('Analyzing event # %d , Time: %.2f' % (numEvent , t2-t1))
	
		#Storing kinemaic values of interest	
		
		met[0] = mets.product()[0].pt()
		met_phi[0] = mets.product()[0].phi()
		met_eta[0] = mets.product()[0].eta()

		if met[0] < 50: continue

		jets_ = jets.product()

		nJet[0] = len(jets_)
		mjj[0] = invMassTwoJets(jets_)

		for i, jet in enumerate(jets_):

			jet_pt[i] = jet.pt()
			jet_energy[i] = jet.energy()
			jet_eta[i] = jet.eta()
			jet_phi[i] = jet.phi()
			jet_px[i] = jet.px()
			jet_py[i] = jet.py()
			jet_pz[i] = jet.pz()	
			
			#Getting b-tag information for each jet
			tags = jet.getPairDiscri()

			for tag in tags:

				if tag.first == 'pfCombinedSecondaryVertexV2BJetTags':
	
					jet_btag_CSVv2[i] = tag.second
	
		num_bJets = 0

		for val in jet_btag_CSVv2:

			if val > 0.8484: #2017 requirements

				num_bJets += 1 

		if num_bJets != 0:
			
			contains_bJet = 1

		else: contains_bJet = 0

		try:

			absEtaDiff_leadingTwoJets[0] = abs(jet_eta[0] - jet_eta[1])

		except IndexError:

			print('Event contains less than 2 jets!')
			absEtaDiff_leadingTwoJets[0] = 0

		minPhi_jetMET[0] = minJetMETPhi(jets, mets) #Minimum delta_phi between jets and MET
	
		if jet_pt[0] < 50: continue

		###################

		electrons_ = electrons.product()

		nElectron[0] = 0
	
		for el in electrons_:
	
			if el.electronID('cutBasedElectronID-Spring15-25ns-V1-standalone-loose') == 1. and el.pt() > 10 and abs(el.eta()) < 2.5:
	
				electron_pt[nElectron[0]] = el.pt()
				electron_eta[nElectron[0]] = el.eta()
				electron_phi[nElectron[0]] = el.phi()
				nElectron[0] += 1		

		muons_ = muons.product()

		nMuon[0] = 0

		for mu in muons_:

			if (mu.isGlobalMuon() or mu.isTrackerMuon()) and mu.isPFMuon() and mu.pt() > 5: #Iso requirement will be added 
	
				muon_pt[nMuon[0]] = mu.pt()
				muon_eta[nMuon[0]] = mu.eta()
				muon_phi[nMuon[0]] = mu.phi()
				nMuon[0] += 1

		taus_ = taus.product()

		nTau[0] = 0

		for tau in taus_:

			if tau.pt() > 20 and abs(tau.eta()) < 2.3: #decayModeFindingNewDMs already implemented by MiniAOD
	
				tau_pt[nTau[0]] = tau.pt()
				tau_eta[nTau[0]] = tau.eta()
				tau_phi[nTau[0]] = tau.phi()
				nTau[0] += 1

		#Filling out the branch for lepton veto

		if nElectron[0] + nMuon[0] + nTau[0] != 0:

			containsLepton[0] = 1

		else: containsLepton[0] = 0

		photons_ = photons.product()

		nPhoton[0] = 0
		
		for ph in photons_:

			if ph.photonID('PhotonCutBasedIDLoose') == 1 and abs(ph.eta()) < 2.5 and ph.pt() > 15:

				photon_pt[nPhoton[0]] = ph.pt()
				photon_eta[nPhoton[0]] = ph.eta()
				photon_phi[nPhoton[0]] = ph.phi()
				nPhoton[0] += 1
	
		if nPhoton[0] != 0: containsPhoton[0] = 1

		else: containsPhoton[0] = 0
		
		##################

		genParticles_ = genParticles.product()

		nParticles[0] = len(genParticles_)
	
		for j, prt in enumerate(genParticles_):

			pdgId[j] = prt.pdgId()
			#mothers[i] = prt.mother()
		
		triggerBits_ = triggerBits.product()

		#print(type(triggerBits_))

		#print('Number of trigger paths: %d' % triggerBits_.size())

		names = event.object().triggerNames(triggerBits_)

		##########################
	
		#print(type(names))

		#print(triggerBits_.size())

		if numEvent < 2:
		
			print(names.triggerNames())

			for name in names.triggerNames():

				print(name)

		##########################		

		for k in range(triggerBits_.size()):

			#VBF DiJet triggers

			if names.triggerNames()[k] == 'HLT_DiJet110_35_Mjj650_PFMET110_v2':
				if triggerBits_.accept(k):
					HLT_DiJet110_35_Mjj650_PFMET110_v2[0] = 1
					print('In the if statement!')
					print(HLT_DiJet110_35_Mjj650_PFMET110_v2[0])
				else:
					HLT_DiJet110_35_Mjj650_PFMET110_v2[0] = 0 
					print('In the if statement!')
					print(HLT_DiJet110_35_Mjj650_PFMET110_v2[0])
 

			elif names.triggerNames()[k] == 'HLT_DiJet110_35_Mjj650_PFMET120_v2':
				if triggerBits_.accept(k):
					HLT_DiJet110_35_Mjj650_PFMET120_v2[0] = 1
				else:
					HLT_DiJet110_35_Mjj650_PFMET120_v2[0] = 0 
			
			elif names.triggerNames()[k] == 'HLT_DiJet110_35_Mjj650_PFMET130_v2':
				if triggerBits_.accept(k):
					HLT_DiJet110_35_Mjj650_PFMET130_v2[0] = 1
				else:
					HLT_DiJet110_35_Mjj650_PFMET130_v2[0] = 0 

			#MET triggers
			
			elif names.triggerNames()[k] == 'HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v13': 
				if triggerBits_.accept(k):
					HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v13[0] = 1
				else:
					HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v13[0] = 0 
		
			elif names.triggerNames()[k] == 'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v13': 
				if triggerBits_.accept(k):
					HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v13[0] = 1
				else:
					HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v13[0] = 0 

			elif names.triggerNames()[k] == 'HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v12': 
				if triggerBits_.accept(k):
					HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v12[0] = 1
				else:
					HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v12[0] = 0 
			
			elif names.triggerNames()[k] == 'HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v12': 
				if triggerBits_.accept(k):
					HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v12[0] = 1
				else:
					HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v12[0] = 0 

		#Filling L1 level information
		bxVector_jet = l1Jets.product()
		bxVector_met = l1EtSums.product()	
	
		bx=0 #Check!

		for i in range(bxVector_met.size(bx)):

			etsum_obj = bxVector_met.at(bx, i)
			
			if etsum_obj.getType() == getattr(etsum_obj, 'kMissingEt'): #Getting L1 level MET attributes
			
				L1_met[0] = etsum_obj.pt()
				L1_met_eta[0] = etsum_obj.eta()
				L1_met_phi[0] = etsum_obj.phi()

		L1_nJet[0] = bxVector_jet.size(bx)

		for i in range(bxVector_jet.size(bx)):

			jet = bxVector_jet.at(bx, i)				
			
			L1_jet_pt[i] = jet.pt()
			L1_jet_eta[i] = jet.eta()			
			L1_jet_phi[i] = jet.phi()			
			L1_jet_energy[i] = jet.energy()			
			L1_jet_px[i] = jet.px()			
			L1_jet_py[i] = jet.py()			
			L1_jet_pz[i] = jet.pz()			

		########################

		#Cleaning filters		

		filters_ = filters.product()
	
		filterNames = event.object().triggerNames(filters_)
	
		for numFilter in range(filters_.size()):

			if filterNames.triggerNames()[numFilter] == 'Flag_BadPFMuonFilter':

				if filters_.accept(numFilter): Flag_BadPFMuonFilter[0] = 1

				else: Flag_BadPFMuonFilter[0] = 0
			
			elif filterNames.triggerNames()[numFilter] == 'Flag_goodVertices':

				if filters_.accept(numFilter): Flag_goodVertices[0] = 1

				else: Flag_goodVertices[0] = 0

			elif filterNames.triggerNames()[numFilter] == 'Flag_globalSuperTightHalo2016Filter':

				if filters_.accept(numFilter): Flag_globalSuperTightHalo2016Filter[0] = 1

				else: Flag_globalSuperTightHalo2016Filter[0] = 0

			elif filterNames.triggerNames()[numFilter] == 'Flag_HBHENoiseFilter':

				if filters_.accept(numFilter): Flag_HBHENoiseFilter[0] = 1

				else: Flag_HBHENoiseFilter[0] = 0

			elif filterNames.triggerNames()[numFilter] == 'Flag_HBHENoiseIsoFilter':

				if filters_.accept(numFilter): Flag_HBHENoiseIsoFilter[0] = 1

				else: Flag_HBHENoiseIsoFilter[0] = 0

			elif filterNames.triggerNames()[numFilter] == 'Flag_EcalDeadCellTriggerPrimitiveFilter':

				if filters_.accept(numFilter): Flag_EcalDeadCellTriggerPrimitiveFilter[0] = 1

				else: Flag_EcalDeadCellTriggerPrimitiveFilter[0] = 0

		tree.Fill()

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--test', help = 'Only go over the first file for testing', action = 'store_true')
	parser.add_argument('-s', '--shortTest', help = 'Only go over the first 100 events in the first file for testing', action = 'store_true')
	args = parser.parse_args()

	#Create a new ROOT file

	if args.test:
		
		output = ROOT.TFile('inputs/VBF_HToInv_2017_test.root', 'RECREATE')
	
	elif args.shortTest:

		output = ROOT.TFile('inputs/VBF_HToInv_2017_shortTest.root', 'RECREATE')

	else:
		
		#output = ROOT.TFile('inputs/VBF_HToInv_2017_first10Files_newTest.root', 'RECREATE')
	
		output = ROOT.TFile('inputs/VBF_HToInv_2017_new.root', 'RECREATE')

	#Create a new ROOT TTree
	eventTree = ROOT.TTree('eventTree', 'eventTree')

	#####################
	#eventTree.AutoSave()
	#output.SaveSelf()
	#####################
	
	#Initialize the variables and create branches	
	declare_branches(eventTree)
	
	t1 = time.time()

	f = file('inputs/MiniAOD_files2017.txt', 'r')

	for numFile, filename in enumerate(f.readlines()):
	
		t2 = time.time()

		if args.test or args.shortTest:

			if numFile == 1: break

		################Testing
		#print('Printing the content!')
		#output.cd()
		#output.ls()
		################

		print('Working on file {0:<5d} t = {1:.2f}'.format(numFile+1, t2-t1))
		
		writeTree(filename, eventTree, args)

		output.ls()

		if numFile%10 == 0:
	
			output.cd() #Go to the file directory
			
			#Save the output root file
			#eventTree.Write('eventTree')
			output.Write()

	output.Close()
	#inputFile = 'root://cmsxrootd.fnal.gov///store/mc/RunIISummer17MiniAOD/VBF_HToInvisible_M125_13TeV_powheg_pythia8/MINIAODSIM/NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v1/50000/CE13A08A-579E-E711-B9BB-001E67E5E8B6.root'	


if __name__ == '__main__':

	main()

	










