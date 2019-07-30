import ROOT
import numpy as np

def define2DHistos():

	'''
	Define necessary 2D histograms for further use and store it in a dict.
	'''

	histo_dict = {}

	#mjj_histo stores mjj values of the highest mjj pair and leading jet pt pair
	mjj_bins = np.arange(500., 2000., 50.)
	mjj_histo = ROOT.TH2F('mjj_histo', 'mjj_histo', len(mjj_bins)-1, mjj_bins, len(mjj_bins)-1, mjj_bins)
	mjj_histo.GetXaxis().SetTitle('mjj from the highest mjj pair(GeV)')
	mjj_histo.GetYaxis().SetTitle('mjj from the leading jet pair(GeV)')

	#leadJetPt_histo stores the larger jet pt from the pair with the highest mjj pair and leading pair
	leadJetPt_bins = np.arange(20., 300., 20.)
	leadJetPt_histo = ROOT.TH2F('leadJetPt_histo', 'leadJetPt_histo', len(leadJetPt_bins)-1, leadJetPt_bins, len(leadJetPt_bins)-1, leadJetPt_bins)
	leadJetPt_histo.GetXaxis().SetTitle('leading Jet Pt of the highest mjj pair (GeV)')
	leadJetPt_histo.GetYaxis().SetTitle('leading Jet Pt of the leading jet pair (GeV)')

	#trailJetPt_histo stores the smaller jet pt from the pair with the highest mjj pair and leading pair
	trailJetPt_bins = np.arange(20., 200., 20.)
	trailJetPt_histo = ROOT.TH2F('trailJetPt_histo', 'trailJetPt_histo', len(trailJetPt_bins)-1, trailJetPt_bins, len(trailJetPt_bins)-1, trailJetPt_bins)
	trailJetPt_histo.GetXaxis().SetTitle('trailing Jet Pt of the highest mjj pair (GeV)')
	trailJetPt_histo.GetYaxis().SetTitle('trailing Jet Pt of the leading jet pair (GeV)')
	
	#leadJetEta_histo stores the larger jet eta from the pair with the highest mjj pair and leading pair
	leadJetEta_bins = np.arange(-5., 5., 0.5)
	leadJetEta_histo = ROOT.TH2F('leadJetEta_histo', 'leadJetEta_histo', len(leadJetEta_bins)-1, leadJetEta_bins, len(leadJetEta_bins)-1, leadJetEta_bins)
	leadJetEta_histo.GetXaxis().SetTitle('leading Jet Eta of the highest mjj pair (GeV')
	leadJetEta_histo.GetYaxis().SetTitle('leading Jet Eta of the leading jet pair (GeV')
	
	#trailJetEta_histo stores the smaller jet eta from the pair with the highest mjj pair and leading pair
	trailJetEta_bins = np.arange(-5., 5., 0.5)
	trailJetEta_histo = ROOT.TH2F('trailJetEta_histo', 'trailJetEta_histo', len(trailJetEta_bins)-1, trailJetEta_bins, len(trailJetEta_bins)-1, trailJetEta_bins)
	trailJetEta_histo.GetXaxis().SetTitle('trailing Jet Eta of the highest mjj pair (GeV')
	trailJetEta_histo.GetYaxis().SetTitle('trailing Jet Eta of the leading jet pair (GeV')

	histo_dict['mjj_histo'] = mjj_histo
	histo_dict['leadJetPt_histo'] = leadJetPt_histo
	histo_dict['trailJetPt_histo'] = trailJetPt_histo 
	histo_dict['leadJetEta_histo'] = leadJetEta_histo
	histo_dict['trailJetEta_histo'] = trailJetEta_histo 

	return histo_dict

