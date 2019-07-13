import ROOT
import os 
from array import array

def drawTriggerEff_MET(inputFile, trigger, args, mjjCut, leadingJetPtCut, trailingJetPtCut):

	'''
	Constructs the trigger efficiency graph for a given trigger, as a function of MET.
	Returns the MET histogram wih VBF cuts + trigger and efficiency plot.
	On top of default VBF cuts, applies the given mjj, leadingJetPt and trailingJetPt cuts.
	'''

	f = ROOT.TFile.Open(inputFile, 'UPDATE')

	met_array = array('f', [200., 220., 240., 270., 300., 340., 380., 420., 500.]) 

	outputDir = 'output/' + trigger

	if not os.path.isdir(outputDir):
	
		os.mkdir(outputDir)

	#Create the output ROOT file to save the histograms and efficiency graphs

	if args.test:

		fileName = trigger + '_mjj' + str(mjjCut) + '_leadingJetPt' + str(leadingJetPtCut) + '_trailingJetPt' + str(trailingJetPtCut) + '_test.root'
		filePath = os.path.join(outputDir, fileName)

		out = ROOT.TFile(filePath, 'RECREATE')

	else:

		fileName = trigger + '_mjj' + str(mjjCut) + '_leadingJetPt' + str(leadingJetPtCut) + '_trailingJetPt' + str(trailingJetPtCut) + '.root'
		filePath = os.path.join(outputDir, fileName)

		out = ROOT.TFile(filePath, 'RECREATE')

	#if count == 0: #First time calling the function

		#Clean the file (maybe to be implemented)

		#histNames = ['met_hist', 'met_hist_afterVBFCuts', 'met_hist_afterVBFCutsAndTrigger']

		#for i, hist in enumerate(histNames):

		#	if i < 2:

		#		deleteHistos(hist)

		#	else:

		#		for trig in triggers:
		#		
		#			histo = hist + '_' + trigger

		#			deleteHistos(histo)

	met_hist = ROOT.TH1F('met_hist', 'met_hist', len(met_array)-1, met_array)
	
	met_hist_afterVBFCuts = ROOT.TH1F('met_hist_afterVBFCuts', 'met_hist_afterVBFCuts', len(met_array)-1, met_array)	
	met_hist_afterVBFCuts.SetLineColor(ROOT.kRed)
	
	met_hist_afterVBFCutsAndTrigger = ROOT.TH1F('met_hist_afterVBFCutsAndTrigger', 'met_hist_afterVBFCutsAndTrigger', len(met_array)-1, met_array)	
	met_hist_afterVBFCutsAndTrigger.SetLineColor(ROOT.kBlack)

	vbfCuts = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && mjj > ' + str(mjjCut) + ' && jet_pt[0] > ' + str(leadingJetPtCut) + ' && jet_pt[1] > ' + str(trailingJetPtCut) 

	#vbfCuts = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && met > 200 && jet_pt[0] > 80 && jet_pt[1] > 40 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && mjj > 500 && absEtaDiff_leadingTwoJets > 2.5 && Flag_BadPFMuonFilter == 1 && Flag_goodVertices == 1 && Flag_globalSuperTightHalo2016Filter == 1 && Flag_HBHENoiseFilter == 1 && Flag_HBHENoiseIsoFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1'

	vbfAndTriggerCuts = vbfCuts + ' && ' + trigger + ' == 1'

	f.eventTree.Draw('met>>met_hist')
	f.eventTree.Draw('met>>met_hist_afterVBFCuts', vbfCuts, '')
	f.eventTree.Draw('met>>met_hist_afterVBFCutsAndTrigger', vbfAndTriggerCuts, '')
	
	print('Events passing VBF cuts: {}'.format(f.eventTree.GetEntries(vbfCuts)))
	print('Events passing VBF cuts + {}: {}\n'.format(trigger, f.eventTree.GetEntries(vbfAndTriggerCuts)))
	
	#Go to the directory for trigger efficiencies 
	
	try: out.GetKey('triggerEff_MET').IsFolder()

	except ReferenceError:

		out.mkdir('triggerEff_MET', 'triggerEff_MET') 

	out.cd('triggerEff_MET')
	
	#Check if the two histograms are consistent

	if ROOT.TEfficiency.CheckConsistency(met_hist_afterVBFCutsAndTrigger, met_hist_afterVBFCuts):

		eff_graph_MET = ROOT.TEfficiency(met_hist_afterVBFCutsAndTrigger, met_hist_afterVBFCuts)
		
		eff_graph_MET.SetTitle(trigger + ';MET (GeV);eff')

		if not args.noWrite:
		
			eff_graph_MET.Write('eff_graph_' + trigger + '_MET')
		
		eff_graph_mjj.Draw('AP')

		canv = ROOT.TCanvas('canv', 'canv')

		pngDir = 'pngImages/triggerEffPlots'
		file_name = trigger + '_MET.png'
		
		canv.Print(os.path.join(pngDir, file_name))

		print('Efficiency graph for ' + trigger + ' with respect to MET is constructed!\n')

	out.cd()
	
	try: out.GetKey('metHistos').IsFolder()

	except ReferenceError: 

		out.mkdir('metHistos', 'metHistos') 
	
	out.cd('metHistos')

	if not args.noWrite:

		met_hist.Write('met_hist')
		met_hist_afterVBFCuts.Write('met_hist_afterVBFCuts')
		met_hist_afterVBFCutsAndTrigger.Write('met_hist_afterVBFCutsAndTrigger_' + trigger)
	
	met_hist.SetDirectory(0)
	met_hist_afterVBFCuts.SetDirectory(0)
	met_hist_afterVBFCutsAndTrigger.SetDirectory(0)
	
	out.cd()

	out.Close()
	f.Close()

	return met_hist_afterVBFCutsAndTrigger, eff_graph_MET

def drawTriggerEff_trailingJetPt(inputFile, trigger, args, mjjCut, leadingJetPtCut):

	'''
    Constructs the trigger efficiency graph for a given trigger, as a function of trailing jet pt. 
    Returns the trailing jet pt histogram wih VBF cuts + trigger and efficiency plot.
	On top of default VBF cuts, applies the given mjj and leadingJetPt cuts.
    '''

	f = ROOT.TFile.Open(inputFile, 'UPDATE')

	trailingJetPt_array = array('f', [20., 25., 30., 35., 45., 55., 70., 80.])

	trailingJetPt_hist = ROOT.TH1F('trailingJetPt_hist', 'trailingJetPt_hist', len(trailingJetPt_array)-1, trailingJetPt_array)

	trailingJetPt_hist_afterVBFCuts = ROOT.TH1F('trailingJetPt_hist_afterVBFCuts', 'trailingJetPt_hist_afterVBFCuts', len(trailingJetPt_array)-1, trailingJetPt_array)	
	trailingJetPt_hist_afterVBFCuts.SetLineColor(ROOT.kRed)
	
	trailingJetPt_hist_afterVBFCutsAndTrigger = ROOT.TH1F('trailingJetPt_hist_afterVBFCutsAndTrigger', 'trailingJetPt_hist_afterVBFCutsAndTrigger', len(trailingJetPt_array)-1, trailingJetPt_array)
	trailingJetPt_hist_afterVBFCutsAndTrigger.SetLineColor(ROOT.kBlack)

	#Arrange the cuts

	vbfCuts = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && mjj > ' + str(mjjCut) + ' && jet_pt[0] > ' + str(leadingJetPtCut)

	vbfAndTriggerCuts = vbfCuts + ' && ' + trigger + ' == 1'

	f.eventTree.Draw('jet_pt[0]>>trailingJetPt_hist')
	f.eventTree.Draw('jet_pt[0]>>trailingJetPt_hist_afterVBFCuts', vbfCuts, '')
	f.eventTree.Draw('jet_pt[0]>>trailingJetPt_hist_afterVBFCutsAndTrigger', vbfAndTriggerCuts, '')
	
	####
	print('Events passing VBF cuts: {}'.format(f.eventTree.GetEntries(vbfCuts)))
	print('Events passing VBF cuts + {}: {}\n'.format(trigger, f.eventTree.GetEntries(vbfAndTriggerCuts)))
	####	
	
	#Go to the directory for trigger efficiencies 
	
	try: f.GetKey('triggerEff_trailingJetPt').IsFolder()

	except ReferenceError: 

		f.mkdir('triggerEff_trailingJetPt', 'triggerEff_trailingJetPt') 

	f.cd('triggerEff_trailingJetPt')
	
	if ROOT.TEfficiency.CheckConsistency(trailingJetPt_hist_afterVBFCutsAndTrigger, trailingJetPt_hist_afterVBFCuts):

		eff_graph_trailingJetPt = ROOT.TEfficiency(trailingJetPt_hist_afterVBFCutsAndTrigger, trailingJetPt_hist_afterVBFCuts)

		eff_graph_trailingJetPt.SetTitle(trigger + ';trailingJetPt (GeV);eff')

		if not args.noWrite:

			eff_graph_trailingJetPt.Write('eff_graph_' + trigger + '_trailingJetPt')

		canv = ROOT.TCanvas('canv', 'canv')
	
		eff_graph_mjj.Draw('AP')

		pngDir = 'pngImages/triggerEffPlots'
		fileName = trigger + '_trailingJetPt.png'
		
		canv.Print(os.path.join(pngDir, fileName))
	
		print('Efficiency graph for ' + trigger + ' with respect to trailing jet pt is constructed!\n')
	
	f.cd()
	
	try: f.GetKey('trailingJetPtHistos').IsFolder()

	except ReferenceError: 

		f.mkdir('trailingJetPtHistos', 'trailingJetPtHistos') 
	
	f.cd('trailingJetPtHistos')

	if not args.noWrite:
	
		trailingJetPt_hist.Write('trailingJetPt_hist')
		trailingJetPt_hist_afterVBFCuts.Write('trailingJetPt_hist_afterVBFCuts')
		trailingJetPt_hist_afterVBFCutsAndTrigger.Write('trailingJetPt_hist_afterVBFCutsAndTrigger_' + trigger)
	
	trailingJetPt_hist.SetDirectory(0)
	trailingJetPt_hist_afterVBFCuts.SetDirectory(0)
	trailingJetPt_hist_afterVBFCutsAndTrigger.SetDirectory(0)

	f.cd()
		
	f.Close()

	return trailingJetPt_hist_afterVBFCutsAndTrigger, eff_graph_trailingJetPt

def drawTriggerEff_leadingJetPt(inputFile, trigger, args, mjjCut):

	'''
    Constructs the trigger efficiency graph for a given trigger, as a function of leading jet pt. 
    Returns the leading jet pt histogram wih VBF cuts + trigger and efficiency plot.
	On top of default VBF cuts, applies the given mjj cut.
    '''

	f = ROOT.TFile.Open(inputFile, 'UPDATE')

	leadingJetPt_array = array('f', [80., 90., 100., 115., 130., 150., 180., 230.])

	leadingJetPt_hist = ROOT.TH1F('leadingJetPt_hist', 'leadingJetPt_hist', len(leadingJetPt_array)-1, leadingJetPt_array)

	leadingJetPt_hist_afterVBFCuts = ROOT.TH1F('leadingJetPt_hist_afterVBFCuts', 'leadingJetPt_hist_afterVBFCuts', len(leadingJetPt_array)-1, leadingJetPt_array)	
	leadingJetPt_hist_afterVBFCuts.SetLineColor(ROOT.kRed)
	
	leadingJetPt_hist_afterVBFCutsAndTrigger = ROOT.TH1F('leadingJetPt_hist_afterVBFCutsAndTrigger', 'leadingJetPt_hist_afterVBFCutsAndTrigger', len(leadingJetPt_array)-1, leadingJetPt_array)
	leadingJetPt_hist_afterVBFCutsAndTrigger.SetLineColor(ROOT.kBlack)

	#Cuts are default VBF cuts and mjj cut provided

	vbfCuts = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && mjj > ' + str(mjjCut)

	vbfAndTriggerCuts = vbfCuts + ' && ' + trigger + ' == 1'

	f.eventTree.Draw('jet_pt[0]>>leadingJetPt_hist')
	f.eventTree.Draw('jet_pt[0]>>leadingJetPt_hist_afterVBFCuts', vbfCuts, '')
	f.eventTree.Draw('jet_pt[0]>>leadingJetPt_hist_afterVBFCutsAndTrigger', vbfAndTriggerCuts, '')
	
	####
	print('Events passing VBF cuts: {}'.format(f.eventTree.GetEntries(vbfCuts)))
	print('Events passing VBF cuts + {}: {}\n'.format(trigger, f.eventTree.GetEntries(vbfAndTriggerCuts)))
	####	
	
	#Go to the directory for trigger efficiencies 
	
	try: f.GetKey('triggerEff_leadingJetPt').IsFolder()

	except ReferenceError: 

		f.mkdir('triggerEff_leadingJetPt', 'triggerEff_leadingJetPt') 

	f.cd('triggerEff_leadingJetPt')
	
	if ROOT.TEfficiency.CheckConsistency(leadingJetPt_hist_afterVBFCutsAndTrigger, leadingJetPt_hist_afterVBFCuts):

		eff_graph_leadingJetPt = ROOT.TEfficiency(leadingJetPt_hist_afterVBFCutsAndTrigger, leadingJetPt_hist_afterVBFCuts)

		eff_graph_leadingJetPt.SetTitle(trigger + ';leadingJetPt (GeV);eff')

		if not args.noWrite:

			eff_graph_leadingJetPt.Write('eff_graph_' + trigger + '_leadingJetPt')

		canv = ROOT.TCanvas('canv', 'canv')
	
		eff_graph_mjj.Draw('AP')
		
		pngDir = 'pngImages/triggerEffPlots'
		fileName = trigger + '_leadingJetPt.png'

		canv.Print(os.path.join(pngDir, fileName))
	
		print('Efficiency graph for ' + trigger + ' with respect to leading jet pt is constructed!\n')
	
	f.cd()
	
	try: f.GetKey('leadingJetPtHistos').IsFolder()

	except ReferenceError: 

		f.mkdir('leadingJetPtHistos', 'leadingJetPtHistos') 
	
	f.cd('leadingJetPtHistos')

	if not args.noWrite:
	
		leadingJetPt_hist.Write('leadingJetPt_hist')
		leadingJetPt_hist_afterVBFCuts.Write('leadingJetPt_hist_afterVBFCuts')
		leadingJetPt_hist_afterVBFCutsAndTrigger.Write('leadingJetPt_hist_afterVBFCutsAndTrigger_' + trigger)
	
	leadingJetPt_hist.SetDirectory(0)
	leadingJetPt_hist_afterVBFCuts.SetDirectory(0)
	leadingJetPt_hist_afterVBFCutsAndTrigger.SetDirectory(0)

	f.cd()
		
	f.Close()

	return leadingJetPt_hist_afterVBFCutsAndTrigger, eff_graph_leadingJetPt
	


def drawTriggerEff_mjj(inputFile, trigger, args):

	'''
	Constructs the trigger efficiency graph for a given trigger, as a function of invariant mass of two leading jets, mjj.
	Returns the mjj histogram wih VBF cuts + trigger and efficiency plot.
	'''

	f = ROOT.TFile.Open(inputFile, 'UPDATE')
	
	outputDir = 'output/' + trigger

	if not os.path.isdir(outputDir):
	
		os.makedirs(outputDir)

	#Create the output ROOT file to save the histograms and efficiency graphs

	if args.test:

		fileName = trigger + '_test.root'
		filePath = os.path.join(outputDir, fileName)

		out = ROOT.TFile(filePath, 'RECREATE')

	else:

		fileName = trigger + '.root'
		filePath = os.path.join(outputDir, fileName)

		out = ROOT.TFile(filePath, 'RECREATE')

	mjj_array = array('f', [500., 520., 540., 570., 600., 640., 680., 730., 790., 880., 1000.]) 

	mjj_hist = ROOT.TH1F('mjj_hist', 'mjj_hist', len(mjj_array)-1, mjj_array)

	mjj_hist_afterVBFCuts = ROOT.TH1F('mjj_hist_afterVBFCuts', 'mjj_hist_afterVBFCuts', len(mjj_array)-1, mjj_array)	
	mjj_hist_afterVBFCuts.SetLineColor(ROOT.kRed)
	
	mjj_hist_afterVBFCutsAndTrigger = ROOT.TH1F('mjj_hist_afterVBFCutsAndTrigger', 'mjj_hist_afterVBFCutsAndTrigger', len(mjj_array)-1, mjj_array)
	mjj_hist_afterVBFCutsAndTrigger.SetLineColor(ROOT.kBlack)

	vbfCuts = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5'

	#vbfCuts = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && met > 200 && jet_pt[0] > 80 && jet_pt[1] > 40 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && mjj > 500 && absEtaDiff_leadingTwoJets > 2.5 && Flag_BadPFMuonFilter == 1 && Flag_goodVertices == 1 && Flag_globalSuperTightHalo2016Filter == 1 && Flag_HBHENoiseFilter == 1 && Flag_HBHENoiseIsoFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1'

	vbfAndTriggerCuts = vbfCuts + ' && ' + trigger + ' == 1'

	f.eventTree.Draw('mjj>>mjj_hist')
	f.eventTree.Draw('mjj>>mjj_hist_afterVBFCuts', vbfCuts, '')
	f.eventTree.Draw('mjj>>mjj_hist_afterVBFCutsAndTrigger', vbfAndTriggerCuts, '')

	#Make the histograms bin-width divided

	#for nBin in range(1, mjj_hist.GetNbinsX()+1):

	#	mjj_orig = mjj_hist.GetBinContent(nBin)
	#	mjj_binWidth = mjj_hist.GetBinWidth(nBin)
	#	mjj_hist.SetBinContent(nBin, mjj_orig/mjj_binWidth)

	#	mjj_afterVBF_orig = mjj_hist_afterVBFCuts.GetBinContent(nBin)
	#	mjj_afterVBF_binWidth = mjj_hist_afterVBFCuts.GetBinWidth(nBin)
	#	mjj_hist_afterVBFCuts.SetBinContent(nBin, mjj_afterVBF_orig/mjj_afterVBF_binWidth) 
	#
	#	mjj_afterVBFTrig_orig = mjj_hist_afterVBFCutsAndTrigger.GetBinContent(nBin)
	#	mjj_afterVBFTrig_binWidth = mjj_hist_afterVBFCutsAndTrigger.GetBinWidth(nBin)
	#	mjj_hist_afterVBFCutsAndTrigger.SetBinContent(nBin, mjj_afterVBFTrig_orig/mjj_afterVBFTrig_binWidth)
		

	####
	print('Events passing VBF cuts: {}'.format(f.eventTree.GetEntries(vbfCuts)))
	print('Events passing VBF cuts + {}: {}\n'.format(trigger, f.eventTree.GetEntries(vbfAndTriggerCuts)))
	####	
	
	#Go to the directory for trigger efficiencies 
	
	try: out.GetKey('triggerEff_mjj').IsFolder()

	except ReferenceError: 

		out.mkdir('triggerEff_mjj', 'triggerEff_mjj') 

	out.cd('triggerEff_mjj')

	#Check if the two histograms are consistent

	if ROOT.TEfficiency.CheckConsistency(mjj_hist_afterVBFCutsAndTrigger, mjj_hist_afterVBFCuts):

		eff_graph_mjj = ROOT.TEfficiency(mjj_hist_afterVBFCutsAndTrigger, mjj_hist_afterVBFCuts)

		eff_graph_mjj.SetTitle(trigger + ';mjj (GeV);eff')

		if not args.noWrite:

			eff_graph_mjj.Write('eff_graph_' + trigger + '_mjj')

		canv = ROOT.TCanvas('canv', 'canv')
	
		eff_graph_mjj.Draw('AP')

		pngDir = 'pngImages/triggerEffPlots'
		fileName = trigger + '_mjj.png'

		canv.Print(os.path.join(pngDir, fileName))
	
		print('Efficiency graph for ' + trigger + ' with respect to mjj is constructed!\n')
	
	out.cd()
	
	try: out.GetKey('mjjHistos').IsFolder()

	except ReferenceError: 

		out.mkdir('mjjHistos', 'mjjHistos') 
	
	out.cd('mjjHistos')

	if not args.noWrite:
	
		mjj_hist.Write('mjj_hist')
		mjj_hist_afterVBFCuts.Write('mjj_hist_afterVBFCuts')
		mjj_hist_afterVBFCutsAndTrigger.Write('mjj_hist_afterVBFCutsAndTrigger_' + trigger)
	
	mjj_hist.SetDirectory(0)
	mjj_hist_afterVBFCuts.SetDirectory(0)
	mjj_hist_afterVBFCutsAndTrigger.SetDirectory(0)

	out.cd()
	
	out.Close()	
	f.Close()

	return mjj_hist_afterVBFCutsAndTrigger, eff_graph_mjj

