import ROOT

def declareHistos():

	print('Declaring histograms')

	histos = {}

	nJets_hist = ROOT.TH1D('nJets_hist', 'Number of Jets (RECO)', 15, 0, 15)
	nJets_hist.GetXaxis().SetTitle('Number of Jets')
	nJets_hist.GetYaxis().SetTitle('Number of Events')
	histos['nJets_hist'] = nJets_hist

	mjj_hist = ROOT.TH1F('mjj_hist', 'Invariant Mass of Two Leading Jets (RECO)', 50, 0, 500)
	mjj_hist.GetXaxis().SetTitle('Invariant Mass (GeV)')
	mjj_hist.GetYaxis().SetTitle('Number of Events')
	histos['mjj_hist'] = mjj_hist	
	
	print('Histograms declared')

	return histos





