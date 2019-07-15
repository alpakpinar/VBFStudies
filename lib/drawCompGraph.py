import ROOT
import numpy as np
import os
from array import array

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

	#####################
	#Construct histograms for the case where two jets are in barrel
	#####################

	hist1_twoJetsInBarrel.SetLineColor(ROOT.kBlack)
	hist1_twoJetsInBarrel.SetLineWidth(2)
	
	hist2_twoJetsInBarrel.SetLineColor(ROOT.kRed)
	hist2_twoJetsInBarrel.SetLineWidth(2)

	legend1 = ROOT.TLegend(0.6, 0.6, 0.85, 0.85)
	legend1.SetBorderSize(0)
	
	legend1.AddEntry(hist1_twoJetsInBarrel, label1, 'l')
	legend1.AddEntry(hist2_twoJetsInBarrel, label2, 'l')

	canv1 = ROOT.TCanvas('canv1', 'canv1')

	if hist2_twoJetsInBarrel.GetMaximum() > hist1_twoJetsInBarrel.GetMaximum():
		
		hist2_twoJetsInBarrel.GetXaxis().SetTitle('MET (GeV)')
		hist2_twoJetsInBarrel.GetYaxis().SetTitle('Number of Events')

		hist2_twoJetsInBarrel.SetTitle('')

		hist2_twoJetsInBarrel.Draw()
		hist1_twoJetsInBarrel.Draw('same')
	
	else:
	
		hist1_twoJetsInBarrel.GetXaxis().SetTitle('MET (GeV)')
		hist1_twoJetsInBarrel.GetYaxis().SetTitle('Number of Events')

		hist1_twoJetsInBarrel.SetTitle('')

		hist1_twoJetsInBarrel.Draw()
		hist2_twoJetsInBarrel.Draw('same')

	legend1.Draw('same')
	
	filename = label1 + '_' + label2 + '_MET_' + str(mjjCut) + '_' + str(leadingJetPtCut) + '_' + str(trailingJetPtCut) + '.png'
	dirName = 'pngImages/triggerCompPlots/MET_plots/twoJetsInBarrel'

	if not os.path.isdir(dirName):

		os.makedirs(dirName)

	filePath = os.path.join(dirName, filename)

	canv1.Print(filePath)

	print('MET comparison plot saved')
	print('Filename: {}\n'.format(filePath))

	#####################
	#Construct histograms for the case where two jets are in endcap
	#####################

	hist1_twoJetsInEndcap.SetLineColor(ROOT.kBlack)
	hist1_twoJetsInEndcap.SetLineWidth(2)

	hist2_twoJetsInEndcap.SetLineColor(ROOT.kRed)
	hist2_twoJetsInEndcap.SetLineWidth(2)

	legend2 = ROOT.TLegend(0.6, 0.6, 0.85, 0.85)
	legend2.SetBorderSize(0)
	
	legend2.AddEntry(hist1_twoJetsInEndcap, label1, 'l')
	legend2.AddEntry(hist2_twoJetsInEndcap, label2, 'l')

	canv2 = ROOT.TCanvas('canv2', 'canv2')
	
	if hist2_twoJetsInEndcap.GetMaximum() > hist1_twoJetsInEndcap.GetMaximum():
		
		hist2_twoJetsInEndcap.GetXaxis().SetTitle('MET (GeV)')
		hist2_twoJetsInEndcap.GetYaxis().SetTitle('Number of Events')

		hist2_twoJetsInEndcap.SetTitle('')

		hist2_twoJetsInEndcap.Draw()
		hist1_twoJetsInEndcap.Draw('same')
	
	else:
	
		hist1_twoJetsInEndcap.GetXaxis().SetTitle('MET (GeV)')
		hist1_twoJetsInEndcap.GetYaxis().SetTitle('Number of Events')

		hist1_twoJetsInEndcap.SetTitle('')

		hist1_twoJetsInEndcap.Draw()
		hist2_twoJetsInEndcap.Draw('same')

	legend2.Draw('same')

	filename = label1 + '_' + label2 + '_MET_' + str(mjjCut) + '_' + str(leadingJetPtCut) + '_' + str(trailingJetPtCut) + '.png'
	dirName = 'pngImages/triggerCompPlots/MET_plots/twoJetsInEndcap'

	if not os.path.isdir(dirName):

		os.makedirs(dirName)

	filePath = os.path.join(dirName, filename)

	canv2.Print(filePath)

	print('MET comparison plot saved')
	print('Filename: {}\n'.format(filePath))

	#####################
	#Construct histograms for the case where one jet is in endcap and the other in barrel
	#####################

	hist1_oneJetInBarrel_oneJetInEndcap.SetLineColor(ROOT.kBlack)
	hist1_oneJetInBarrel_oneJetInEndcap.SetLineWidth(2)

	hist2_oneJetInBarrel_oneJetInEndcap.SetLineColor(ROOT.kRed)
	hist2_oneJetInBarrel_oneJetInEndcap.SetLineWidth(2)

	legend3 = ROOT.TLegend(0.6, 0.6, 0.85, 0.85)
	legend3.SetBorderSize(0)
	
	legend3.AddEntry(hist1_oneJetInBarrel_oneJetInEndcap, label1, 'l')
	legend3.AddEntry(hist2_oneJetInBarrel_oneJetInEndcap, label2, 'l')

	canv3 = ROOT.TCanvas('canv3', 'canv3')
	
	if hist2_oneJetInBarrel_oneJetInEndcap.GetMaximum() > hist1_oneJetInBarrel_oneJetInEndcap.GetMaximum():
		
		hist2_oneJetInBarrel_oneJetInEndcap.GetXaxis().SetTitle('MET (GeV)')
		hist2_oneJetInBarrel_oneJetInEndcap.GetYaxis().SetTitle('Number of Events')

		hist2_oneJetInBarrel_oneJetInEndcap.SetTitle('')

		hist2_oneJetInBarrel_oneJetInEndcap.Draw()
		hist1_oneJetInBarrel_oneJetInEndcap.Draw('same')
	
	else:
	
		hist1_oneJetInBarrel_oneJetInEndcap.GetXaxis().SetTitle('MET (GeV)')
		hist1_oneJetInBarrel_oneJetInEndcap.GetYaxis().SetTitle('Number of Events')

		hist1_oneJetInBarrel_oneJetInEndcap.SetTitle('')

		hist1_oneJetInBarrel_oneJetInEndcap.Draw()
		hist2_oneJetInBarrel_oneJetInEndcap.Draw('same')

	legend3.Draw('same')

	filename = label1 + '_' + label2 + '_MET_' + str(mjjCut) + '_' + str(leadingJetPtCut) + '_' + str(trailingJetPtCut) + '.png'
	dirName = 'pngImages/triggerCompPlots/MET_plots/oneJetInBarrel_oneJetInEndcap'

	if not os.path.isdir(dirName):

		os.makedirs(dirName)

	filePath = os.path.join(dirName, filename)

	canv3.Print(filePath)

	print('MET comparison plot saved')
	print('Filename: {}\n'.format(filePath))

	fin.Close()






