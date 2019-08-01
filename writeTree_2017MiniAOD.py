import ROOT
import time
import argparse
import os 

from lib.vbf_tree_2017 import * 
from lib.helperFunctions import invMassTwoJets, minJetMETPhi, isTightJet
from lib.veto import *

# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events	
	
def writeTree(inputFile, tree, args):
	
	electrons, electronLabel = Handle('std::vector<pat::Electron>'), 'slimmedElectrons'
	muons, muonLabel = Handle('std::vector<pat::Muon>'), 'slimmedMuons'
	taus, tauLabel = Handle('std::vector<pat::Tau>'), 'slimmedTaus'
	photons, photonLabel = Handle('std::vector<pat::Photon>'), 'slimmedPhotons'
	jets, jetLabel = Handle('std::vector<pat::Jet>'), 'slimmedJets'
	mets, metLabel = Handle('std::vector<pat::MET>'), 'slimmedMETs'
	genParticles, genParticlesLabel = Handle('std::vector<reco::GenParticle>'), 'prunedGenParticles'

	triggerBits, triggerBitLabel = Handle('edm::TriggerResults'), ('TriggerResults','','HLT')
	filterBits, filterLabel = Handle('edm::TriggerResults'), ('TriggerResults', '', 'PAT')

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
		event.getByLabel(filterLabel, filterBits)
		event.getByLabel(l1JetLabel, l1Jets)
		event.getByLabel(l1EtSumLabel, l1EtSums)

		t2 = time.time()

		if numEvent % 1000 == 0 and numEvent != 0:		
			print('Analyzing event # %d , Time: %.2f' % (numEvent , t2-t1))
	
		#Storing kinemaic values of interest	
		
		mets_ = mets.product()

		met[0] = mets_[0].pt()
		met_phi[0] = mets_[0].phi()
		met_eta[0] = mets_[0].eta()

		if met[0] < 50: continue

		######################
		#Implementing tight jet ID, 2017 recommendations
		######################

		jets_ = jets.product()

		nJet[0] = 0

		AK4_tightJets = []
		
		for i, jet in enumerate(jets_):

			if isTightJet(jet): 

				AK4_tightJets.append(jet)

		nJet[0] = len(AK4_tightJets)
		
		if nJet[0] < 2: continue #Discard the events with number of jets smaller than 2

		mjj[0] = invMassTwoJets(AK4_tightJets)

		for i, jet in enumerate(AK4_tightJets):

			jet_pt[i] = jet.pt()
			jet_energy[i] = jet.energy()
			jet_eta[i] = jet.eta()
			jet_phi[i] = jet.phi()
			
		absEtaDiff_leadingTwoJets[0] = abs(jet_eta[0] - jet_eta[1])

		minPhi_jetMET[0] = minJetMETPhi(jets_, mets_) #Minimum delta_phi between jets and MET
	
		if jet_pt[0] < 30: continue

		###################

		if containsLeptonOrPhoton(electrons, muons, taus, photons): continue #Lepton/photon veto

		if contains_bJet(AK4_tightJets): continue #b-jet veto

		genParticles_ = genParticles.product()

		nParticles[0] = len(genParticles_)
	
		for j, prt in enumerate(genParticles_):

			pdgId[j] = prt.pdgId()
		
		##########################
		
		triggerBits_ = triggerBits.product()

		names = event.object().triggerNames(triggerBits_)

		for k in range(triggerBits_.size()):

			#VBF DiJet triggers

			if names.triggerName(k) == 'HLT_DiJet110_35_Mjj650_PFMET110_v5':
	
				if triggerBits_.accept(k):
					HLT_DiJet110_35_Mjj650_PFMET110_v5[0] = 1

				else:
					HLT_DiJet110_35_Mjj650_PFMET110_v5[0] = 0 
 

			elif names.triggerNames()[k] == 'HLT_DiJet110_35_Mjj650_PFMET120_v5':
				if triggerBits_.accept(k):
					HLT_DiJet110_35_Mjj650_PFMET120_v5[0] = 1
				else:
					HLT_DiJet110_35_Mjj650_PFMET120_v5[0] = 0 
			
			elif names.triggerNames()[k] == 'HLT_DiJet110_35_Mjj650_PFMET130_v5':
				if triggerBits_.accept(k):
					HLT_DiJet110_35_Mjj650_PFMET130_v5[0] = 1
				else:
					HLT_DiJet110_35_Mjj650_PFMET130_v5[0] = 0 

			#MET triggers
			
			elif names.triggerNames()[k] == 'HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v16': 
				if triggerBits_.accept(k):
					HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v16[0] = 1
				else:
					HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v16[0] = 0 
		
			elif names.triggerNames()[k] == 'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v16': 
				if triggerBits_.accept(k):
					HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v16[0] = 1
				else:
					HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v16[0] = 0 

			elif names.triggerNames()[k] == 'HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v15': 
				if triggerBits_.accept(k):
					HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v15[0] = 1
				else:
					HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v15[0] = 0 
			
			elif names.triggerNames()[k] == 'HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v15': 
				if triggerBits_.accept(k):
					HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v15[0] = 1
				else:
					HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v15[0] = 0 

		#Filling L1 level information
		bxVector_jet = l1Jets.product()
		bxVector_met = l1EtSums.product()	
	
		bx=0 

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

		########################

		#Cleaning filters		

		filters_ = filterBits.product()

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
	parser.add_argument('-l', '--local', help = 'Run over the local files', action = 'store_true')
	args = parser.parse_args()
	
	#Create a new ROOT file

	if args.test:
		
		output = ROOT.TFile('inputs/VBF_HToInv_2017_test.root', 'RECREATE')
	
	elif args.shortTest:

		output = ROOT.TFile('inputs/VBF_HToInv_2017_shortTest.root', 'RECREATE')

	else:
	
		output = ROOT.TFile('inputs/VBF_HToInv_2017.root', 'RECREATE')

	#Create a new ROOT TTree
	eventTree = ROOT.TTree('eventTree', 'eventTree')
	
	#Initialize the variables and create branches	
	declare_branches(eventTree)
	
	t1 = time.time()

	if args.local:

		MCFilesDir = 'evaluateJetPairs/inputs/ROOT_MCFiles'

		for numFile, fileName in enumerate(os.listdir(MCFilesDir)):
			
			t2 = time.time()

			if args.test or args.shortTest:

				if numFile == 2: break

			file_path = os.path.join(MCFilesDir, fileName)

			print('Working on file {0:<5d} t = {1:.2f}'.format(numFile+1, t2-t1))
		
			print('Filename: {}'.format(file_path))
		
			writeTree(file_path, eventTree, args)

			if numFile%10 == 0:
		
				output.cd() #Go to the file directory
				
				#Save the output root file
				output.Write()

	else:

		f = file('inputs/MiniAOD_files2017.txt', 'r')

		for numFile, filename in enumerate(f.readlines()):
		
			t2 = time.time()

			if args.test or args.shortTest:

				if numFile == 1: break

			print('Working on file {0:<5d} t = {1:.2f}'.format(numFile+1, t2-t1))
		
			print('Filename: {}'.format(filename))
		
			writeTree(filename, eventTree, args)

			if numFile%10 == 0:
		
				output.cd() #Go to the file directory
				
				#Save the output root file
				output.Write()

	output.Close()
	#inputFile = 'root://cmsxrootd.fnal.gov///store/mc/RunIISummer17MiniAOD/VBF_HToInvisible_M125_13TeV_powheg_pythia8/MINIAODSIM/NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v1/50000/CE13A08A-579E-E711-B9BB-001E67E5E8B6.root'	


if __name__ == '__main__':
	
	main()

	










