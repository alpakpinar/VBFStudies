import ROOT
import time
import argparse
from math import pi 

from vbf_tree import * 

# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events	

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', help = 'Only go over the first 100 events for testing', action = 'store_true')
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
	
	#Create a new ROOT file
	output = ROOT.TFile('VBF_HToInv.root', 'RECREATE')

	#Create a new ROOT TTree
	eventTree = ROOT.TTree('eventTree', 'eventTree')
	
	#Initialize the variables and create branches	
	declare_branches(eventTree)

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
	#l1Muons, l1MuonLabel  = Handle("BXVector"), "gmtStage2Digis:Muon"
	#l1EGammas, l1EGammaLabel  = Handle("BXVector"), "caloStage2Digis:EGamma"
	#l1Jets, l1JetLabel  = Handle("BXVector"), "caloStage2Digis:Jet"
	#l1EtSums, l1EtSumLabel  = Handle("BXVector"), "caloStage2Digis:EtSum"
	#l1Taus, l1TauLabel  = Handle("BXVector"), "caloStage2Digis:Tau"

	events = Events(inputFile)

	print('Took the input file successfully')

	t1 = time.time()

	for i, event in enumerate(events):

		if args.test:
			if i == 10: break

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
		#event.getByLabel(l1MuonLabel, l1Muons)
		#event.getByLabel(l1EGammaLabel, l1EGammas)
		#event.getByLabel(l1JetLabel, l1Jets)
		#event.getByLabel(l1EtSumLabel, l1EtSums)
		#event.getByLabel(l1TauLabel, l1Taus)

		t2 = time.time()

		if i % 100 == 0 and i != 0:		
			print('Analyzing event # %d , Time: %.2f' % (i , t2-t1))
	
		#Storing kinemaic values of interest	
		met[0] = mets.product()[0].pt()
		metPhi[0] = mets.product()[0].phi()
		#Add genMET!

		if met[0] < 50: continue

		jets_ = jets.product()

		nJet[0] = len(jets_)

		for i, jet in enumerate(jets_):

			jet_pt[i] = jet.pt()
			jet_energy[i] = jet.energy()
			jet_eta[i] = jet.eta()
			jet_phi[i] = jet.phi()

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
		
		print('Number of trigger paths: %d' % triggerBits.product().size())

		names = event.object().triggerNames(triggerBits.product())


		for i in range(triggerBits.product().size()):

			print('Trigger ', names.triggerNames()[i], ('PASS' if triggerBits.product().accept(i) else 'FAIL')) 

		eventTree.Fill()

	#Save the output root file
	output.Write()

if __name__ == '__main__':

	inputFile = 'root://cmsxrootd.fnal.gov///store/mc/RunIISummer17MiniAOD/VBF_HToInvisible_M125_13TeV_powheg_pythia8/MINIAODSIM/NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v1/50000/CE13A08A-579E-E711-B9BB-001E67E5E8B6.root'	
	
	writeTree(inputFile)

	









