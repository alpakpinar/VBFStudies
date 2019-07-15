import ROOT
import numpy as np
import os
from array import array

def drawCompGraph(histo1, histo2, label1, label2, variable, case, cuts):

	'''
	Fundamental drawer function used by other functions.
	
	Draws and saves the comparison graph for two given histograms.
	Labels (label1 and label2) are trigger labels to be shown in the legend. Also will appear in the png filename.
	Variable that will be on the x-axis should be specified: MET, leadingJetPt, trailingJetPt or mjj.
	There are three available case options: Two jets in barrel, endcap or one in each region.
	This must be specified in the case option while calling the function.
	Cuts applied must be given as a list for the cuts argument. 
	
	'''

	#Check the variable and case arguments

	if variable not in ['MET', 'leadingJetPt', 'trailingJetPt', 'mjj']:

		raise ValueError('Variable argument is not correctly given! This argument should be one of the following: MET, leadingJetPt, trailingJetPt, mjj')

	if case not in ['twoJetsInEndcap', 'twoJetsInBarrel', 'oneJetInBarrel_oneJetInEndcap']:

		raise ValueError('Case argument is not correctly given! This argument should be one of the following: twoJetsInEndcap, twoJetsInBarrel, oneJetInBarrel_oneJetInEndcap')

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
	
	filename = label1 + '_' + label2 + '_' + variable + '_' + str(mjjCut) + '_' + str(leadingJetPtCut) + '_' + str(trailingJetPtCut) + '.png'
	
	#Take or create the relevant directory to save png files

	if case == 'twoJetsInBarrel':
		
		dirName = 'pngImages/triggerCompPlots/' + variable + '_plots/twoJetsInBarrel'

	elif case == 'twoJetsInEndcap':

		dirName = 'pngImages/triggerCompPlots/' + variable + '_plots/twoJetsInEndcap'

	elif case == 'oneJetInBarrel_oneJetInEndcap':

		dirName = 'pngImages/triggerCompPlots/' + variable + '_plots/oneJetInBarrel_oneJetInEndcap'

	if not os.path.isdir(dirName):

		os.makedirs(dirName)

	filePath = os.path.join(dirName, filename)

	canv.Print(filePath)

	print('MET comparison plot for the case ' + case + ' saved')
	print('Filename: {}\n'.format(filePath))

############################################

def drawCompGraph_mjj(dataFile, trigger1, trigger2, label1, label2, cuts):

	'''
	Draws the VBF cuts + trigger acceptance graph for two triggers, as a function of invariant mass of two jets, mjj.
	Takes the data from the input eventTree.
	Cuts on mjj, leadingJetPt, trailingJetPt and met must be specified in the cuts list.
	'''

	print('Working on mjj comparison plot')
	print('Trigger1 : {}'.format(label1))
	print('Trigger2 : {}'.format(label2))

	ROOT.gStyle.SetOptStat(0)
	#ROOT.TH1.AddDirectory(False)

	mjj_array = np.arange(500., 3000., 50.)  

	fin = ROOT.TFile(dataFile)

	#Get the relevant cuts
	mjjCut, leadingJetPtCut, trailingJetPtCut = cuts[0], cuts[1], cuts[2]

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
	
	fin.Close()

###########################

def drawCompGraph_trailingJetPt(dataFile, trigger1, trigger2, label1, label2, cuts):

	'''
	Draws the VBF cuts + trigger acceptance graph for two triggers, as a function of trailing jet pt.
	Takes the data from the input eventTree.
	Cuts on mjj, leadingJetPt, trailingJetPt and met must be specified in the cuts list.
	'''

	print('Working on trailing jet pt comparison plot')
	print('Trigger1 : {}'.format(label1))
	print('Trigger2 : {}'.format(label2))

	ROOT.gStyle.SetOptStat(0)
	#ROOT.TH1.AddDirectory(False)

	trailingJetPt_array = np.arange(40., 200., 5.)  

	fin = ROOT.TFile(dataFile)

	#Get the relevant cuts
	mjjCut, leadingJetPtCut, trailingJetPtCut = cuts[0], cuts[1], cuts[2]

	hist1_twoJetsInBarrel = ROOT.TH1F('hist1_twoJetsInBarrel', trigger1, len(trailingJetPt_array) - 1, array('f', trailingJetPt_array))
	hist2_twoJetsInBarrel = ROOT.TH1F('hist2_twoJetsInBarrel', trigger2, len(trailingJetPt_array) - 1, array('f', trailingJetPt_array))
	hist1_twoJetsInEndcap = ROOT.TH1F('hist1_twoJetsInEndcap', trigger1, len(trailingJetPt_array) - 1, array('f', trailingJetPt_array))
	hist2_twoJetsInEndcap = ROOT.TH1F('hist2_twoJetsInEndcap', trigger2, len(trailingJetPt_array) - 1, array('f', trailingJetPt_array))
	hist1_oneJetInBarrel_oneJetInEndcap = ROOT.TH1F('hist1_oneJetInBarrel_oneJetInEndcap', trigger1, len(trailingJetPt_array) - 1, array('f', trailingJetPt_array))
	hist2_oneJetInBarrel_oneJetInEndcap = ROOT.TH1F('hist2_oneJetInBarrel_oneJetInEndcap', trigger2, len(trailingJetPt_array) - 1, array('f', trailingJetPt_array))

	cuts1 = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && mjj > ' + str(mjjCut) + ' && jet_pt[0] > ' + str(leadingJetPtCut) + ' && jet_pt[1] > ' + str(trailingJetPtCut) + ' && ' + trigger1 + ' == 1' 

	cuts2 = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && mjj > ' + str(mjjCut) + ' && jet_pt[0] > ' + str(leadingJetPtCut) + ' && jet_pt[1] > ' + str(trailingJetPtCut) + ' && ' + trigger2 + ' == 1' 

	fin.cd()

	#####################
	#ETA RANGES SHOULD BE CHECKED!
	#####################

	fin.eventTree.Draw('jet_pt[1]>>hist1_twoJetsInBarrel', cuts1 + ' && abs(jet_eta[0]) < 1.479 && abs(jet_eta[1]) < 1.479', '') 
	fin.eventTree.Draw('jet_pt[1]>>hist2_twoJetsInBarrel', cuts2 + ' && abs(jet_eta[0]) < 1.479 && abs(jet_eta[1]) < 1.479', '')
	
	fin.eventTree.Draw('jet_pt[1]>>hist1_twoJetsInEndcap', cuts1 + ' && abs(jet_eta[0]) > 1.479 && abs(jet_eta[1]) > 1.479', '')
	fin.eventTree.Draw('jet_pt[1]>>hist2_twoJetsInEndcap', cuts2 + ' && abs(jet_eta[0]) > 1.479 && abs(jet_eta[1]) > 1.479', '')

	fin.eventTree.Draw('jet_pt[1]>>hist1_oneJetInBarrel_oneJetInEndcap', cuts1 + ' && ((abs(jet_eta[0]) > 1.479 && abs(jet_eta[1]) < 1.479) || (abs(jet_eta[0]) < 1.479 && abs(jet_eta[1]) > 1.479))', '')
	fin.eventTree.Draw('jet_pt[1]>>hist2_oneJetInBarrel_oneJetInEndcap', cuts2 + ' && ((abs(jet_eta[0]) > 1.479 && abs(jet_eta[1]) < 1.479) || (abs(jet_eta[0]) < 1.479 && abs(jet_eta[1]) > 1.479))', '')
	
	#Construct histograms for all cases 
	
	drawCompGraph(hist1_twoJetsInBarrel, hist2_twoJetsInBarrel, label1, label2, 'trailingJetPt', 'twoJetsInBarrel', cuts)

	drawCompGraph(hist1_twoJetsInEndcap, hist2_twoJetsInEndcap, label1, label2, 'trailingJetPt', 'twoJetsInEndcap', cuts)

	drawCompGraph(hist1_oneJetInBarrel_oneJetInEndcap, hist2_oneJetInBarrel_oneJetInEndcap, label1, label2, 'trailingJetPt', 'oneJetInBarrel_oneJetInEndcap', cuts)

	fin.Close()

###########################

def drawCompGraph_leadingJetPt(dataFile, trigger1, trigger2, label1, label2, cuts):

	'''
	Draws the VBF cuts + trigger acceptance graph for two triggers, as a function of leading jet pt.
	Takes the data from the input eventTree.
	Cuts on mjj, leadingJetPt, trailingJetPt and met must be specified in the cuts list.
	'''

	print('Working on leading jet pt comparison plot')
	print('Trigger1 : {}'.format(label1))
	print('Trigger2 : {}'.format(label2))

	ROOT.gStyle.SetOptStat(0)
	#ROOT.TH1.AddDirectory(False)

	leadingJetPt_array = np.arange(150., 450., 15.)  

	fin = ROOT.TFile(dataFile)

	#Get the relevant cuts
	mjjCut, leadingJetPtCut, trailingJetPtCut = cuts[0], cuts[1], cuts[2]

	hist1_twoJetsInBarrel = ROOT.TH1F('hist1_twoJetsInBarrel', trigger1, len(leadingJetPt_array) - 1, array('f', leadingJetPt_array))
	hist2_twoJetsInBarrel = ROOT.TH1F('hist2_twoJetsInBarrel', trigger2, len(leadingJetPt_array) - 1, array('f', leadingJetPt_array))
	hist1_twoJetsInEndcap = ROOT.TH1F('hist1_twoJetsInEndcap', trigger1, len(leadingJetPt_array) - 1, array('f', leadingJetPt_array))
	hist2_twoJetsInEndcap = ROOT.TH1F('hist2_twoJetsInEndcap', trigger2, len(leadingJetPt_array) - 1, array('f', leadingJetPt_array))
	hist1_oneJetInBarrel_oneJetInEndcap = ROOT.TH1F('hist1_oneJetInBarrel_oneJetInEndcap', trigger1, len(leadingJetPt_array) - 1, array('f', leadingJetPt_array))
	hist2_oneJetInBarrel_oneJetInEndcap = ROOT.TH1F('hist2_oneJetInBarrel_oneJetInEndcap', trigger2, len(leadingJetPt_array) - 1, array('f', leadingJetPt_array))

	cuts1 = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && mjj > ' + str(mjjCut) + ' && jet_pt[0] > ' + str(leadingJetPtCut) + ' && jet_pt[1] > ' + str(trailingJetPtCut) + ' && ' + trigger1 + ' == 1' 

	cuts2 = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && mjj > ' + str(mjjCut) + ' && jet_pt[0] > ' + str(leadingJetPtCut) + ' && jet_pt[1] > ' + str(trailingJetPtCut) + ' && ' + trigger2 + ' == 1' 

	fin.cd()

	#####################
	#ETA RANGES SHOULD BE CHECKED!
	#####################

	fin.eventTree.Draw('jet_pt[0]>>hist1_twoJetsInBarrel', cuts1 + ' && abs(jet_eta[0]) < 1.479 && abs(jet_eta[1]) < 1.479', '') 
	fin.eventTree.Draw('jet_pt[0]>>hist2_twoJetsInBarrel', cuts2 + ' && abs(jet_eta[0]) < 1.479 && abs(jet_eta[1]) < 1.479', '')
	
	fin.eventTree.Draw('jet_pt[0]>>hist1_twoJetsInEndcap', cuts1 + ' && abs(jet_eta[0]) > 1.479 && abs(jet_eta[1]) > 1.479', '')
	fin.eventTree.Draw('jet_pt[0]>>hist2_twoJetsInEndcap', cuts2 + ' && abs(jet_eta[0]) > 1.479 && abs(jet_eta[1]) > 1.479', '')

	fin.eventTree.Draw('jet_pt[0]>>hist1_oneJetInBarrel_oneJetInEndcap', cuts1 + ' && ((abs(jet_eta[0]) > 1.479 && abs(jet_eta[1]) < 1.479) || (abs(jet_eta[0]) < 1.479 && abs(jet_eta[1]) > 1.479))', '')
	fin.eventTree.Draw('jet_pt[0]>>hist2_oneJetInBarrel_oneJetInEndcap', cuts2 + ' && ((abs(jet_eta[0]) > 1.479 && abs(jet_eta[1]) < 1.479) || (abs(jet_eta[0]) < 1.479 && abs(jet_eta[1]) > 1.479))', '')
	
	#Construct histograms for all cases 
	
	drawCompGraph(hist1_twoJetsInBarrel, hist2_twoJetsInBarrel, label1, label2, 'leadingJetPt', 'twoJetsInBarrel', cuts)

	drawCompGraph(hist1_twoJetsInEndcap, hist2_twoJetsInEndcap, label1, label2, 'leadingJetPt', 'twoJetsInEndcap', cuts)

	drawCompGraph(hist1_oneJetInBarrel_oneJetInEndcap, hist2_oneJetInBarrel_oneJetInEndcap, label1, label2, 'leadingJetPt', 'oneJetInBarrel_oneJetInEndcap', cuts)

	fin.Close()

###########################

def drawCompGraph_MET(dataFile, trigger1, trigger2, label1, label2, cuts):

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

	fin.Close()






