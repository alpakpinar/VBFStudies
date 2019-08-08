import ROOT
import os
import numpy as np 
from array import array

def constructTriggerEff(histo_cut, histo_all, trigger, args, pngDir, fileName):

	'''
	Draws and saves the efficiency graph for a given trigger, given two historgrams.
	Saves the graph both as a graph in the relevant ROOT file and a png file in the relevant directory (if noWrite option is NOT specified while running the main script).
	Saves the png file in the given directory pngDir, and filename will be fileName. Creates the pngDir if not already created.
	Called in other drawTriggerEff functions.
	
	ARGUMENTS:
	---histo_cut: The histogram with VBF cuts + trigger cut applied
	---histo_all: The histogram with only VBF cuts applied
	---trigger: The trigger in consideration
	---args: This is the arguments parsed in while calling ../readTree.py.
	---pngDir: The name of the directory to save the histogram as a .png file.
	---fileName: The name of the .png file to be saved.
	'''

	#Obtain the variable to be plotted and the case (two jets forward, central etc...)

	histoName_splitted = histo_cut.GetName().split('_')

	variable = histoName_splitted[0]
	case = histoName_splitted[-1]

	pngDir += '_' + case #Add the case information in the dir name

	#Text box containing the case for jet eta

	#text = ROOT.TPaveText(0.6, 0.6, 0.8, 0.8)
	#text.AddText(case)
	
	#Construct the efficiency graph and save it

	if ROOT.TEfficiency.CheckConsistency(histo_cut, histo_all):

		eff_graph = ROOT.TEfficiency(histo_cut, histo_all)

		eff_graph.SetTitle(trigger + ';' + variable + ' (GeV);eff')
	
		if not args.noWrite:

			eff_graph.Write('eff_graph_' + trigger + '_' + variable + '_' + case)

		canv = ROOT.TCanvas('canv', 'canv')
	
		eff_graph.Draw('AP')
		
		ROOT.gPad.Update()
		graph = eff_graph.GetPaintedGraph()
		graph.SetMinimum(0)
		graph.SetMaximum(1)

		#text.Draw('same')
		
		if not args.noWrite:

			eff_graph.Write('eff_graph_' + trigger + '_' + variable + '_' + case)

		#Create the relevant dir if not already present

		if not os.path.isdir(pngDir):

			os.makedirs(pngDir)

		canv.Print(os.path.join(pngDir, fileName))
	
		print('Efficiency graph for ' + trigger + ' with respect to mjj is constructed!')
		print('CASE: {}\n'.format(case))


def drawTriggerEff_MET(inputFile, trigger, args, mjjCut, leadingJetPtCut, trailingJetPtCut):

	'''
	Constructs the trigger efficiency graph for a given trigger, as a function of invariant mass of two leading jets, mjj.
	Applies the default VBF cuts and given leadingJetPt and trailingJetPt cuts.

	ARGUMENTS:	
	--- inputFile: The ROOT file containing eventTree.
	--- trigger: The trigger name for which the efficiency curve will be drawn.
	--- args: This is the arguments parsed in while calling ../readTree.py.
	--- leadingJetPtCut: The leading jet pt cut to be applied.
	--- trailingJetPtCut: The trailing jet pt cut to be applied.
	'''

	f = ROOT.TFile.Open(inputFile, 'UPDATE')

	#met_array = array('f', [80., 90., 100., 110., 117., 124., 131., 138., 145., 152., 159., 166., 173., 180., 187., 194., 201., 210., 220.]) 
	met_array = np.arange(80., 230., 15.) 

	outputDir = 'output/' + trigger

	if not os.path.isdir(outputDir):
	
		os.mkdir(outputDir)

	#Create the output ROOT file to save the histograms and efficiency graphs
	
	if args.test:

		fileName = trigger + '_test.root'
		filePath = os.path.join(outputDir, fileName)

		out = ROOT.TFile.Open(filePath, 'UPDATE')

	else:

		fileName = trigger + '.root'
		filePath = os.path.join(outputDir, fileName)

		out = ROOT.TFile.Open(filePath, 'UPDATE')

	met_hist_twoCentralJets = ROOT.TH1F('met_hist_twoCentralJets', 'met_hist_twoCentralJets', len(met_array)-1, met_array)
	met_hist_twoForwardJets = ROOT.TH1F('met_hist_twoForwardJets', 'met_hist_twoForwardJets', len(met_array)-1, met_array)
	met_hist_oneCentralJetOneForwardJet = ROOT.TH1F('met_hist_oneCentralJetOneForwardJet', 'met_hist_oneCentralJetOneForwardJet', len(met_array)-1, met_array)
	
	met_hist_afterVBFCuts_twoCentralJets = ROOT.TH1F('met_hist_afterVBFCuts_twoCentralJets', 'met_hist_afterVBFCuts_twoCentralJets', len(met_array)-1, met_array)	
	met_hist_afterVBFCuts_twoCentralJets.SetLineColor(ROOT.kRed)
	met_hist_afterVBFCuts_twoForwardJets = ROOT.TH1F('met_hist_afterVBFCuts_twoForwardJets', 'met_hist_afterVBFCuts_twoForwardJets', len(met_array)-1, met_array)	
	met_hist_afterVBFCuts_twoForwardJets.SetLineColor(ROOT.kRed)
	met_hist_afterVBFCuts_oneCentralJetOneForwardJet = ROOT.TH1F('met_hist_afterVBFCuts_oneCentralJetOneForwardJet', 'met_hist_afterVBFCuts_oneCentralJetOneForwardJet', len(met_array)-1, met_array)	
	met_hist_afterVBFCuts_oneCentralJetOneForwardJet.SetLineColor(ROOT.kRed)
	
	met_hist_afterVBFCutsAndTrigger_twoCentralJets = ROOT.TH1F('met_hist_afterVBFCutsAndTrigger_twoCentralJets', 'met_hist_afterVBFCutsAndTrigger_twoCentralJets', len(met_array)-1, met_array)	
	met_hist_afterVBFCutsAndTrigger_twoCentralJets.SetLineColor(ROOT.kBlack)
	met_hist_afterVBFCutsAndTrigger_twoForwardJets = ROOT.TH1F('met_hist_afterVBFCutsAndTrigger_twoForwardJets', 'met_hist_afterVBFCutsAndTrigger_twoForwardJets', len(met_array)-1, met_array)	
	met_hist_afterVBFCutsAndTrigger_twoForwardJets.SetLineColor(ROOT.kBlack)
	met_hist_afterVBFCutsAndTrigger_oneCentralJetOneForwardJet = ROOT.TH1F('met_hist_afterVBFCutsAndTrigger_oneCentralJetOneForwardJet', 'met_hist_afterVBFCutsAndTrigger_oneCentralJetOneForwardJet', len(met_array)-1, met_array)	
	met_hist_afterVBFCutsAndTrigger_oneCentralJetOneForwardJet.SetLineColor(ROOT.kBlack)

	vbfCuts = 'minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && Flag_BadPFMuonFilter == 1 && Flag_goodVertices == 1 && Flag_globalSuperTightHalo2016Filter == 1 && Flag_HBHENoiseFilter == 1 && Flag_HBHENoiseIsoFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && mjj > ' + str(mjjCut) + ' && jet_pt[0] > ' + str(leadingJetPtCut) + ' && jet_pt[1] > ' + str(trailingJetPtCut) 

	vbfAndTriggerCuts = vbfCuts + ' && ' + trigger + ' == 1'
	
	twoCentralJets_cut = '(abs(jet_eta[0]) <= 2.5 && abs(jet_eta[1]) <= 2.5)'
	twoForwardJets_cut = '(abs(jet_eta[0]) > 2.5 && abs(jet_eta[1]) > 2.5)'
	oneCentralJetOneForwardJet_cut = '((abs(jet_eta[0]) <= 2.5 && abs(jet_eta[1]) > 2.5) || (abs(jet_eta[0]) > 2.5 && abs(jet_eta[1]) <= 2.5))'

	f.eventTree.Draw('met>>met_hist_twoCentralJets', twoCentralJets_cut, '')
	f.eventTree.Draw('met>>met_hist_twoForwardJets', twoForwardJets_cut, '')
	f.eventTree.Draw('met>>met_hist_oneCentralJetOneForwardJet', oneCentralJetOneForwardJet_cut, '')

	f.eventTree.Draw('met>>met_hist_afterVBFCuts_twoCentralJets', vbfCuts + ' && ' + twoCentralJets_cut, '')
	f.eventTree.Draw('met>>met_hist_afterVBFCuts_twoForwardJets', vbfCuts + ' && ' + twoForwardJets_cut, '')
	f.eventTree.Draw('met>>met_hist_afterVBFCuts_oneCentralJetOneForwardJet', vbfCuts + ' && ' + oneCentralJetOneForwardJet_cut, '')

	f.eventTree.Draw('met>>met_hist_afterVBFCutsAndTrigger_twoCentralJets', vbfAndTriggerCuts + ' && ' + twoCentralJets_cut, '')
	f.eventTree.Draw('met>>met_hist_afterVBFCutsAndTrigger_twoForwardJets', vbfAndTriggerCuts + ' && ' + twoForwardJets_cut, '')
	f.eventTree.Draw('met>>met_hist_afterVBFCutsAndTrigger_oneCentralJetOneForwardJet', vbfAndTriggerCuts + ' && ' + oneCentralJetOneForwardJet_cut, '')
	
	print('Events passing VBF cuts: {}'.format(f.eventTree.GetEntries(vbfCuts)))
	print('Events passing VBF cuts + {}: {}\n'.format(trigger, f.eventTree.GetEntries(vbfAndTriggerCuts)))
	
	#Go to the directory (in the ROOT file) for trigger efficiencies 
	
	folderName = 'triggerEff_MET_mjjCut' + str(mjjCut) + 'leadingJetPtCut' + str(leadingJetPtCut) + '_trailingJetPtCut' + str(trailingJetPtCut)
	
	try: out.GetKey(folderName).IsFolder()

	except ReferenceError:

		out.mkdir(folderName, folderName) 

	out.cd(folderName)
	
	#Name of the directory to save the png files, and the name of the png file

	pngDir = 'pngImages/triggerEffPlots/METPlots/mjjCut' + str(mjjCut) + '_leadingJetPtCut' + str(leadingJetPtCut) + '_trailingJetPtCut' + str(trailingJetPtCut)
	file_name = trigger + '_MET_mjjCut' + str(mjjCut) + '_leadingJetPtCut' + str(leadingJetPtCut) + '_trailingJetPtCut' + str(trailingJetPtCut) + '.png'
	
	constructTriggerEff(met_hist_afterVBFCutsAndTrigger_twoCentralJets, met_hist_afterVBFCuts_twoCentralJets, trigger, args, pngDir, file_name)
	constructTriggerEff(met_hist_afterVBFCutsAndTrigger_twoForwardJets, met_hist_afterVBFCuts_twoForwardJets, trigger, args, pngDir, file_name)
	constructTriggerEff(met_hist_afterVBFCutsAndTrigger_oneCentralJetOneForwardJet, met_hist_afterVBFCuts_oneCentralJetOneForwardJet, trigger, args, pngDir, file_name)

	out.cd()
	
	#Browse (create if necessary) the folder for individual histograms

	histoDirName = 'METHistos_mjjCut' + str(mjjCut) + '_leadingJetPtCut' + str(leadingJetPtCut) + '_trailingJetPtCut' + str(trailingJetPtCut)
	
	try: out.GetKey(histoDirName).IsFolder()

	except ReferenceError: 

		out.mkdir(histoDirName, histoDirName) 
	
	out.cd(histoDirName)

	if not args.noWrite:

		met_hist_twoCentralJets.Write('met_hist_twoCentralJets')
		met_hist_twoForwardJets.Write('met_hist_twoForwardJets')
		met_hist_oneCentralJetOneForwardJet.Write('met_hist_oneCentralJetOneForwardJet')
		
		met_hist_afterVBFCuts_twoCentralJets.Write('met_hist_afterVBFCuts_twoCentralJets')
		met_hist_afterVBFCuts_twoForwardJets.Write('met_hist_afterVBFCuts_twoForwardJets')
		met_hist_afterVBFCuts_oneCentralJetOneForwardJet.Write('met_hist_afterVBFCuts_oneCentralJetOneForwardJet')
		
		met_hist_afterVBFCutsAndTrigger_twoCentralJets.Write('met_hist_afterVBFCutsAndTrigger_twoCentralJets')
		met_hist_afterVBFCutsAndTrigger_twoForwardJets.Write('met_hist_afterVBFCutsAndTrigger_twoForwardJets')
		met_hist_afterVBFCutsAndTrigger_oneCentralJetOneForwardJet.Write('met_hist_afterVBFCutsAndTrigger_oneCentralJetOneForwardJet')
	
	met_hist_twoCentralJets.SetDirectory(0)
	met_hist_twoForwardJets.SetDirectory(0)
	met_hist_oneCentralJetOneForwardJet.SetDirectory(0)

	met_hist_afterVBFCuts_twoCentralJets.SetDirectory(0)
	met_hist_afterVBFCuts_twoForwardJets.SetDirectory(0)
	met_hist_afterVBFCuts_oneCentralJetOneForwardJet.SetDirectory(0)

	met_hist_afterVBFCutsAndTrigger_twoCentralJets.SetDirectory(0)
	met_hist_afterVBFCutsAndTrigger_twoForwardJets.SetDirectory(0)
	met_hist_afterVBFCutsAndTrigger_oneCentralJetOneForwardJet.SetDirectory(0)
	
	out.cd()

	out.Close()
	f.Close()

def drawTriggerEff_trailingJetPt(inputFile, trigger, args, mjjCut, leadingJetPtCut):

	'''
    Constructs the trigger efficiency graph for a given trigger, as a function of trailing jet pt. 
    Returns the trailing jet pt histogram wih VBF cuts + trigger and efficiency plot.
	On top of default VBF cuts, applies the given mjj and leadingJetPt cuts.
    '''

	f = ROOT.TFile.Open(inputFile, 'UPDATE')
	
	outputDir = 'output/' + trigger

	if not os.path.isdir(outputDir):
	
		os.makedirs(outputDir)

	#Create the output ROOT file to save the histograms and efficiency graphs

	if args.test:

		fileName = trigger + '_test.root'
		filePath = os.path.join(outputDir, fileName)

		out = ROOT.TFile.Open(filePath, 'UPDATE')

	else:

		fileName = trigger + '.root'
		filePath = os.path.join(outputDir, fileName)

		out = ROOT.TFile.Open(filePath, 'UPDATE')

	trailingJetPt_array = array('f', [20., 23., 26., 29., 32., 35., 39., 43., 47., 52., 56., 60., 65., 70., 75., 80.])

	trailingJetPt_hist = ROOT.TH1F('trailingJetPt_hist', 'trailingJetPt_hist', len(trailingJetPt_array)-1, trailingJetPt_array)

	trailingJetPt_hist_afterVBFCuts = ROOT.TH1F('trailingJetPt_hist_afterVBFCuts', 'trailingJetPt_hist_afterVBFCuts', len(trailingJetPt_array)-1, trailingJetPt_array)	
	trailingJetPt_hist_afterVBFCuts.SetLineColor(ROOT.kRed)
	
	trailingJetPt_hist_afterVBFCutsAndTrigger = ROOT.TH1F('trailingJetPt_hist_afterVBFCutsAndTrigger', 'trailingJetPt_hist_afterVBFCutsAndTrigger', len(trailingJetPt_array)-1, trailingJetPt_array)
	trailingJetPt_hist_afterVBFCutsAndTrigger.SetLineColor(ROOT.kBlack)

	#Arrange the cuts

	vbfCuts = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && mjj > ' + str(mjjCut) + ' && jet_pt[0] > ' + str(leadingJetPtCut)

	vbfAndTriggerCuts = vbfCuts + ' && ' + trigger + ' == 1'

	f.eventTree.Draw('jet_pt[1]>>trailingJetPt_hist')
	f.eventTree.Draw('jet_pt[1]>>trailingJetPt_hist_afterVBFCuts', vbfCuts, '')
	f.eventTree.Draw('jet_pt[1]>>trailingJetPt_hist_afterVBFCutsAndTrigger', vbfAndTriggerCuts, '')
	
	####
	print('Events passing VBF cuts: {}'.format(f.eventTree.GetEntries(vbfCuts)))
	print('Events passing VBF cuts + {}: {}\n'.format(trigger, f.eventTree.GetEntries(vbfAndTriggerCuts)))
	####	
	
	#Go to the directory for trigger efficiencies 
	
	try: out.GetKey('triggerEff_trailingJetPt').IsFolder()

	except ReferenceError: 

		out.mkdir('triggerEff_trailingJetPt', 'triggerEff_trailingJetPt') 

	out.cd('triggerEff_trailingJetPt')
	
	if ROOT.TEfficiency.CheckConsistency(trailingJetPt_hist_afterVBFCutsAndTrigger, trailingJetPt_hist_afterVBFCuts):

		eff_graph_trailingJetPt = ROOT.TEfficiency(trailingJetPt_hist_afterVBFCutsAndTrigger, trailingJetPt_hist_afterVBFCuts)

		eff_graph_trailingJetPt.SetTitle(trigger + ';trailingJetPt (GeV);eff')

		if not args.noWrite:

			eff_graph_trailingJetPt.Write('eff_graph_' + trigger + '_trailingJetPt')

		canv = ROOT.TCanvas('canv', 'canv')
	
		eff_graph_trailingJetPt.Draw('AP')

		pngDir = 'pngImages/triggerEffPlots/trailingJetPtPlots/mjjCut' + str(mjjCut) + '_leadingJetPtCut' + str(leadingJetPtCut)
		fileName = trigger + '_trailingJetPt_mjjCut' + str(mjjCut) + '_leadingJetPtCut' + str(leadingJetPtCut) + '.png'
		
		if not os.path.isdir(pngDir):

			os.makedirs(pngDir)

		canv.Print(os.path.join(pngDir, fileName))
	
		print('Efficiency graph for ' + trigger + ' with respect to trailing jet pt is constructed!\n')
	
	out.cd()
	
	try: out.GetKey('trailingJetPtHistos').IsFolder()

	except ReferenceError: 

		out.mkdir('trailingJetPtHistos', 'trailingJetPtHistos') 
	
	out.cd('trailingJetPtHistos')

	if not args.noWrite:
	
		trailingJetPt_hist.Write('trailingJetPt_hist')
		trailingJetPt_hist_afterVBFCuts.Write('trailingJetPt_hist_afterVBFCuts')
		trailingJetPt_hist_afterVBFCutsAndTrigger.Write('trailingJetPt_hist_afterVBFCutsAndTrigger_' + trigger)
	
	trailingJetPt_hist.SetDirectory(0)
	trailingJetPt_hist_afterVBFCuts.SetDirectory(0)
	trailingJetPt_hist_afterVBFCutsAndTrigger.SetDirectory(0)

	out.cd()
	
	out.Close()	
	f.Close()

	return trailingJetPt_hist_afterVBFCutsAndTrigger, eff_graph_trailingJetPt


def drawTriggerEff_leadingJetPt(inputFile, trigger, args, mjjCut):

	'''
    Constructs the trigger efficiency graph for a given trigger, as a function of leading jet pt. 
    Returns the leading jet pt histogram wih VBF cuts + trigger and efficiency plot.
    Applies given mjjCut on top of default VBF selections.
	'''

	f = ROOT.TFile.Open(inputFile, 'UPDATE')
	
	outputDir = 'output/' + trigger

	if not os.path.isdir(outputDir):
	
		os.makedirs(outputDir)

	#Create the output ROOT file to save the histograms and efficiency graphs

	if args.test:

		fileName = trigger + '_test.root'
		filePath = os.path.join(outputDir, fileName)

		out = ROOT.TFile.Open(filePath, 'UPDATE')

	else:

		fileName = trigger + '.root'
		filePath = os.path.join(outputDir, fileName)

		out = ROOT.TFile.Open(filePath, 'UPDATE')

	leadingJetPt_array = array('f', [80., 85., 90., 95.,  100., 105.,  110., 115., 120., 130., 140., 150., 160., 175., 190., 210., 230., 250., 280., 310., 350.]) 

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

	#Including overflow bin for each histogram

	#leadingJetPt_hist.GetXaxis().SetRange(1, leadingJetPt_hist.GetNbinsX()+1)
	#leadingJetPt_hist_afterVBFCuts.GetXaxis().SetRange(1, leadingJetPt_hist.GetNbinsX()+1)
	#leadingJetPt_hist_afterVBFCutsAndTrigger.GetXaxis().SetRange(1, leadingJetPt_hist.GetNbinsX()+1)
	
	####
	print('Events passing VBF cuts: {}'.format(f.eventTree.GetEntries(vbfCuts)))
	print('Events passing VBF cuts + {}: {}\n'.format(trigger, f.eventTree.GetEntries(vbfAndTriggerCuts)))
	####	

	#Go to the directory for trigger efficiencies 
	
	try: out.GetKey('triggerEff_leadingJetPt').IsFolder()

	except ReferenceError: 

		out.mkdir('triggerEff_leadingJetPt', 'triggerEff_leadingJetPt') 

	out.cd('triggerEff_leadingJetPt')
	
	if ROOT.TEfficiency.CheckConsistency(leadingJetPt_hist_afterVBFCutsAndTrigger, leadingJetPt_hist_afterVBFCuts):

		eff_graph_leadingJetPt = ROOT.TEfficiency(leadingJetPt_hist_afterVBFCutsAndTrigger, leadingJetPt_hist_afterVBFCuts)

		eff_graph_leadingJetPt.SetTitle(trigger + ';leadingJetPt (GeV);eff')

		if not args.noWrite:

			eff_graph_leadingJetPt.Write('eff_graph_' + trigger + '_leadingJetPt')

		canv = ROOT.TCanvas('canv', 'canv')
	
		eff_graph_leadingJetPt.Draw('AP')
		
		pngDir = 'pngImages/triggerEffPlots/leadingJetPtPlots/mjjCut' + str(mjjCut)
		fileName = trigger + '_leadingJetPt_mjjCut' + str(mjjCut)  + '.png'

		if not os.path.isdir(pngDir):

			os.makedirs(pngDir)

		canv.Print(os.path.join(pngDir, fileName))
	
		print('Efficiency graph for ' + trigger + ' with respect to leading jet pt is constructed!\n')
	
	out.cd()
	
	try: out.GetKey('leadingJetPtHistos').IsFolder()

	except ReferenceError: 

		out.mkdir('leadingJetPtHistos', 'leadingJetPtHistos') 
	
	out.cd('leadingJetPtHistos')

	if not args.noWrite:
	
		leadingJetPt_hist.Write('leadingJetPt_hist')
		leadingJetPt_hist_afterVBFCuts.Write('leadingJetPt_hist_afterVBFCuts')
		leadingJetPt_hist_afterVBFCutsAndTrigger.Write('leadingJetPt_hist_afterVBFCutsAndTrigger_' + trigger)
	
	leadingJetPt_hist.SetDirectory(0)
	leadingJetPt_hist_afterVBFCuts.SetDirectory(0)
	leadingJetPt_hist_afterVBFCutsAndTrigger.SetDirectory(0)

	out.cd()
	
	out.Close()	
	f.Close()

	return leadingJetPt_hist_afterVBFCutsAndTrigger, eff_graph_leadingJetPt

def drawTriggerEff_mjj(inputFile, trigger, args, leadingJetPtCut, trailingJetPtCut):

	'''
	Constructs the trigger efficiency graph for a given trigger, as a function of invariant mass of two leading jets, mjj.
	Applies the default VBF cuts and given leadingJetPt and trailingJetPt cuts.

	ARGUMENTS:	
	--- inputFile: The ROOT file containing eventTree.
	--- trigger: The trigger name for which the efficiency curve will be drawn.
	--- args: This is the arguments parsed in while calling ../readTree.py.
	--- leadingJetPtCut: The leading jet pt cut to be applied.
	--- trailingJetPtCut: The trailing jet pt cut to be applied.
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

	mjj_array = np.arange(300., 3000., 300.)
	#mjj_array = array('f', [500., 520., 540., 570., 600., 640., 680., 730., 790., 880., 1000.]) 

	mjj_hist_twoCentralJets = ROOT.TH1F('mjj_hist_twoCentralJets', 'mjj_hist_twoCentralJets', len(mjj_array)-1, mjj_array)
	mjj_hist_twoForwardJets = ROOT.TH1F('mjj_hist_twoForwardJets', 'mjj_hist_twoForwardJets', len(mjj_array)-1, mjj_array)
	mjj_hist_oneCentralJetOneForwardJet = ROOT.TH1F('mjj_hist_oneCentralJetOneForwardJet', 'mjj_hist_oneCentralJetOneForwardJet', len(mjj_array)-1, mjj_array)

	mjj_hist_afterVBFCuts_twoCentralJets = ROOT.TH1F('mjj_hist_afterVBFCuts_twoCentralJets', 'mjj_hist_afterVBFCuts_twoCentralJets', len(mjj_array)-1, mjj_array)	
	mjj_hist_afterVBFCuts_twoCentralJets.SetLineColor(ROOT.kRed)
	mjj_hist_afterVBFCuts_twoForwardJets = ROOT.TH1F('mjj_hist_afterVBFCuts_twoForwardJets', 'mjj_hist_afterVBFCuts_twoForwardJets', len(mjj_array)-1, mjj_array)	
	mjj_hist_afterVBFCuts_twoForwardJets.SetLineColor(ROOT.kRed)
	mjj_hist_afterVBFCuts_oneCentralJetOneForwardJet = ROOT.TH1F('mjj_hist_afterVBFCuts_oneCentralJetOneForwardJet', 'mjj_hist_afterVBFCuts_oneCentralJetOneForwardJet', len(mjj_array)-1, mjj_array)	
	mjj_hist_afterVBFCuts_oneCentralJetOneForwardJet.SetLineColor(ROOT.kRed)
	
	mjj_hist_afterVBFCutsAndTrigger_twoCentralJets = ROOT.TH1F('mjj_hist_afterVBFCutsAndTrigger_twoCentralJets', 'mjj_hist_afterVBFCutsAndTrigger_twoCentralJets', len(mjj_array)-1, mjj_array)
	mjj_hist_afterVBFCutsAndTrigger_twoCentralJets.SetLineColor(ROOT.kBlack)
	mjj_hist_afterVBFCutsAndTrigger_twoForwardJets = ROOT.TH1F('mjj_hist_afterVBFCutsAndTrigger_twoForwardJets', 'mjj_hist_afterVBFCutsAndTrigger_twoForwardJets', len(mjj_array)-1, mjj_array)
	mjj_hist_afterVBFCutsAndTrigger_twoForwardJets.SetLineColor(ROOT.kBlack)
	mjj_hist_afterVBFCutsAndTrigger_oneCentralJetOneForwardJet = ROOT.TH1F('mjj_hist_afterVBFCutsAndTrigger_oneCentralJetOneForwardJet', 'mjj_hist_afterVBFCutsAndTrigger_oneCentralJetOneForwardJet', len(mjj_array)-1, mjj_array)
	mjj_hist_afterVBFCutsAndTrigger_oneCentralJetOneForwardJet.SetLineColor(ROOT.kBlack)

	vbfCuts = 'minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && Flag_BadPFMuonFilter == 1 && Flag_goodVertices == 1 && Flag_globalSuperTightHalo2016Filter == 1 && Flag_HBHENoiseFilter == 1 && Flag_HBHENoiseIsoFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && jet_pt[0] > ' + str(leadingJetPtCut) + ' && jet_pt[1] > ' + str(trailingJetPtCut)

	vbfAndTriggerCuts = vbfCuts + ' && ' + trigger + ' == 1'

	twoCentralJets_cut = '(abs(jet_eta[0]) <= 2.5 && abs(jet_eta[1]) <= 2.5)'
	twoForwardJets_cut = '(abs(jet_eta[0]) > 2.5 && abs(jet_eta[1]) > 2.5)'
	oneCentralJetOneForwardJet_cut = '((abs(jet_eta[0]) <= 2.5 && abs(jet_eta[1]) > 2.5) || (abs(jet_eta[0]) > 2.5 && abs(jet_eta[1]) <= 2.5))'

	f.eventTree.Draw('mjj>>mjj_hist_twoCentralJets', twoCentralJets_cut, '')
	f.eventTree.Draw('mjj>>mjj_hist_twoForwardJets', twoForwardJets_cut, '')
	f.eventTree.Draw('mjj>>mjj_hist_oneCentralJetOneForwardJet', oneCentralJetOneForwardJet_cut, '')
	
	f.eventTree.Draw('mjj>>mjj_hist_afterVBFCuts_twoCentralJets', vbfCuts + ' && ' + twoCentralJets_cut, '')
	f.eventTree.Draw('mjj>>mjj_hist_afterVBFCuts_twoForwardJets', vbfCuts + ' && ' + twoForwardJets_cut, '')
	f.eventTree.Draw('mjj>>mjj_hist_afterVBFCuts_oneCentralJetOneForwardJet', vbfCuts + ' && ' + oneCentralJetOneForwardJet_cut, '')
	
	f.eventTree.Draw('mjj>>mjj_hist_afterVBFCutsAndTrigger_twoCentralJets', vbfAndTriggerCuts + ' && ' + twoCentralJets_cut, '')
	f.eventTree.Draw('mjj>>mjj_hist_afterVBFCutsAndTrigger_twoForwardJets', vbfAndTriggerCuts + ' && ' + twoForwardJets_cut, '')
	f.eventTree.Draw('mjj>>mjj_hist_afterVBFCutsAndTrigger_oneCentralJetOneForwardJet', vbfAndTriggerCuts + ' && ' + oneCentralJetOneForwardJet_cut, '')

	####
	print('Events passing VBF cuts: {}'.format(f.eventTree.GetEntries(vbfCuts)))
	print('Events passing VBF cuts + {}: {}\n'.format(trigger, f.eventTree.GetEntries(vbfAndTriggerCuts)))
	####	

	#Go to the directory (in the ROOT file) for trigger efficiencies 

	folderName = 'triggerEff_mjj_leadingJetPtCut' + str(leadingJetPtCut) + '_trailingJetPtCut' + str(trailingJetPtCut)
	
	try: out.GetKey(folderName).IsFolder()

	except ReferenceError: 

		out.mkdir(folderName, folderName) 

	out.cd(folderName)

	#Name of the directory to save the png files, and the name of the png file
	
	pngDir = 'pngImages/triggerEffPlots/mjjPlots/leadingJetPtCut' + str(leadingJetPtCut) + '_trailingJetPtCut' + str(trailingJetPtCut)
	file_name = trigger + '_mjj_leadingJetPt' + str(leadingJetPtCut) + '_trailingJetPt' + str(trailingJetPtCut) + '.png'
	
	constructTriggerEff(mjj_hist_afterVBFCutsAndTrigger_twoCentralJets, mjj_hist_afterVBFCuts_twoCentralJets, trigger, args, pngDir, file_name)
	constructTriggerEff(mjj_hist_afterVBFCutsAndTrigger_twoForwardJets, mjj_hist_afterVBFCuts_twoForwardJets, trigger, args, pngDir, file_name)
	constructTriggerEff(mjj_hist_afterVBFCutsAndTrigger_oneCentralJetOneForwardJet, mjj_hist_afterVBFCuts_oneCentralJetOneForwardJet, trigger, args, pngDir, file_name)
	
	out.cd()
	
	#Browse (create if necessary) the folder for individual histograms

	histoDirName = 'mjjHistos_leadingJetPtCut' + str(leadingJetPtCut) + '_trailingJetPtCut' + str(trailingJetPtCut)

	try: out.GetKey(histoDirName).IsFolder()

	except ReferenceError: 

		out.mkdir(histoDirName, histoDirName) 
	
	out.cd(histoDirName)

	if not args.noWrite:
	
		mjj_hist_twoCentralJets.Write('mjj_hist_twoCentralJets')
		mjj_hist_twoForwardJets.Write('mjj_hist_twoForwardJets')
		mjj_hist_oneCentralJetOneForwardJet.Write('mjj_hist_oneCentralJetOneForwardJet')
		
		mjj_hist_afterVBFCuts_twoCentralJets.Write('mjj_hist_afterVBFCuts_twoCentralJets')
		mjj_hist_afterVBFCuts_twoForwardJets.Write('mjj_hist_afterVBFCuts_twoForwardJets')
		mjj_hist_afterVBFCuts_oneCentralJetOneForwardJet.Write('mjj_hist_afterVBFCuts_oneCentralJetOneForwardJet')
		
		mjj_hist_afterVBFCutsAndTrigger_twoCentralJets.Write('mjj_hist_afterVBFCutsAndTrigger_twoCentralJets_' + trigger)
		mjj_hist_afterVBFCutsAndTrigger_twoForwardJets.Write('mjj_hist_afterVBFCutsAndTrigger_twoForwardJets_' + trigger)
		mjj_hist_afterVBFCutsAndTrigger_oneCentralJetOneForwardJet.Write('mjj_hist_afterVBFCutsAndTrigger_oneCentralJetOneForwardJet_' + trigger)
	
	mjj_hist_twoCentralJets.SetDirectory(0)
	mjj_hist_twoForwardJets.SetDirectory(0)
	mjj_hist_oneCentralJetOneForwardJet.SetDirectory(0)
	
	mjj_hist_afterVBFCuts_twoCentralJets.SetDirectory(0)
	mjj_hist_afterVBFCuts_twoForwardJets.SetDirectory(0)
	mjj_hist_afterVBFCuts_oneCentralJetOneForwardJet.SetDirectory(0)
	
	mjj_hist_afterVBFCutsAndTrigger_twoCentralJets.SetDirectory(0)
	mjj_hist_afterVBFCutsAndTrigger_twoForwardJets.SetDirectory(0)
	mjj_hist_afterVBFCutsAndTrigger_oneCentralJetOneForwardJet.SetDirectory(0)

	out.cd()
	
	out.Close()	
	f.Close()



