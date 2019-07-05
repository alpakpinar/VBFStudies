import ROOT

def declareHistos():

	print('Declaring histograms')

	histos = {}

	nJets_hist = ROOT.TH1D('nJets_hist', 'Number of Jets (RECO)', 20, 0, 20)
	nJets_hist.GetXaxis().SetTitle('Number of Jets')
	nJets_hist.GetYaxis().SetTitle('Number of Events')
	histos['nJets_hist'] = nJets_hist

	leadingJetPt_hist = ROOT.TH1F('leadingJetPt_hist', 'Leading Jet p_{T} (RECO)', 50, 0, 500)
	leadingJetPt_hist.GetXaxis().SetTitle('p_{T} (GeV)')
	leadingJetPt_hist.GetYaxis().SetTitle('Number of Events')
	histos['leadingJetPt_hist'] = leadingJetPt_hist
	
	trailingJetPt_hist = ROOT.TH1F('trailingJetPt_hist', 'Trailing Jet p_{T} (RECO)', 50, 0, 500)
	trailingJetPt_hist.GetXaxis().SetTitle('p_{T} (GeV)')
	trailingJetPt_hist.GetYaxis().SetTitle('Number of Events')
	histos['trailingJetPt_hist'] = trailingJetPt_hist

	print('Histograms declared')

	return histos






