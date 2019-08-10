import ROOT 
import numpy as np
import os

def fillAndSave_MjjMETHisto(tree, allCuts, fileName, histoName=None, scale=False, saveToROOTFile=False):

	'''
	Used by other draw2DHisto functions to fill, draw and save the 2D histogram,
	given all the cuts applied and the eventTree.

	allCuts must be a string containing all the cuts applied.

	File name must be provided to save the png file.

	Saves the relevant histogram in the relevant directory as a png file.

	===ARGUMENTS===
	--- tree           : The eventTree in the ROOT file.
	--- allCuts        : A string containing all the cuts applied, including trigger cuts.
	--- fileName       : Name of the png file to be saved.
	--- histoName      : Name of the histogram to be saved in the ROOT file.
						 If the histogram won't be saved in a ROOT file, the default value None can be used.
	--- scale          : If scale is False, the number of events in the resulting histogram won't be scaled. (default)
				   		 If histogram is to be scaled, scale must be an integer or float specifying the scale factor.  
			 	   		 Histogram will be multiplied by the provided scaleFactor at the end.
	--- saveToROOTFile : If True, the histogram will be saved into a ROOT file. By default, this option is False.

	Returns the filled histogram.
	''' 
	# No stat box in the histogram
	
	ROOT.gStyle.SetOptStat(0)
	
	# Plot with numbers printed on bins

	ROOT.gStyle.SetPaintTextFormat('.2g')

	mjj_array = np.arange(500., 5000., 450.)
	met_array = np.arange(50., 300., 20.)
	
	if saveToROOTFile:

		if not 'out1.root' in os.listdir('.'):

			out = ROOT.TFile('out1.root', 'RECREATE')

		else:

			out = ROOT.TFile('out1.root', 'UPDATE')

	# Get whether the histogram is for events passing VBF trigger
	# or MET trigger.

	histoType = fileName.split('_')[-1]

	if histoName:
	
		histo = ROOT.TH2F(histoName, histoName, len(met_array)-1, met_array, len(mjj_array)-1, mjj_array)	

		tree.Draw('mjj:met>>{}'.format(histoName), allCuts, '')

	else:

		histo = ROOT.TH2F('histo', 'histo', len(met_array)-1, met_array, len(mjj_array)-1, mjj_array)

		tree.Draw('mjj:met>>histo', allCuts, '')
	
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

	# Scale the histogram if requested
	
	if scale: 

		scaleFactor = scale
		print('INFO: Scaling the 2D histogram by {}'.format(scaleFactor))
		histo.Scale(scaleFactor)

	# Get the relevant dir, create one if neccessary

	pngDir = 'pngImages/mjj_MET2DPlots'

	if not os.path.isdir(pngDir): os.makedirs(pngDir)

	file_path = os.path.join(pngDir, fileName)

	# Define the canvas and print the histogram

	canv = ROOT.TCanvas('canv', 'canv', 800, 600)

	histo.Draw('COLZ,TEXT')
	
	canv.Print(file_path)

	if saveToROOTFile:
	
		out.Write()

	# Seperate the histogram from the current working directory
	# i.e. the ROOT file

	histo.SetDirectory(0)

	print('*'*20)
	print('INFO: {} saved'.format(file_path))
	print('*'*20 + '\n')

	#out.Close()

	return histo

def draw2DHistoForEventsAcceptedOnlyByVBFTrigger(dataFile, vbfTrigger, metTrigger, cuts, scale=False, saveToROOTFile=False):

	'''
	Plots and saves 2D histogram for events that are passing the VBF trigger,
	but not passing the MET trigger.

	Reads the data from the eventTree in the given dataFile.

	On the histogram:
	x-axis: MET 
	y-axis: mjj

	===ARGUMENTS===
	--- dataFile       : The input ROOT file containing the eventTree
	--- vbfTrigger     : VBF trigger in consideration 
	--- metTrigger     : MET trigger in consideration
	--- cuts           : A list or tuple containing leading jet pt and trailing jet pt cuts: (leadJetPt, trailingJetPt)
	--- scale          : If scale is False, the number of events in the resulting histogram won't be scaled. (default)
				 	     If histogram is to be scaled, scale must be a tuple of the following form: (True, scaleFactor)
			 		     Histogram will be multiplied by the provided scaleFactor at the end.
	--- saveToROOTFile : If True, the histogram will be saved into a ROOT file. By default, this option is False.

	Returns the filled histogram.
	'''

	if len(cuts) != 2: raise ValueError('Number of cuts should be exactly 2!')

	if not (isinstance(cuts, list) or isinstance(cuts, tuple)): raise TypeError('cuts must be provided as a list or tuple!')

	# Proceed if no problem

	leadJetPtCut, trailJetPtCut = cuts[0], cuts[1]

	allCuts = 'minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && jet_pt[0] > ' + str(leadJetPtCut) + ' && jet_pt[1] > ' + str(trailJetPtCut) 
	
	# Append the trigger business

	allCuts += ' && {0} == 0 && {1} == 1 '.format(metTrigger, vbfTrigger)

	f = ROOT.TFile(dataFile)
	tree = f.eventTree

	fileName = dataFile.replace('.root', '')

	if 'inputs' in fileName:
	
		fileName = fileName.split('/')[-1]		

	fileName += '_mjj_METHisto_passingOnlyVBF.png'

	histoName = 'EventsAcc_OnlyByVBFTrigger'

	#fileName = 'mjj_METHisto_leadJetPtCut{0}_trailJetPtCut{1}_passingOnlyVBF.png'.format(leadJetPtCut, trailJetPtCut)

	filledHisto = fillAndSave_MjjMETHisto(tree, allCuts, fileName, histoName, scale, saveToROOTFile) 

	# Temporary
	filledHisto.RebinY(2)
	
	# This will seperate the histogram from the current file directory,
	# making it possible to use inside other functions, scripts etc.

	filledHisto.SetDirectory(0)

	f.Close()
	
	return filledHisto

def draw2DHistoForEventsAcceptedByMETTrigger(dataFile, metTrigger, cuts, scale=False, saveToROOTFile=False):
	
	'''
	Plots a 2D histogram for events that are passing the MET trigger.

	Reads the data from the eventTree in the given dataFile.

	On the histogram:
	x-axis: MET 
	y-axis: mjj

	===ARGUMENTS===
	--- dataFile       : Input ROOT file containing eventTree.
	--- metTrigger     : MET trigger in consideration.
	--- cuts   	       : A list or tuple containing leading jet pt and trailing jet pt cuts: (leadJetPt, trailJetPt)
	--- scale          : If scale is False, the number of events in the resulting histogram won't be scaled. (default)
				         If histogram is to be scaled, scale must be an integer or float specifying the scale factor.  
			 	         Histogram will be multiplied by the provided scaleFactor at the end.
	--- saveToROOTFile : If True, the histogram will be saved into a ROOT file. By default, this option is False.

	Returns the filled histogram.
	'''
	# No stat box in the histogram
	
	ROOT.gStyle.SetOptStat(0)

	if len(cuts) != 2: raise ValueError('Number of cuts should be exactly 2!')

	if not (isinstance(cuts, list) or isinstance(cuts, tuple)): raise TypeError('cuts must be provided as a list or tuple!')

	# Proceed if no problem

	leadJetPtCut, trailJetPtCut = cuts[0], cuts[1]

	allCuts = 'minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && jet_pt[0] > ' + str(leadJetPtCut) + ' && jet_pt[1] > ' + str(trailJetPtCut) 
	
	# Append the trigger business

	allCuts += ' && {} == 1'.format(metTrigger)
	
	f = ROOT.TFile(dataFile)
	tree = f.eventTree
	
	fileName = dataFile.replace('.root', '')
	
	if 'inputs' in fileName:
	
		fileName = fileName.split('/')[-1]		

	fileName += '_mjj_METHisto_passingMET.png'

	histoName = 'EventsAcc_ByMETTrigger'
	
	#fileName = 'mjj_METHisto_leadJetPtCut{0}_trailJetPtCut{1}_passingMET.png'.format(leadJetPtCut, trailJetPtCut)

	filledHisto = fillAndSave_MjjMETHisto(tree, allCuts, fileName, histoName, scale, saveToROOTFile)

	# Temporary
	filledHisto.RebinY(2)

	# This will seperate the histogram from the current file directory,
	# making it possible to use inside other functions, scripts etc.

	filledHisto.SetDirectory(0)

	f.Close()
	
	return filledHisto

def draw2DHistoForPercentageVBFTriggerGain(dataFile, vbfTrigger, metTrigger, cuts, scale=False, saveToROOTFile=False):

	'''
	Plots a 2D histogram containing the ratio of the following as a function of mjj and MET:
	-- Number of events that pass the given VBF trigger but not the given MET trigger
	-- Number of events that pass the given MET trigger
	
	===ARGUMENTS===
	--- dataFile       : Input ROOT file containing eventTree.
	--- vbfTrigger     : VBF trigger in consideration.
	--- metTrigger     : MET trigger in consideration.
	--- cuts   	       : A list or tuple containing leading jet pt and trailing jet pt cuts: (leadJetPt, trailJetPt)
	--- scale          : If scale is False, the number of events in the resulting histogram won't be scaled. (default)
				 	     If histogram is to be scaled, scale must be a tuple of the following form: (True, scaleFactor)
			 		     Histogram will be multiplied by the provided scaleFactor at the end.
	--- saveToROOTFile : If True, the histogram will be saved into a ROOT file. By default, this option is False.

	Saves the 2D histogram in the relevant directory.

	Doesn't return anything.
	'''
	# No stat box in thee histogram

	ROOT.gStyle.SetOptStat(0)
	
	# Plot with numbers printed on bins

	ROOT.gStyle.SetPaintTextFormat('.2g')

	if len(cuts) != 2: raise ValueError('Number of cuts should be exactly 2!')

	if not (isinstance(cuts, list) or isinstance(cuts, tuple)): raise TypeError('cuts must be provided as a list or tuple!')

	leadJetPtCut, trailJetPtCut = cuts[0], cuts[1]

	histo_eventsPassingMETTrigger = draw2DHistoForEventsAcceptedByMETTrigger(dataFile, metTrigger, cuts, scale, saveToROOTFile)

	histo_eventsPassingVBFTrigger_failingMETTrrigger = draw2DHistoForEventsAcceptedOnlyByVBFTrigger(dataFile, vbfTrigger, metTrigger, cuts, scale, saveToROOTFile)

	# Divide the two histograms

	histo_eventsPassingVBFTrigger_failingMETTrrigger.Divide(histo_eventsPassingMETTrigger)

	pngDir = 'pngImages/mjj_MET2DPlots'

	if not os.path.isdir(pngDir): os.makedirs(pngDir)

	fileName = dataFile.replace('.root', '')
	
	if 'inputs' in fileName:
	
		fileName = fileName.split('/')[-1]		

	fileName += '_mjj_METHisto_ratioHist.png'

	#fileName = 'mjj_METHisto_RatioHist_leadJetPtCut{0}_trailJetPtCut{1}.png'.format(leadJetPtCut, trailJetPtCut)

	file_path = os.path.join(pngDir, fileName)

	# Define the canvas and print the histogram

	canv = ROOT.TCanvas('canv', 'canv', 800, 600)

	histo_eventsPassingVBFTrigger_failingMETTrrigger.Draw('COLZ,TEXT,E')
	
	canv.Print(file_path)

	print('*'*20)
	print('INFO: {} saved'.format(file_path))
	print('*'*20 + '\n')
	
##################################

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
	




