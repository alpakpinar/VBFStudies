import ROOT

def readTree(inputFile):

	f = ROOT.TFile.Open(inputFile)

	event_count_before = 0
	event_count_after = 0

	for event in f.eventTree:
		
		event_count_before += 1
		
		# Reading the branches of eventTree		
		met = event.met
		metPhi = event.metPhi
		leadingJetPt = event.leadingJetPt
		trailingJetPt = event.trailingJetPt
		leadingJetEta = event.leadingJetEta
		trailingJetEta = event.trailingJetEta
		minPhi_jetMET = event.minPhi_jetMET
		etaProduct = event.etaProduct
		delta_jj = event.delta_jj	
		
		#VBF cuts
		if met < 200: continue

		if (leadingJetPt < 80 or trailingJetPt < 40): continue

		if minPhi_jetMET < 0.5: continue

		if etaProduct > 0: continue

		if delta_jj < 2.5: continue

		event_count_after += 1
				

if __name__ == '__main__':

	inputFile = 'VBF_HToInv.root'
	readTree(inputFile) 

 
