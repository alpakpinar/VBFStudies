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

	met_array = np.arange(100., 500., 25.)  

	fin = ROOT.TFile(dataFile)

	#Get the relevant cuts
	mjjCut, leadingJetPtCut, trailingJetPtCut = cuts[0], cuts[1], cuts[2]

	hist1 = ROOT.TH1F('hist1', trigger1, len(met_array) - 1, array('f', met_array))
	hist2 = ROOT.TH1F('hist2', trigger2, len(met_array) - 1, array('f', met_array))

	cuts1 = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && mjj > ' + str(mjjCut) + ' && jet_pt[0] > ' + str(leadingJetPtCut) + ' && jet_pt[1] > ' + str(trailingJetPtCut) + ' && ' + trigger1 + ' == 1' 

	cuts2 = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && absEtaDiff_leadingTwoJets > 2.5 && mjj > ' + str(mjjCut) + ' && jet_pt[0] > ' + str(leadingJetPtCut) + ' && jet_pt[1] > ' + str(trailingJetPtCut) + ' && ' + trigger2 + ' == 1' 

	fin.cd()

	fin.eventTree.Draw('met>>hist1', cuts1, '')
	fin.eventTree.Draw('met>>hist2', cuts2, '')
	
	hist1.SetLineColor(ROOT.kBlack)
	hist1.SetLineWidth(2)
	
	hist2.SetLineColor(ROOT.kRed)
	hist2.SetLineWidth(2)
	hist2.GetXaxis().SetTitle('MET (GeV)')
	hist2.GetYaxis().SetTitle('Number of Events')

	hist2.SetTitle('')

	legend = ROOT.TLegend(0.6, 0.6, 0.85, 0.85)
	legend.SetBorderSize(0)
	
	legend.AddEntry(hist1, label1, 'l')
	legend.AddEntry(hist2, label2, 'l')

	canv = ROOT.TCanvas('canv', 'canv')

	hist2.Draw()
	hist1.Draw('same')
	legend.Draw('same')
	
	filename = label1 + '_' + label2 + '_MET_' + str(mjjCut) + '_' + str(leadingJetPtCut) + '_' + str(trailingJetPtCut) + '.png'
	dirName = 'pngImages/triggerCompPlots/MET_plots'

	if not os.path.isdir(dirName):

		os.makedirs(dirName)

	filePath = os.path.join(dirName, filename)

	canv.Print(filePath)

	print('MET comparison plot saved')
	print('Filename: {}\n'.format(filePath))
	
	fin.Close()
