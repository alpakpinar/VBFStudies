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
	
def writeTree(inputFile, tree, args, numEvents, numSavedEvents):

	'''
	Reads the inputFile and fills the tree.

	ARGUMENTS:
	---inputFile: MiniAOD ROOT file containing the events.
	---tree: The tree to be written. This is to be declared before calling this function.
	---args: Arguments parsed while calling this script.
			 If args contain the flag short, the event loop will be terminated at event 100.
			 If args contain the flag background, the event loop will be terminated if the total number of saved events reach 1M.
	---numEvents: Cumulative number of events looped over. This is to keep track of total number of events looped over. 
	---numSavedEvents: Cumulative number of events that are saved to the tree. This is to keep track of total number of events saved.
	'''
	
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

		numSavedEvents += 1

	print('Cumulative number of events looped over: {}'.format(numEvents))
	print('Cumulative number of events saved      : {}'.format(numSavedEvents))

	return numSavedEvents

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--test', help = 'Only go over the first two files for testing', action = 'store_true')
	parser.add_argument('-s', '--shortTest', help = 'Only go over the first 100 events in the first two files for testing', action = 'store_true')
	parser.add_argument('-l', '--local', help = 'Run over the local files', action = 'store_true')
	parser.add_argument('-b', '--background', help = 'Run over the background files', action = 'store_true')
	parser.add_argument('-c', '--counter', help = '''Determines which files on the input txt file to be run over. 
													 counter=0: File will run over files 1-5 in the given txt file
													 counter=1: File will run over files 6-10 in the given txt file
													 and so on.''', type = int)
	parser.add_argument('-f', '--fileIdx', help= '''Determines which txt file to be run over.
											     file=0: File will run over the first .txt file in the backgroundFiles dir
												 file=1: File will run over the second .txt file in the backgroundFiles dir
												 and so on.''', type = int)

	args = parser.parse_args()
	
	# Get the index for the first file 		
	counter = args.counter
	file_idx = 5*counter

	# Get which txt file in the background dir is to be considered
	txtFileIdx = args.fileIdx 
	
	#Create a new ROOT file

	if args.test:
		
		output = ROOT.TFile('inputs/VBF_HToInv_2017_test.root', 'RECREATE')
	
	elif args.shortTest and not args.background:
	
		output = ROOT.TFile('inputs/VBF_HToInv_2017_shortTest.root', 'RECREATE')

	elif args.shortTest and args.background:
		
		backgroundFilesDir = 'inputs/backgroundFiles'

		txtFileName_splitted = os.listdir(backgroundFilesDir)[1].split('_')[1:-1]
		ROOT_fileName = '_'.join(txtFileName_splitted) + '_shortTest' + '.root'
		ROOT_filePath = os.path.join('inputs', ROOT_fileName)
	
		output = ROOT.TFile(ROOT_filePath, 'RECREATE')

	elif args.background:
	
		backgroundFilesDir = 'inputs/backgroundFiles'

		txtFileName_splitted = os.listdir(backgroundFilesDir)[txtFileIdx].split('_')[2:-1]
		ROOT_fileName = '_'.join(txtFileName_splitted) + '_files{}-{}'.format(file_idx, file_idx+4)  + '.root'
		ROOT_filePath = os.path.join('inputs', ROOT_fileName)
	
		output = ROOT.TFile(ROOT_filePath, 'RECREATE')


	else:
	
		output = ROOT.TFile('inputs/VBF_HToInv_2017.root', 'RECREATE')

	#Create a new ROOT TTree
	eventTree = ROOT.TTree('eventTree', 'eventTree')
	
	#Initialize the variables and create branches	
	declare_branches(eventTree)
	
	t1 = time.time()

	# Track the total number of events looped over
	# and total saved number of events

	numEvents = 0
	numSavedEvents = 0

	if args.local:

		MCFilesDir = 'evaluateJetPairs/inputs/ROOT_MCFiles'

		for numFile, fileName in enumerate(os.listdir(MCFilesDir)):
			
			t2 = time.time()

			if args.test or args.shortTest:

				if numFile == 3: break

			file_path = os.path.join(MCFilesDir, fileName)

			print('Working on file {0:<5d} t = {1:.2f}'.format(numFile+1, t2-t1))
		
			print('Filename: {}'.format(file_path))
		
			writeTree(file_path, eventTree, args, numEvents, numSavedEvents)

			if numFile%10 == 0:
		
				output.cd() #Go to the file directory
				
				#Save the output root file
				output.Write()

	elif args.background:

		backgroundFilesDir = 'inputs/backgroundFiles'

		txtFile = os.listdir(backgroundFilesDir)[txtFileIdx]

		txtFile_path = os.path.join(backgroundFilesDir, txtFile)

		f = file(txtFile_path, 'r')

		print('*'*20)
		print('INFO: Will consider txt file {}'.format(txtFile))
		print('INFO: Will run over files with idx between {}-{}'.format(file_idx, file_idx+4))
		print('*'*20)

		for numFile, fileEntry in enumerate(f.readlines()[file_idx:file_idx+5]):

			t2 = time.time()

			splittedFileEntry = fileEntry.split('  ')

			fileName = 'root://cmsxrootd.fnal.gov//' + splittedFileEntry[0]

			numEvents += int(splittedFileEntry[1])
	
			if args.test or args.shortTest:

				if numFile == 2: break

			print('Working on file {0:<5d} t = {1:.2f}'.format(numFile+1, t2-t1))
		
			print('Filename: {}'.format(fileName))
		
			numSavedEvents = writeTree(fileName, eventTree, args, numEvents, numSavedEvents)

			print('Cumulative number of events looped over: {}'.format(numEvents))

		#	if numFile%10 == 0:
		#
		#		output.cd() #Go to the file directory
		#		
		#		#Save the output root file
		#		output.Write()

		output.Write()

	else:

		f = file('inputs/MiniAOD_files2017.txt', 'r')

		for numFile, filename in enumerate(f.readlines()):
		
			t2 = time.time()

			if args.test or args.shortTest:

				if numFile == 1: break

			print('Working on file {0:<5d} t = {1:.2f}'.format(numFile+1, t2-t1))
		
			print('Filename: {}'.format(filename))
		
			writeTree(filename, eventTree, args, numEvents, numSavedEvents)

			if numFile%10 == 0:
		
				output.cd() #Go to the file directory
				
				#Save the output root file
				output.Write()

	print('*'*20)
	print('RESULTS')
	print('Total number of events looped over: {}'.format(numEvents))
	print('Total number of events saved:       {}'.format(numSavedEvents))
	print('*'*20)

	output.Close()
	#inputFile = 'root://cmsxrootd.fnal.gov///store/mc/RunIISummer17MiniAOD/VBF_HToInvisible_M125_13TeV_powheg_pythia8/MINIAODSIM/NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v1/50000/CE13A08A-579E-E711-B9BB-001E67E5E8B6.root'	


if __name__ == '__main__':
	
	main()

	










