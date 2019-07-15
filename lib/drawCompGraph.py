import ROOT
import numpy as np
import os
from array import array

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

	outputDir = 'output/triggerComparisons'

	#fileName = label1 + '_' + label2 + '.root' 

	#outFile = os.path.join(outputDir, fileName) 

	fin = ROOT.TFile(dataFile)

	#fout = ROOT.TFile(outFile, 'RECREATE')
	
	#Get the relevant cuts
	mjjCut, leadingJetPtCut, trailingJetPtCut = cuts[0], cuts[1], cuts[2]

	hist1 = ROOT.TH1F('hist1', trigger1, len(met_array) - 1, array('f', met_array))
	hist2 = ROOT.TH1F('hist2', trigger2, len(met_array) - 1, array('f', met_array))

	#hist1.SetDirectory(0)
	#hist2.SetDirectory(0)

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
	
	filename = label1 + '_' + label2 + '_MET.png'
	dirName = 'pngImages/triggerCompPlots'

	filePath = os.path.join(dirName, filename)

	canv.Print(filePath)

	print('MET comparison plot saved')
	print('Filename: {}\n'.format(filePath))

	#fout.cd()
	
	#hist1.Write('hist1')
	#hist2.Write('hist2')

	#fout.Close()
	fin.Close()
