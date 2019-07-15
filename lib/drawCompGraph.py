import ROOT
import numpy as np
import os
from array import array

def drawCompGraph(histo1, histo2, label1, label2, variable, case, cuts):

	'''
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

	mjjCut = cuts[0]
	leadingJetPtCut = cuts[1]
	trailingJetPtCut = cuts[2]

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
		
		dirName = 'pngImages/triggerCompPlots/MET_plots/twoJetsInBarrel'

	elif case == 'twoJetsInEndcap':

		dirName = 'pngImages/triggerCompPlots/MET_plots/twoJetsInEndcap'

	elif case == 'oneJetInBarrel_oneJetInEndcap':

		dirName = 'pngImages/triggerCompPlots/MET_plots/oneJetInBarrel_oneJetInEndcap'

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

	mjj_array = np.arange(700., 1200., 25.)  

	fin = ROOT.TFile(dataFile)

	#Get the relevant cuts
	mjjCut, leadingJetPtCut, trailingJetPtCut = cuts[0], cuts[1], cuts[2]

	hist1 = ROOT.TH1F('hist1', trigger1, len(mjj_array) - 1, array('f', mjj_array))
	hist2 = ROOT.TH1F('hist2', trigger2, len(mjj_array) - 1, array('f', mjj_array))

	cuts1 = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && mjj > ' + str(mjjCut) + ' && jet_pt[0] > ' + str(leadingJetPtCut) + ' && jet_pt[1] > ' + str(trailingJetPtCut) + ' && ' + trigger1 + ' == 1' 

	cuts2 = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && mjj > ' + str(mjjCut) + ' && jet_pt[0] > ' + str(leadingJetPtCut) + ' && jet_pt[1] > ' + str(trailingJetPtCut) + ' && ' + trigger2 + ' == 1' 

	fin.cd()

	fin.eventTree.Draw('mjj>>hist1', cuts1, '')
	fin.eventTree.Draw('mjj>>hist2', cuts2, '')
	
	hist1.SetLineColor(ROOT.kBlack)
	hist1.SetLineWidth(2)
	
	hist2.SetLineColor(ROOT.kRed)
	hist2.SetLineWidth(2)

	legend = ROOT.TLegend(0.6, 0.6, 0.85, 0.85)
	legend.SetBorderSize(0)
	
	legend.AddEntry(hist1, label1, 'l')
	legend.AddEntry(hist2, label2, 'l')

	canv = ROOT.TCanvas('canv', 'canv')

	if hist2.GetMaximum() > hist1.GetMaximum():
		
		hist2.GetXaxis().SetTitle('M_{jj} (GeV)')
		hist2.GetYaxis().SetTitle('Number of Events')
		hist2.SetTitle('')
		
		hist2.Draw()
		hist1.Draw('same')

	else:

		hist1.GetXaxis().SetTitle('M_{jj} (GeV)')
		hist1.GetYaxis().SetTitle('Number of Events')
		hist1.SetTitle('')

		hist1.Draw()
		hist2.Draw('same')

	legend.Draw('same')
	
	filename = label1 + '_' + label2 + '_mjj_' + str(mjjCut) + '_' + str(leadingJetPtCut) + '_' + str(trailingJetPtCut) + '.png'
	dirName = 'pngImages/triggerCompPlots/mjj_plots'

	if not os.path.isdir(dirName):

		os.makedirs(dirName)

	filePath = os.path.join(dirName, filename)

	canv.Print(filePath)

	print('Mjj comparison plot saved')
	print('Filename: {}\n'.format(filePath))

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

	trailingJetPt_array = np.arange(40., 120., 5.)  

	fin = ROOT.TFile(dataFile)

	#Get the relevant cuts
	mjjCut, leadingJetPtCut, trailingJetPtCut = cuts[0], cuts[1], cuts[2]

	hist1 = ROOT.TH1F('hist1', trigger1, len(trailingJetPt_array) - 1, array('f', trailingJetPt_array))
	hist2 = ROOT.TH1F('hist2', trigger2, len(trailingJetPt_array) - 1, array('f', trailingJetPt_array))

	cuts1 = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && mjj > ' + str(mjjCut) + ' && jet_pt[0] > ' + str(leadingJetPtCut) + ' && jet_pt[1] > ' + str(trailingJetPtCut) + ' && ' + trigger1 + ' == 1' 

	cuts2 = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && mjj > ' + str(mjjCut) + ' && jet_pt[0] > ' + str(leadingJetPtCut) + ' && jet_pt[1] > ' + str(trailingJetPtCut) + ' && ' + trigger2 + ' == 1' 

	fin.cd()

	fin.eventTree.Draw('jet_pt[1]>>hist1', cuts1, '')
	fin.eventTree.Draw('jet_pt[1]>>hist2', cuts2, '')
	
	hist1.SetLineColor(ROOT.kBlack)
	hist1.SetLineWidth(2)
	
	hist2.SetLineColor(ROOT.kRed)
	hist2.SetLineWidth(2)

	legend = ROOT.TLegend(0.6, 0.6, 0.85, 0.85)
	legend.SetBorderSize(0)
	
	legend.AddEntry(hist1, label1, 'l')
	legend.AddEntry(hist2, label2, 'l')

	canv = ROOT.TCanvas('canv', 'canv')

	if hist2.GetMaximum() > hist1.GetMaximum():
		
		hist2.GetXaxis().SetTitle('Trailing Jet Pt (GeV)')
		hist2.GetYaxis().SetTitle('Number of Events')
		hist2.SetTitle('')
		
		hist2.Draw()
		hist1.Draw('same')

	else:

		hist1.GetXaxis().SetTitle('Trailing Jet Pt (GeV)')
		hist1.GetYaxis().SetTitle('Number of Events')
		hist1.SetTitle('')

		hist1.Draw()
		hist2.Draw('same')

	legend.Draw('same')
	
	filename = label1 + '_' + label2 + '_trailingJetPt_' + str(mjjCut) + '_' + str(leadingJetPtCut) + '_' + str(trailingJetPtCut) + '.png'
	dirName = 'pngImages/triggerCompPlots/trailingJetPt_plots'

	if not os.path.isdir(dirName):

		os.makedirs(dirName)

	filePath = os.path.join(dirName, filename)

	canv.Print(filePath)

	print('Trailing jet pt comparison plot saved')
	print('Filename: {}\n'.format(filePath))

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

	leadingJetPt_array = np.arange(150., 300., 10.)  

	fin = ROOT.TFile(dataFile)

	#Get the relevant cuts
	mjjCut, leadingJetPtCut, trailingJetPtCut = cuts[0], cuts[1], cuts[2]

	hist1 = ROOT.TH1F('hist1', trigger1, len(leadingJetPt_array) - 1, array('f', leadingJetPt_array))
	hist2 = ROOT.TH1F('hist2', trigger2, len(leadingJetPt_array) - 1, array('f', leadingJetPt_array))

	cuts1 = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && mjj > ' + str(mjjCut) + ' && jet_pt[0] > ' + str(leadingJetPtCut) + ' && jet_pt[1] > ' + str(trailingJetPtCut) + ' && ' + trigger1 + ' == 1' 

	cuts2 = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && mjj > ' + str(mjjCut) + ' && jet_pt[0] > ' + str(leadingJetPtCut) + ' && jet_pt[1] > ' + str(trailingJetPtCut) + ' && ' + trigger2 + ' == 1' 

	fin.cd()

	fin.eventTree.Draw('jet_pt[0]>>hist1', cuts1, '')
	fin.eventTree.Draw('jet_pt[0]>>hist2', cuts2, '')
	
	hist1.SetLineColor(ROOT.kBlack)
	hist1.SetLineWidth(2)
	
	hist2.SetLineColor(ROOT.kRed)
	hist2.SetLineWidth(2)

	legend = ROOT.TLegend(0.6, 0.6, 0.85, 0.85)
	legend.SetBorderSize(0)
	
	legend.AddEntry(hist1, label1, 'l')
	legend.AddEntry(hist2, label2, 'l')

	canv = ROOT.TCanvas('canv', 'canv')

	if hist2.GetMaximum() > hist1.GetMaximum():
		
		hist2.GetXaxis().SetTitle('Leading Jet Pt (GeV)')
		hist2.GetYaxis().SetTitle('Number of Events')
		hist2.SetTitle('')
		
		hist2.Draw()
		hist1.Draw('same')

	else:

		hist1.GetXaxis().SetTitle('Leading Jet Pt (GeV)')
		hist1.GetYaxis().SetTitle('Number of Events')
		hist1.SetTitle('')

		hist1.Draw()
		hist2.Draw('same')

	legend.Draw('same')
	
	filename = label1 + '_' + label2 + '_leadingJetPt_' + str(mjjCut) + '_' + str(leadingJetPtCut) + '_' + str(trailingJetPtCut) + '.png'
	dirName = 'pngImages/triggerCompPlots/leadingJetPt_plots'

	if not os.path.isdir(dirName):

		os.makedirs(dirName)

	filePath = os.path.join(dirName, filename)

	canv.Print(filePath)

	print('Leading jet pt comparison plot saved')
	print('Filename: {}\n'.format(filePath))

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

	fin.eventTree.Draw('met>>hist1_oneJetInBarrel_oneJetInEndcap', cuts1 + ' && (abs(jet_eta[0]) > 1.479 && abs(jet_eta[1]) < 1.479) || (abs(jet_eta[0]) < 1.479 && abs(jet_eta[1]) > 1.479)', '')
	fin.eventTree.Draw('met>>hist2_oneJetInBarrel_oneJetInEndcap', cuts2 + ' && (abs(jet_eta[0]) > 1.479 && abs(jet_eta[1]) < 1.479) || (abs(jet_eta[0]) < 1.479 && abs(jet_eta[1]) > 1.479)', '')

	#Construct histograms for all cases 
	
	drawCompGraph(hist1_twoJetsInBarrel, hist2_twoJetsInBarrel, label1, label2, 'MET', 'twoJetsInBarrel', cuts)

	drawCompGraph(hist1_twoJetsInEndcap, hist2_twoJetsInEndcap, label1, label2, 'MET', 'twoJetsInEndcap', cuts)

	drawCompGraph(hist1_oneJetInBarrel_oneJetInEndcap, hist2_oneJetInBarrel_oneJetInEndcap, label1, label2, 'MET', 'oneJetInBarrel_oneJetInEndcap', cuts)

	fin.Close()






