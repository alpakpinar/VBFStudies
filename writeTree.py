import ROOT
import time
import argparse
from math import pi
from array import array

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
	eventTree = ROOT.TTree('eventTree', 'List of different variables in events from VBF_HToInvisible dataset')

	#Initialize the variables and create branches

	met = array('f', [0.0])
	metPhi = array('f', [0.0])
	leadingJetPt = array('f', [0.0])
	trailingJetPt = array('f', [0.0])
	leadingJetEta = array('f', [0.0])
	trailingJetEta = array('f', [0.0])
	minPhi_jetMET = array('f', [0.0])
	etaProduct = array('f', [0.0])
	delta_jj = array('f', [0.0])
	
	eventTree.Branch('met', met, 'met/F')
	eventTree.Branch('metPhi', metPhi, 'metPhi/F')
	eventTree.Branch('leadingJetPt', leadingJetPt, 'leadingJetPt/F')
	eventTree.Branch('trailingJetPt', trailingJetPt, 'trailingJetPt/F')
	eventTree.Branch('leadingJetEta', leadingJetEta, 'leadingJetEta/F')
	eventTree.Branch('trailingJetEta', trailingJetEta, 'trailingJetEta/F')
	eventTree.Branch('minPhi_jetMET', minPhi_jetMET, 'minPhi_jetMET/F')
	eventTree.Branch('etaProduct', etaProduct, 'etaProduct/F')
	eventTree.Branch('delta_jj', delta_jj, 'delta_jj/F')

	electrons, electronLabel = Handle('std::vector<pat::Electron>'), 'slimmedElectrons'
	muons, muonLabel = Handle('std::vector<pat::Muon>'), 'slimmedMuons'
	taus, tauLabel = Handle('std::vector<pat::Tau>'), 'slimmedTaus'
	photons, photonLabel = Handle('std::vector<pat::Photon>'), 'slimmedPhotons'
	jets, jetLabel = Handle('std::vector<pat::Jet>'), 'slimmedJets'
	mets, metLabel = Handle('std::vector<pat::MET>'), 'slimmedMETs'

	events = Events(inputFile)

	print('Took the input file successfully')

	t1 = time.time()

	for i, event in enumerate(events):

		if args.test:
			if i == 100: break

		event.getByLabel(electronLabel, electrons)
		event.getByLabel(muonLabel, muons)
		event.getByLabel(tauLabel, taus)
		event.getByLabel(photonLabel, photons)
		event.getByLabel(jetLabel, jets)
		event.getByLabel(metLabel, mets)

		t2 = time.time()

		if i % 100 == 0 and i != 0:		
			print('Analyzing event # %d , Time: %.2f' % (i , t2-t1))
	
		#Storing kinemaic values of interest	
		met[0] = mets.product()[0].pt()
		metPhi[0] = mets.product()[0].phi()

		if met[0] < 50: continue

		jets_ = jets.product()

		if len(jets_) > 1:
		
			leadingJetPt[0] = jets_[0].pt()
			trailingJetPt[0] = jets_[1].pt()

			if leadingJetPt[0] < 40: continue

			leadingJetEta[0] = jets_[0].eta()
			trailingJetEta[0] = jets_[1].eta()
			
			minPhi_jetMET[0] = minJetMETPhi(jets, mets) #Minimum delta_phi between jets and MET
			
			etaProduct[0] = jets_[0].eta() * jets_[1].eta() #Eta_1 * Eta_2

			delta_jj[0] = abs(jets_[0].eta() - jets_[1].eta())

		eventTree.Fill()

	#Save the output root file
	output.Write()

if __name__ == '__main__':

	inputFile = 'root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv3/VBF_HToInvisible_M800_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v2/70000/D2978D87-B53A-E911-856C-0025905B856C.root'

	writeTree(inputFile)

	










