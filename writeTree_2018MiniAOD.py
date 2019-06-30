import ROOT
import time
import argparse
from math import pi 

from lib.vbf_tree_2018 import * 

# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events	

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', help = 'Only go over the first file for testing', action = 'store_true')
args = parser.parse_args()

def minJetMETPhi(jets, mets):
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


def writeTree(inputFile):
	
	electrons, electronLabel = Handle('std::vector<pat::Electron>'), 'slimmedElectrons'
	muons, muonLabel = Handle('std::vector<pat::Muon>'), 'slimmedMuons'
	taus, tauLabel = Handle('std::vector<pat::Tau>'), 'slimmedTaus'
	photons, photonLabel = Handle('std::vector<pat::Photon>'), 'slimmedPhotons'
	jets, jetLabel = Handle('std::vector<pat::Jet>'), 'slimmedJets'
	mets, metLabel = Handle('std::vector<pat::MET>'), 'slimmedMETs'
	genParticles, genParticlesLabel = Handle('std::vector<reco::GenParticle>'), 'prunedGenParticles'

	triggerBits, triggerBitLabel = Handle("edm::TriggerResults"), ("TriggerResults","","HLT")
	triggerObjects, triggerObjectLabel  = Handle("std::vector<pat::TriggerObjectStandAlone>"), "slimmedPatTrigger"
	triggerPrescales, triggerPrescaleLabel  = Handle("pat::PackedTriggerPrescales"), "patTrigger"
	l1Jets, l1JetLabel  = Handle("BXVector<l1t::Jet>"), "caloStage2Digis:Jet"
	l1EtSums, l1EtSumLabel  = Handle("BXVector<l1t::EtSum>"), "caloStage2Digis:EtSum"

	events = Events(inputFile)

	print('Took the input file successfully')

	t1 = time.time()

	for i, event in enumerate(events):

		event.getByLabel(electronLabel, electrons)
		event.getByLabel(muonLabel, muons)
		event.getByLabel(tauLabel, taus)
		event.getByLabel(photonLabel, photons)
		event.getByLabel(jetLabel, jets)
		event.getByLabel(metLabel, mets)
		event.getByLabel(genParticlesLabel, genParticles)

		event.getByLabel(triggerBitLabel, triggerBits)
		event.getByLabel(triggerObjectLabel, triggerObjects)
		event.getByLabel(triggerPrescaleLabel, triggerPrescales)
		event.getByLabel(l1JetLabel, l1Jets)
		event.getByLabel(l1EtSumLabel, l1EtSums)

		t2 = time.time()

		if i % 100 == 0 and i != 0:		
			print('Analyzing event # %d , Time: %.2f' % (i , t2-t1))
	
		#Storing kinemaic values of interest	
		
		met[0] = mets.product()[0].pt()
		met_phi[0] = mets.product()[0].phi()
		met_eta[0] = mets.product()[0].eta()

		if met[0] < 50: continue

		jets_ = jets.product()

		nJet[0] = len(jets_)

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
			
			minPhi_jetMET[0] = minJetMETPhi(jets, mets) #Minimum delta_phi between jets and MET
	
		if jet_pt[0] < 50: continue
	
		electrons_ = electrons.product()

		nElectron[0] = len(electrons_)
	
		for i, el in enumerate(electrons_):
	
			electron_pt[i] = el.pt()
			electron_eta[i] = el.eta()
			electron_phi[i] = el.phi()
		
		muons_ = muons.product()

		nMuon[0] = len(muons_)

		for i, mu in enumerate(muons_):
	
			muon_pt[i] = mu.pt()
			muon_eta[i] = mu.eta()
			muon_phi[i] = mu.phi()

		taus_ = taus.product()

		nTau[0] = len(taus_)

		for i, tau in enumerate(taus_):
	
			tau_pt[i] = tau.pt()
			tau_eta[i] = tau.eta()
			tau_phi[i] = tau.phi()

		genParticles_ = genParticles.product()

		nParticles[0] = len(genParticles_)
	
		for i, prt in enumerate(genParticles_):

			pdgId[i] = prt.pdgId()
			#mothers[i] = prt.mother()
		
		triggerBits_ = triggerBits.product()

		names = event.object().triggerNames(triggerBits_)
	
		for i in range(triggerBits_.size()):

			if names.triggerNames()[i] == 'HLT_DiJet110_35_Mjj650_PFMET110_v9':
				if triggerBits_.accept(i):
					HLT_DiJet110_35_Mjj650_PFMET110_v9[0] = 1
				else:
					HLT_DiJet110_35_Mjj650_PFMET110_v9[0] = 0 
 
			elif names.triggerNames()[i] == 'HLT_DiJet110_35_Mjj650_PFMET120_v9':
				if triggerBits_.accept(i):
					HLT_DiJet110_35_Mjj650_PFMET120_v9[0] = 1
				else:
					HLT_DiJet110_35_Mjj650_PFMET120_v9[0] = 0 
			
			elif names.triggerNames()[i] == 'HLT_DiJet110_35_Mjj650_PFMET130_v9':
				if triggerBits_.accept(i):
					HLT_DiJet110_35_Mjj650_PFMET130_v9[0] = 1
				else:
					HLT_DiJet110_35_Mjj650_PFMET130_v9[0] = 0 
		
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
		
		eventTree.Fill()

if __name__ == '__main__':
	
	#Create a new ROOT file
	if args.test:

		output = ROOT.TFile('inputs/VBF_HToInv_2018_test.root', 'RECREATE')

	else:
	
		output = ROOT.TFile('inputs/VBF_HToInv_2018.root', 'RECREATE')

	#Create a new ROOT TTree
	eventTree = ROOT.TTree('eventTree', 'eventTree')
	
	#Initialize the variables and create branches	
	declare_branches(eventTree)

	t1 = time.time()

	f = file('inputs/MiniAOD_files2018.txt', 'r')

	for i, filename in enumerate(f.readlines()):
	
		t2 = time.time()

		if args.test:

			if i == 1: break

		print('Working on file {0:<5d} t = {1:.2f}'.format(i+1, t2-t1))
		
		writeTree(filename)
	
	#Save the output root file
	output.Write()

	#inputFile = 'root://cmsxrootd.fnal.gov///store/mc/RunIIAutumn18MiniAOD/VBF_HToInvisible_M125_TuneCP5_PSweights_13TeV_powheg_pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/80000/FDBE8CDB-175D-D942-8046-37E10DD9D6CE.root'


	










