import ROOT 
import numpy as np
import os

def fillAndSave_MjjMETHisto(tree, allCuts, fileName):

	'''
	Used by other draw2DHisto functions to fill, draw and save the 2D histogram,
	given all the cuts applied and the eventTree.

	allCuts must be a string containing all the cuts applied.

	File name must be provided to save the png file.

	Saves the relevant histogram in the relevant directory as a png file.

	Returns the filled histogram.
	''' 
	# No stat box in the histogram
	
	ROOT.gStyle.SetOptStat(0)
	
	# Plot with numbers printed on bins

	ROOT.gStyle.SetPaintTextFormat('.2g')

	mjj_array = np.arange(500., 5000., 450.)
	met_array = np.arange(50., 300., 20.)

	# Fill the histogram from the tree to a temp histogram

	hist = ROOT.TH2F('hist', 'hist', len(met_array)-1, met_array, len(mjj_array)-1, mjj_array)
	tree.Draw('mjj:met>>hist', allCuts, '')

	# Get whether the histogram is for events passing VBF trigger
	# or MET trigger.

	histoType = fileName.split('_')[-1]
	
	# Get the filled histogram

	histo = ROOT.gDirectory.Get('hist')
	
	if 'passingOnlyVBF' in histoType:
		histo.SetTitle('Events Passing VBF Trigger & Failing MET Trigger')

	elif 'passingMET' in histoType:
		histo.SetTitle('Events Passing MET Trigger') 

	elif 'EventsPassingVBF' in histoType:
		histo.SetTitle('Events Passing VBF Trigger')

	elif 'EventsWithoutVBF' in histoType:
		histo.SetTitle('Events Passing VBF Selections (No Trigger Req)')

	histo.GetXaxis().SetTitle('MET (GeV)')
	histo.GetYaxis().SetTitle('mjj (GeV)')
	
	# Get the relevant dir, create one if neccessary

	pngDir = 'pngImages/mjj_MET2DPlots'

	if not os.path.isdir(pngDir): os.makedirs(pngDir)

	file_path = os.path.join(pngDir, fileName)

	# Define the canvas and print the histogram

	canv = ROOT.TCanvas('canv', 'canv', 800, 600)

	histo.Draw('COLZ,TEXT')
	
	canv.Print(file_path)

	print('*'*20)
	print('INFO: {} saved'.format(file_path))
	print('*'*20 + '\n')

	return histo

def draw2DHistoForEventsAcceptedOnlyByVBFTrigger(dataFile, *argv):

	'''
	Plots and saves 2D histogram for events that are passing the VBF trigger,
	but not passing the MET trigger.

	Reads the data from the eventTree in the given dataFile.

	On the histogram:
	x-axis: MET 
	y-axis: mjj

	In extra arguments argv, following must be specified in the following order:
	--- VBF trigger 
	--- MET trigger
	--- Cuts provided as a list or tuple with the following entries: [leadingJetPtCut, trailingJetPtCut]

	Returns the filled histogram.
	'''


	vbfTrigger, metTrigger, cuts = argv[0], argv[1], argv[2]

	if len(cuts) != 2: raise ValueError('Number of cuts should be exactly 2!')

	if not (isinstance(cuts, list) or isinstance(cuts, tuple)): raise TypeError('cuts must be provided as a list or tuple!')

	# Proceed if no problem

	leadJetPtCut, trailJetPtCut = cuts[0], cuts[1]

	allCuts = 'minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && jet_pt[0] > ' + str(leadJetPtCut) + ' && jet_pt[1] > ' + str(trailJetPtCut) 
	
	# Append the trigger business

	allCuts += ' && {0} == 0 && {1} == 1 '.format(metTrigger, vbfTrigger)

	f = ROOT.TFile(dataFile)
	tree = f.eventTree

	fileName = 'mjj_METHisto_leadJetPtCut{0}_trailJetPtCut{1}_passingOnlyVBF.png'.format(leadJetPtCut, trailJetPtCut)

	filledHisto = fillAndSave_MjjMETHisto(tree, allCuts, fileName) 

	# This will seperate the histogram from the current file directory,
	# making it possible to use inside other functions, scripts etc.

	filledHisto.SetDirectory(0)

	f.Close()
	
	return filledHisto

def draw2DHistoForEventsAcceptedOnlyByMETTrigger(dataFile, *argv):
	
	'''
	Plots a 2D histogram for events that are passing the MET trigger.

	Reads the data from the eventTree in the given dataFile.

	On the histogram:
	x-axis: MET 
	y-axis: mjj

	In extra arguments argv, following must be specified in the following order:
	--- MET trigger
	--- Cuts provided as a list or tuple with the following entries: [leadingJetPtCut, trailingJetPtCut]

	Returns the filled histogram.
	'''
	# No stat box in the histogram
	
	ROOT.gStyle.SetOptStat(0)

	metTrigger, cuts = argv[0], argv[1]

	if len(cuts) != 2: raise ValueError('Number of cuts should be exactly 2!')

	if not (isinstance(cuts, list) or isinstance(cuts, tuple)): raise TypeError('cuts must be provided as a list or tuple!')

	# Proceed if no problem

	leadJetPtCut, trailJetPtCut = cuts[0], cuts[1]

	allCuts = 'minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && jet_pt[0] > ' + str(leadJetPtCut) + ' && jet_pt[1] > ' + str(trailJetPtCut) 
	
	# Append the trigger business

	allCuts += ' && {} == 1'.format(metTrigger)
	
	f = ROOT.TFile(dataFile)
	tree = f.eventTree
	
	fileName = 'mjj_METHisto_leadJetPtCut{0}_trailJetPtCut{1}_passingMET.png'.format(leadJetPtCut, trailJetPtCut)

	filledHisto = fillAndSave_MjjMETHisto(tree, allCuts, fileName)

	# This will seperate the histogram from the current file directory,
	# making it possible to use inside other functions, scripts etc.

	filledHisto.SetDirectory(0)

	f.Close()
	
	return filledHisto

def draw2DHistoForPercentageVBFTriggerGain(dataFile, *argv):

	'''
	Plots a 2D histogram containing the ratio of the following as a function of mjj and MET:
	-- Number of events that pass the given VBF trigger but not the given MET trigger
	-- Number of events that pass the given MET trigger

	Extra arguments argv must contain the following in the following order:
	--- The VBF trigger in consideration
	--- The MET trigger in consideration
	--- The cuts applied as a list or tuple: (leadJetPtCut, trailJetPtCut)

	Saves the 2D histogram in the relevant directory.

	Doesn't return anything.
	'''
	# No stat box in thee histogram

	ROOT.gStyle.SetOptStat(0)
	
	# Plot with numbers printed on bins

	ROOT.gStyle.SetPaintTextFormat('.2g')

	vbfTrigger, metTrigger, cuts = argv[0], argv[1], argv[2]
	
	if len(cuts) != 2: raise ValueError('Number of cuts should be exactly 2!')

	if not (isinstance(cuts, list) or isinstance(cuts, tuple)): raise TypeError('cuts must be provided as a list or tuple!')

	leadJetPtCut, trailJetPtCut = cuts[0], cuts[1]

	histo_eventsPassingMETTrigger = draw2DHistoForEventsAcceptedOnlyByMETTrigger(dataFile, metTrigger, cuts)

	histo_eventsPassingVBFTrigger_failingMETTrrigger = draw2DHistoForEventsAcceptedOnlyByVBFTrigger(dataFile, vbfTrigger, metTrigger, cuts)

	# Divide the two histograms

	histo_eventsPassingVBFTrigger_failingMETTrrigger.Divide(histo_eventsPassingMETTrigger)

	pngDir = 'pngImages/mjj_MET2DPlots'

	if not os.path.isdir(pngDir): os.makedirs(pngDir)

	fileName = 'mjj_METHisto_RatioHist_leadJetPtCut{0}_trailJetPtCut{1}.png'.format(leadJetPtCut, trailJetPtCut)

	file_path = os.path.join(pngDir, fileName)

	# Define the canvas and print the histogram

	canv = ROOT.TCanvas('canv', 'canv', 800, 600)

	histo_eventsPassingVBFTrigger_failingMETTrrigger.Draw('COLZ,TEXT')
	
	canv.Print(file_path)

	print('*'*20)
	print('INFO: {} saved'.format(file_path))
	print('*'*20 + '\n')
	
def draw2DHisto_PercentageOfEventsPassingVBFTrigger(dataFile, vbfTrigger, cuts):

	'''
	Fills, draws and saves a 2D histogram containing the ratio of number of events passing the VBF trigger,
	as a function of mjj and MET.
	
	Saves the histogram as a .png file in the relevant directory.
	
	ARGUMENTS:
	---inputFile: The ROOT file containing the eventTree.
	---vbfTrigger: VBF trigger in consideration.
	---cuts: A tuple or list of length 2, containing leading jet pt and trailing jet pt cuts: (leadJetPt, trailJetPt)
	''' 
	if len(cuts) != 2: raise ValueError('Number of cuts should be exactly 2!')

	if not (isinstance(cuts, list) or isinstance(cuts, tuple)): raise TypeError('cuts must be provided as a list or tuple!')

	# Proceed if no problem

	# No stat box in thee histogram

	ROOT.gStyle.SetOptStat(0)
	
	# Plot with numbers printed on bins

	ROOT.gStyle.SetPaintTextFormat('.2g')

	leadJetPtCut, trailJetPtCut = cuts[0], cuts[1]
	
	mainCuts = 'minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && jet_pt[0] > ' + str(leadJetPtCut) + ' && jet_pt[1] > ' + str(trailJetPtCut) 
	
	# Append the trigger business

	allCuts = mainCuts + ' && {} == 1'.format(vbfTrigger)
	
	f = ROOT.TFile(dataFile)
	tree = f.eventTree

	fileName_withVBFTrigger = 'mjj_METHisto_leadJetPtCut{0}_trailJetPtCut{1}_numEventsPassingVBFTrigger.png'.format(leadJetPtCut, trailJetPtCut)

	fileName_allEvents = 'mjj_METHisto_RatioHist_leadJetPtCut{0}_trailJetPtCut{1}_numEventsWithoutVBFTrigger.png'.format(leadJetPtCut, trailJetPtCut)
	
	# Get the two histograms

	hist = fillAndSave_MjjMETHisto(tree, allCuts, fileName_withVBFTrigger)

	hist_allEvents = fillAndSave_MjjMETHisto(tree, mainCuts, fileName_allEvents)

	# Divide the two histograms
	
	hist.Divide(hist_allEvents)

	# Save the ratio histogram

	pngDir = 'pngImages/mjj_MET2DPlots'

	if not os.path.isdir(pngDir): os.makedirs(pngDir)

	fileName = 'mjj_METHisto_RatioEventsPassingVBFTrig_leadJetPtCut{0}_trailJetPtCut{1}.png'.format(leadJetPtCut, trailJetPtCut)

	file_path = os.path.join(pngDir, fileName)

	# Define the canvas and print the histogram

	canv = ROOT.TCanvas('canv', 'canv', 800, 600)

	hist.Draw('COLZ,TEXT')
	
	canv.Print(file_path)

	print('*'*20)
	print('INFO: {} saved'.format(file_path))
	print('*'*20 + '\n')
	




