import ROOT
import numpy as np
import os
from array import array

def drawCompGraph(histo1, histo2, label1, label2, variable, cuts, case=None):

	'''
	Fundamental drawer function used by other functions.
	
	Draws and saves the comparison graph for two given histograms.
	Labels (label1 and label2) are trigger labels to be shown in the legend. Also will appear in the png filename.
	Variable that will be on the x-axis should be specified: MET, leadingJetPt, trailingJetPt or mjj.

	There are three available case options: Two jets in barrel, endcap or one in each region.
	This must be specified in the case option while calling the function.
	If case is None (default), no region seperation will be done.	

	Cuts applied must be given as a list for the cuts argument. 
	
	'''

	#Check the variable and case arguments

	if variable not in ['MET', 'leadingJetPt', 'trailingJetPt', 'mjj']:

		raise ValueError('Variable argument is not correctly given! This argument should be one of the following: MET, leadingJetPt, trailingJetPt, mjj')

	if not (case in ['twoJetsInEndcap', 'twoJetsInBarrel', 'oneJetInBarrel_oneJetInEndcap'] or case == None):

		raise ValueError('Case argument is not correctly given! This argument should be either None (default) or one of the following: twoJetsInEndcap, twoJetsInBarrel, oneJetInBarrel_oneJetInEndcap')

	#Proceed if there is no problem 

	mjjCut, leadingJetPtCut, trailingJetPtCut = cuts[0], cuts[1], cuts[2]

	histo1.SetLineColor(ROOT.kBlack)
	histo1.SetLineWidth(2)
	
	histo2.SetLineColor(ROOT.kRed)
	histo2.SetLineWidth(2)

	legend = ROOT.TLegend(0.6, 0.6, 0.85, 0.85)
	legend.SetBorderSize(0)
	
	legend.AddEntry(histo1, label1, 'l')
	legend.AddEntry(histo2, label2, 'l')

	canv = ROOT.TCanvas('canv', 'canv')

	x_label = variable + ' (GeV)' #x-axis label
	
	if histo2.GetMaximum() > histo1.GetMaximum():
		
		histo2.GetXaxis().SetTitle(x_label)
		histo2.GetYaxis().SetTitle('Number of Events')

		histo2.SetTitle('')

		histo2.Draw()
		histo1.Draw('same')
	
	else:
	
		histo1.GetXaxis().SetTitle(x_label)
		histo1.GetYaxis().SetTitle('Number of Events')

		histo1.SetTitle('')

		histo1.Draw()
		histo2.Draw('same')

	legend.Draw('same')
	
	if variable == 'mjj':

		filename = label1 + '_' + label2 + '_' + str(leadingJetPtCut) + '_' + str(trailingJetPtCut) + '.png'
	
	elif variable == 'MET':

		filename = label1 + '_' + label2 + '_' + str(mjjCut) + '_' + str(leadingJetPtCut) + '_' + str(trailingJetPtCut) + '.png'

	#Take or create the relevant directory to save png files

	if case:
	
		dirName = 'pngImages/triggerCompPlots/' + variable + '_plots/' + case
	
	else:

		dirName = 'pngImages/triggerCompPlots/' + variable + '_plots/allInclusive'
	
	if not os.path.isdir(dirName):

		os.makedirs(dirName)

	filePath = os.path.join(dirName, filename)

	canv.Print(filePath)

	print('{} comparison plot saved'.format(variable))
	print('Filename: {}\n'.format(filePath))

############################################

def drawCompGraph_mjj(dataFile, trigger1, trigger2, label1, label2, cuts, seperateRegions=False):

	'''
	Draws the VBF cuts + trigger acceptance graph for two triggers, as a function of invariant mass of two jets, mjj.
	Takes the data from the input eventTree.
	Cuts on mjj, leadingJetPt, trailingJetPt and met must be specified in the cuts list.
	If seperateRegions option is specified as True, comparison graphs for three different cases are to be plotted:
	--- Two Forward Jets
	--- Two Central Jets
	--- Mixed (one central, one forward jet)
	'''

	print('Working on mjj comparison plot')
	print('Trigger1 : {}'.format(label1))
	print('Trigger2 : {}'.format(label2))

	ROOT.gStyle.SetOptStat(0)
	#ROOT.TH1.AddDirectory(False)

	mjj_array = np.arange(500., 5000., 100.)  

	fin = ROOT.TFile(dataFile)

	#Get the relevant cuts
	leadingJetPtCut, trailingJetPtCut = cuts[1], cuts[2]

	if seperateRegions:

	#############################
	#THIS BLOCK IS TO BE UPDATED FOR THE NEW DATA FILES
	#DON'T USE IT RIGHT NOW
	#############################

		hist1_twoJetsInBarrel = ROOT.TH1F('hist1_twoJetsInBarrel', trigger1, len(mjj_array) - 1, array('f', mjj_array))
		hist2_twoJetsInBarrel = ROOT.TH1F('hist2_twoJetsInBarrel', trigger2, len(mjj_array) - 1, array('f', mjj_array))
		hist1_twoJetsInEndcap = ROOT.TH1F('hist1_twoJetsInEndcap', trigger1, len(mjj_array) - 1, array('f', mjj_array))
		hist2_twoJetsInEndcap = ROOT.TH1F('hist2_twoJetsInEndcap', trigger2, len(mjj_array) - 1, array('f', mjj_array))
		hist1_oneJetInBarrel_oneJetInEndcap = ROOT.TH1F('hist1_oneJetInBarrel_oneJetInEndcap', trigger1, len(mjj_array) - 1, array('f', mjj_array))
		hist2_oneJetInBarrel_oneJetInEndcap = ROOT.TH1F('hist2_oneJetInBarrel_oneJetInEndcap', trigger2, len(mjj_array) - 1, array('f', mjj_array))

		cuts1 = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && mjj > ' + str(mjjCut) + ' && jet_pt[0] > ' + str(leadingJetPtCut) + ' && jet_pt[1] > ' + str(trailingJetPtCut) + ' && ' + trigger1 + ' == 1' 

		cuts2 = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && mjj > ' + str(mjjCut) + ' && jet_pt[0] > ' + str(leadingJetPtCut) + ' && jet_pt[1] > ' + str(trailingJetPtCut) + ' && ' + trigger2 + ' == 1' 

		fin.cd()

		#####################
		#ETA RANGES SHOULD BE CHECKED!
		#####################

		fin.eventTree.Draw('mjj>>hist1_twoJetsInBarrel', cuts1 + ' && abs(jet_eta[0]) < 1.479 && abs(jet_eta[1]) < 1.479', '') 
		fin.eventTree.Draw('mjj>>hist2_twoJetsInBarrel', cuts2 + ' && abs(jet_eta[0]) < 1.479 && abs(jet_eta[1]) < 1.479', '')
		
		fin.eventTree.Draw('mjj>>hist1_twoJetsInEndcap', cuts1 + ' && abs(jet_eta[0]) > 1.479 && abs(jet_eta[1]) > 1.479', '')
		fin.eventTree.Draw('mjj>>hist2_twoJetsInEndcap', cuts2 + ' && abs(jet_eta[0]) > 1.479 && abs(jet_eta[1]) > 1.479', '')

		fin.eventTree.Draw('mjj>>hist1_oneJetInBarrel_oneJetInEndcap', cuts1 + ' && (abs(jet_eta[0]) > 1.479 && abs(jet_eta[1]) < 1.479) || (abs(jet_eta[0]) < 1.479 && abs(jet_eta[1]) > 1.479)', '')
		fin.eventTree.Draw('mjj>>hist2_oneJetInBarrel_oneJetInEndcap', cuts2 + ' && (abs(jet_eta[0]) > 1.479 && abs(jet_eta[1]) < 1.479) || (abs(jet_eta[0]) < 1.479 && abs(jet_eta[1]) > 1.479)', '')
		
		#Construct histograms for all cases 
		
		drawCompGraph(hist1_twoJetsInBarrel, hist2_twoJetsInBarrel, label1, label2, 'mjj', 'twoJetsInBarrel', cuts)

		drawCompGraph(hist1_twoJetsInEndcap, hist2_twoJetsInEndcap, label1, label2, 'mjj', 'twoJetsInEndcap', cuts)

		drawCompGraph(hist1_oneJetInBarrel_oneJetInEndcap, hist2_oneJetInBarrel_oneJetInEndcap, label1, label2, 'mjj', 'oneJetInBarrel_oneJetInEndcap', cuts)
		
	else:

		hist1 = ROOT.TH1F('hist1', trigger1, len(mjj_array)-1, mjj_array)
		hist2 = ROOT.TH1F('hist2', trigger2, len(mjj_array)-1, mjj_array)
		
		cuts1 = 'minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && jet_pt[0] > ' + str(leadingJetPtCut) + ' && jet_pt[1] > ' + str(trailingJetPtCut) + ' && ' + trigger1 + ' == 1' 
		cuts2 = 'minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && jet_pt[0] > ' + str(leadingJetPtCut) + ' && jet_pt[1] > ' + str(trailingJetPtCut) + ' && ' + trigger2 + ' == 1' 

		fin.eventTree.Draw('mjj>>hist1', cuts1, '')
		fin.eventTree.Draw('mjj>>hist2', cuts2, '')

		drawCompGraph(hist1, hist2, label1, label2, 'mjj', cuts)

	fin.Close()

###########################

def drawCompGraph_MET(dataFile, trigger1, trigger2, label1, label2, cuts, seperateRegions=False):

	'''
	Draws the VBF cuts + trigger acceptance graph for two triggers, as a function of MET.
	Takes the data from the input eventTree.
	Cuts on mjj, leadingJetPt, trailingJetPt and met must be specified in the cuts list.
	'''

	print('Working on MET comparison plot')
	print('Trigger1 : {}'.format(label1))
	print('Trigger2 : {}'.format(label2))

	ROOT.gStyle.SetOptStat(0)
	#ROOT.TH1.AddDirectory(False)

	met_array = np.arange(50., 500., 25.)  

	fin = ROOT.TFile(dataFile)

	#Get the relevant cuts
	mjjCut, leadingJetPtCut, trailingJetPtCut = cuts[0], cuts[1], cuts[2]

	if seperateRegions:

	#############################
	#THIS BLOCK IS TO BE UPDATED FOR THE NEW DATA FILES
	#DON'T USE IT RIGHT NOW
	#############################
		
		hist1_twoJetsInBarrel = ROOT.TH1F('hist1_twoJetsInBarrel', trigger1, len(met_array) - 1, array('f', met_array))
		hist2_twoJetsInBarrel = ROOT.TH1F('hist2_twoJetsInBarrel', trigger2, len(met_array) - 1, array('f', met_array))
		hist1_twoJetsInEndcap = ROOT.TH1F('hist1_twoJetsInEndcap', trigger1, len(met_array) - 1, array('f', met_array))
		hist2_twoJetsInEndcap = ROOT.TH1F('hist2_twoJetsInEndcap', trigger2, len(met_array) - 1, array('f', met_array))
		hist1_oneJetInBarrel_oneJetInEndcap = ROOT.TH1F('hist1_oneJetInBarrel_oneJetInEndcap', trigger1, len(met_array) - 1, array('f', met_array))
		hist2_oneJetInBarrel_oneJetInEndcap = ROOT.TH1F('hist2_oneJetInBarrel_oneJetInEndcap', trigger2, len(met_array) - 1, array('f', met_array))

		cuts1 = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && mjj > ' + str(mjjCut) + ' && jet_pt[0] > ' + str(leadingJetPtCut) + ' && jet_pt[1] > ' + str(trailingJetPtCut) + ' && ' + trigger1 + ' == 1' 

		cuts2 = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && mjj > ' + str(mjjCut) + ' && jet_pt[0] > ' + str(leadingJetPtCut) + ' && jet_pt[1] > ' + str(trailingJetPtCut) + ' && ' + trigger2 + ' == 1' 

		fin.cd()

		#####################
		#ETA RANGES SHOULD BE CHECKED!
		#####################

		fin.eventTree.Draw('met>>hist1_twoJetsInBarrel', cuts1 + ' && abs(jet_eta[0]) < 1.479 && abs(jet_eta[1]) < 1.479', '') 
		fin.eventTree.Draw('met>>hist2_twoJetsInBarrel', cuts2 + ' && abs(jet_eta[0]) < 1.479 && abs(jet_eta[1]) < 1.479', '')
		
		fin.eventTree.Draw('met>>hist1_twoJetsInEndcap', cuts1 + ' && abs(jet_eta[0]) > 1.479 && abs(jet_eta[1]) > 1.479', '')
		fin.eventTree.Draw('met>>hist2_twoJetsInEndcap', cuts2 + ' && abs(jet_eta[0]) > 1.479 && abs(jet_eta[1]) > 1.479', '')

		fin.eventTree.Draw('met>>hist1_oneJetInBarrel_oneJetInEndcap', cuts1 + ' && ((abs(jet_eta[0]) > 1.479 && abs(jet_eta[1]) < 1.479) || (abs(jet_eta[0]) < 1.479 && abs(jet_eta[1]) > 1.479))', '')
		fin.eventTree.Draw('met>>hist2_oneJetInBarrel_oneJetInEndcap', cuts2 + ' && ((abs(jet_eta[0]) > 1.479 && abs(jet_eta[1]) < 1.479) || (abs(jet_eta[0]) < 1.479 && abs(jet_eta[1]) > 1.479))', '')

		#Construct histograms for all cases 
		
		drawCompGraph(hist1_twoJetsInBarrel, hist2_twoJetsInBarrel, label1, label2, 'MET', 'twoJetsInBarrel', cuts)

		drawCompGraph(hist1_twoJetsInEndcap, hist2_twoJetsInEndcap, label1, label2, 'MET', 'twoJetsInEndcap', cuts)

		drawCompGraph(hist1_oneJetInBarrel_oneJetInEndcap, hist2_oneJetInBarrel_oneJetInEndcap, label1, label2, 'MET', 'oneJetInBarrel_oneJetInEndcap', cuts)

	else:

		hist1 = ROOT.TH1F('hist1',  trigger1,  len(met_array)-1, met_array)
		hist2 = ROOT.TH1F('hist2',  trigger2,  len(met_array)-1, met_array)

		cuts1 = 'minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && mjj > ' + str(mjjCut) + ' && jet_pt[0] > ' + str(leadingJetPtCut) + ' && jet_pt[1] > ' + str(trailingJetPtCut) + ' && ' + trigger1 + ' == 1' 
		cuts2 = 'minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && mjj > ' + str(mjjCut) + ' && jet_pt[0] > ' + str(leadingJetPtCut) + ' && jet_pt[1] > ' + str(trailingJetPtCut) + ' && ' + trigger2 + ' == 1' 

		fin.eventTree.Draw('met>>hist1', cuts1, '')
		fin.eventTree.Draw('met>>hist2', cuts2, '')

		drawCompGraph(hist1, hist2, label1, label2, 'MET', cuts)

	fin.Close()

def drawDistributionForAcceptedOnlyByVBF(dataFile, variable, *argv):

	'''
	Draws the distribution of given variable for the events that are accepted by the VBF trigger,
	but rejected by the MET trigger specified.
	
	dataFile: The input file contatining the event tree.
	
	variable: The variable of interest to be plotted
	It can be mjj or MET at the moment.

	In argv, following must be provided with the correct order:
	--- VBF trigger in consideration
	--- MET trigger in consideration
	--- A list containing the jet pt cuts applied 
	'''

	vbfTrigger = argv[0]
	metTrigger = argv[1]
	cuts = argv[2]

	if len(cuts) == 2:

		leadingJetPtCut, trailingJetPtCut = cuts[0], cuts[1]
		allCuts = 'minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && jet_pt[0] > ' + str(leadingJetPtCut) + ' && jet_pt[1] > ' + str(trailingJetPtCut) 

	else:
		
		mjjCut, leadingJetPtCut, trailingJetPtCut, metCut = cuts[0], cuts[1], cuts[2], cuts[3]
		allCuts = 'minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && mjj > ' + str(mjjCut) + ' && met > ' + str(metCut[0]) + ' && met < ' + str(metCut[1]) + ' && jet_pt[0] > ' + str(leadingJetPtCut) + ' && jet_pt[1] > ' + str(trailingJetPtCut) 

	print(allCuts)
	
	# Append the trigger business
	
	allCuts += ' && {0} == 0 && {1} == 1'.format(metTrigger, vbfTrigger)

	canv = ROOT.TCanvas('canv', 'canv')

	fin = ROOT.TFile(dataFile)

	if variable == 'mjj':

		mjj_array = np.arange(500., 5000., 100.)

		histo = ROOT.TH1F('histo', 'Distn for Events Failing the VBF Trigger but Passing MET Trigger', len(mjj_array)-1, mjj_array)
		#histo.GetXaxis().SetTitle('mjj (GeV)')
		#histo.GetYaxis().SetTitle('Number of Events')

	elif variable == 'MET':

		met_array = np.arange(50., 500., 25.)

		histo = ROOT.TH1F('histo', 'Distn for Events Failing the VBF Trigger but Passing MET Trigger', len(met_array)-1, met_array)

	elif variable == 'leadJetPt':

		leadJetPt_array = np.arange(50., 500., 25.)
		histo = ROOT.TH1F('histo', 'Distn for Events Failing the VBF Trigger but Passing MET Trigger', len(leadJetPt_array)-1, leadJetPt_array)
	
	elif variable == 'trailJetPt':

		trailJetPt_array = np.arange(20., 300., 20.)
		histo = ROOT.TH1F('histo', 'Distn for Events Failing the VBF Trigger but Passing MET Trigger', len(trailJetPt_array)-1, trailJetPt_array)
	
	else:
	
		raise ValueError("variable argument must be one of the following: 'mjj', 'leadJetPt', 'trailJetPt' or 'MET'!") 

	# Print and save the distribution

	if variable in ['mjj', 'MET']:

		print(fin.eventTree.GetEntries(allCuts))
		fin.eventTree.Draw('{}>>histo'.format(variable.lower()), allCuts, '')
		hist = ROOT.gDirectory.Get('histo')
		hist.SetTitle('')
		hist.GetXaxis().SetTitle('{} (GeV)'.format(variable))
		hist.GetYaxis().SetTitle('Number of Events')

	elif variable == 'leadJetPt':

		fin.eventTree.Draw('jet_pt[0]>>histo', allCuts, '')
		hist = ROOT.gDirectory.Get('histo')
		hist.SetTitle('')
		hist.GetXaxis().SetTitle('{} (GeV)'.format(variable))
		hist.GetYaxis().SetTitle('Number of Events')

	elif variable == 'trailJetPt':

		fin.eventTree.Draw('jet_pt[1]>>histo', allCuts, '')
		hist = ROOT.gDirectory.Get('histo')
		hist.SetTitle('')
		hist.GetXaxis().SetTitle('{} (GeV)'.format(variable))
		hist.GetYaxis().SetTitle('Number of Events')
	
	fileName = '{}_notPassingMET.png'.format(variable)

	canv.Print(fileName)

	fin.Close()	



