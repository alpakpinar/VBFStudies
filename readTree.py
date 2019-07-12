from __future__ import division
import ROOT
import argparse
from math import sqrt
from array import array

from lib.histos import declareHistos
from lib.selections import *

def getFileType():

	parser = argparse.ArgumentParser()
	parser.add_argument('-y', '--year', help = 'The production year for MiniAOD file (2017 or 2018)', type = int)
	parser.add_argument('-t', '--test', help = 'Run over the test file', action = 'store_true')
	parser.add_argument('-s', '--shortTest', help = 'Run over the short test file', action = 'store_true')
	parser.add_argument('-c', '--clean', help = 'Clean the ROOT file by deleting all previous histograms', action = 'store_true')
	parser.add_argument('-n', '--noWrite', help = 'Do not write the efficiency graphs and histograms to the ROOT file', action = 'store_true')
	args = parser.parse_args()

	return args

def deleteHistos(histo):

	'''
	Removes the first 30 versions of the given histogram.
	Called only if -c option is specified while running the script.
	'''
	for i in range(30):

		hist = histo + ';' + str(i+1)
		ROOT.gDirectory.Delete(hist)	
 
def cleanROOTFile(inputFile, histos):
	
	'''
	Removes the first 30 versions of the histograms from the ROOT file.
	Called only if -c option is specified while running the script.
	'''
	print('Cleaning the ROOT file')

	f = ROOT.TFile.Open(inputFile, 'UPDATE')

	for histo in histos.keys():

		for i in range(30):
			
			hist = histo + ';' + str(i+1)
			ROOT.gDirectory.Delete(hist)	
	
	f.Close()
	
	print('Cleaning done')

def deltaR(prt1, prt2):
	
	eta1, eta2 = prt1.eta, prt2.eta
	phi1, phi2 = prt1.phi, prt2.phi
	eta_diff = eta1 - eta2
	phi_diff = phi1 - phi2
	
	return sqrt((eta_diff)**2 + (phi_diff)**2) 

###########################

def drawTriggerEff_MET(inputFile, trigger, args):

	'''
	Constructs the trigger efficiency graph for a given trigger, as a function of MET.
	Returns the MET histogram wih VBF cuts + trigger and efficiency plot.
	'''

	f = ROOT.TFile.Open(inputFile, 'UPDATE')

	met_array = array('f', [200., 220., 240., 270., 300., 340., 380., 420., 500.]) 

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

	vbfCuts = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && met > 200 && jet_pt[0] > 80 && jet_pt[1] > 40 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && mjj > 500 && absEtaDiff_leadingTwoJets > 2.5'

	#vbfCuts = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && met > 200 && jet_pt[0] > 80 && jet_pt[1] > 40 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && mjj > 500 && absEtaDiff_leadingTwoJets > 2.5 && Flag_BadPFMuonFilter == 1 && Flag_goodVertices == 1 && Flag_globalSuperTightHalo2016Filter == 1 && Flag_HBHENoiseFilter == 1 && Flag_HBHENoiseIsoFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1'

	vbfAndTriggerCuts = vbfCuts + ' && ' + trigger + ' == 1'

	f.eventTree.Draw('met>>met_hist')
	f.eventTree.Draw('met>>met_hist_afterVBFCuts', vbfCuts, '')
	f.eventTree.Draw('met>>met_hist_afterVBFCutsAndTrigger', vbfAndTriggerCuts, '')
	
	print('Events passing VBF cuts: {}'.format(f.eventTree.GetEntries(vbfCuts)))
	print('Events passing VBF cuts + {}: {}'.format(trigger, f.eventTree.GetEntries(vbfAndTriggerCuts)))
	
	#Go to the directory for trigger efficiencies 
	
	try: f.GetKey('triggerEff_MET').IsFolder()

	except ReferenceError:

		f.mkdir('triggerEff_MET', 'triggerEff_MET') 

	f.cd('triggerEff_MET')
	
	#Check if the two histograms are consistent

	if ROOT.TEfficiency.CheckConsistency(met_hist_afterVBFCutsAndTrigger, met_hist_afterVBFCuts):

		eff_graph_MET = ROOT.TEfficiency(met_hist_afterVBFCutsAndTrigger, met_hist_afterVBFCuts)
		
		eff_graph_MET.SetTitle(trigger + ';MET (GeV);eff')

		eff_graph_MET.Write('eff_graph_' + trigger + '_MET')

		print('Efficiency graph for ' + trigger + ' with respect to MET is constructed!')

	f.cd()
	
	try: f.GetKey('metHistos').IsFolder()

	except ReferenceError: 

		f.mkdir('metHistos', 'metHistos') 
	
	f.cd('metHistos')

	if not args.noWrite:

		met_hist.Write('met_hist')
		met_hist_afterVBFCuts.Write('met_hist_afterVBFCuts')
		met_hist_afterVBFCutsAndTrigger.Write('met_hist_afterVBFCutsAndTrigger_' + trigger)
	
	met_hist.SetDirectory(0)
	met_hist_afterVBFCuts.SetDirectory(0)
	met_hist_afterVBFCutsAndTrigger.SetDirectory(0)
	
	f.cd()

	f.Close()

	return met_hist_afterVBFCutsAndTrigger, eff_graph_MET

def drawTriggerEff_mjj(inputFile, trigger, args):

	'''
	Constructs the trigger efficiency graph for a given trigger, as a function of invariant mass of two leading jets, mjj.
	Returns the mjj histogram wih VBF cuts + trigger and efficiency plot.
	'''

	f = ROOT.TFile.Open(inputFile, 'UPDATE')

	mjj_array = array('f', [500., 520., 540., 570., 600., 640., 680., 730., 790., 880., 1000.]) 

	mjj_hist = ROOT.TH1F('mjj_hist', 'mjj_hist', len(mjj_array)-1, mjj_array)

	mjj_hist_afterVBFCuts = ROOT.TH1F('mjj_hist_afterVBFCuts', 'mjj_hist_afterVBFCuts', len(mjj_array)-1, mjj_array)	
	mjj_hist_afterVBFCuts.SetLineColor(ROOT.kRed)
	
	mjj_hist_afterVBFCutsAndTrigger = ROOT.TH1F('mjj_hist_afterVBFCutsAndTrigger', 'mjj_hist_afterVBFCutsAndTrigger', len(mjj_array)-1, mjj_array)
	mjj_hist_afterVBFCutsAndTrigger.SetLineColor(ROOT.kBlack)

	vbfCuts = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && met > 200 && jet_pt[0] > 80 && jet_pt[1] > 40 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && mjj > 500 && absEtaDiff_leadingTwoJets > 2.5'

	#vbfCuts = 'containsPhoton == 0 && containsLepton == 0 && contains_bJet == 0 && met > 200 && jet_pt[0] > 80 && jet_pt[1] > 40 && minPhi_jetMET > 0.5 && jet_eta[0]*jet_eta[1]<0 && mjj > 500 && absEtaDiff_leadingTwoJets > 2.5 && Flag_BadPFMuonFilter == 1 && Flag_goodVertices == 1 && Flag_globalSuperTightHalo2016Filter == 1 && Flag_HBHENoiseFilter == 1 && Flag_HBHENoiseIsoFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1'

	vbfAndTriggerCuts = vbfCuts + ' && ' + trigger + ' == 1'

	f.eventTree.Draw('mjj>>mjj_hist')
	f.eventTree.Draw('mjj>>mjj_hist_afterVBFCuts', vbfCuts, '')
	f.eventTree.Draw('mjj>>mjj_hist_afterVBFCutsAndTrigger', vbfAndTriggerCuts, '')

	####
	print('Events passing VBF cuts: {}'.format(f.eventTree.GetEntries(vbfCuts)))
	print('Events passing VBF cuts + {}: {}'.format(trigger, f.eventTree.GetEntries(vbfAndTriggerCuts)))
	####	
	
	#Go to the directory for trigger efficiencies 
	
	try: f.GetKey('triggerEff_mjj').IsFolder()

	except ReferenceError: 

		f.mkdir('triggerEff_mjj', 'triggerEff_mjj') 

	f.cd('triggerEff_mjj')

	#Check if the two histograms are consistent

	if ROOT.TEfficiency.CheckConsistency(mjj_hist_afterVBFCutsAndTrigger, mjj_hist_afterVBFCuts):

		eff_graph_mjj = ROOT.TEfficiency(mjj_hist_afterVBFCutsAndTrigger, mjj_hist_afterVBFCuts)

		eff_graph_mjj.SetTitle(trigger + ';mjj (GeV);eff')

		eff_graph_mjj.Write('eff_graph_' + trigger + '_mjj')

		print('Efficiency graph for ' + trigger + ' with respect to mjj is constructed!')
	
	f.cd()
	
	try: f.GetKey('mjjHistos').IsFolder()

	except ReferenceError: 

		f.mkdir('mjjHistos', 'mjjHistos') 
	
	f.cd('mjjHistos')

	if not args.noWrite:
	
		mjj_hist.Write('mjj_hist')
		mjj_hist_afterVBFCuts.Write('mjj_hist_afterVBFCuts')
		mjj_hist_afterVBFCutsAndTrigger.Write('mjj_hist_afterVBFCutsAndTrigger_' + trigger)
	
	mjj_hist.SetDirectory(0)
	mjj_hist_afterVBFCuts.SetDirectory(0)
	mjj_hist_afterVBFCutsAndTrigger.SetDirectory(0)

	f.cd()
		
	f.Close()

	return mjj_hist_afterVBFCutsAndTrigger, eff_graph_mjj

#############################

def drawCompGraph_MET(trigger1, trigger2, label1, label2,  met_hist_withTriggers):

	'''
	Draws the VBF cuts + trigger acceptance graph for two triggers, as a function of MET.
	'''

	ROOT.gStyle.SetOptStat(0)

	hist1 = met_hist_withTriggers[trigger1]	
	hist1.SetLineColor(ROOT.kBlack)
	hist1.SetLineWidth(2)
	
	hist2 = met_hist_withTriggers[trigger2]	
	hist2.SetLineColor(ROOT.kRed)
	hist2.SetLineWidth(2)
	hist2.GetXaxis().SetTitle('MET (GeV)')
	hist2.GetYaxis().SetTitle('Number of Events')

	legend = ROOT.TLegend(0.6, 0.6, 0.85, 0.85)
	legend.SetBorderSize(0)
	
	legend.AddEntry(hist1, label1, 'l')
	legend.AddEntry(hist2, label2, 'l')

	canv = ROOT.TCanvas('canv', 'canv')

	hist2.Draw()
	hist1.Draw('same')
	legend.Draw('same')

	filename = label1 + '_' + label2 + '_MET.png'
	canv.Print(filename)

##########################
#TO BE TESTED
##########################

def drawCutFlow(inputFile):

	'''
	Draws the cut flow diagram for VBF cuts, given an input tree.
	'''

	f = ROOT.TFile.Open(inputFile, 'UPDATE')
	tree = f.eventTree

	labels, eventCounts = applyVBFSelections(tree)	

	canv = ROOT.TCanvas('canv', 'canv', 800, 600)
	canv.SetGrid()

	cutFlowGraph = ROOT.TGraph(len(eventCounts))

	cutFlowGraph.SetNameTitle('evtCounts', 'Event Counts After Each VBF Cut')

	x_ax = cutFlowGraph.GetXaxis()

	x_ax.Set(len(eventCounts), 0, len(eventCounts))

	for i in range(len(eventCounts)):
		
		x_ax.SetBinLabel(i+1, labels[i]) #Labeling the x-axis

		cutFlowGraph.SetPoint(i, i, eventCounts[i]*100/eventCounts[0]) #Filling the graph with percentage of events passing through each cut
		print(x_ax.GetBinLabel(i+1))

	print(x_ax.GetXmax())

	x_ax.LabelsOption("v")
	x_ax.SetTitle('Cuts')
	x_ax.SetTitleOffset(1.4)
	x_ax.SetLabelSize(0.03)
	
	cutFlowGraph.GetYaxis().SetTitle('% Events Passing')

	cutFlowGraph.SetMarkerStyle(20)

	cutFlowGraph.Draw("AP")
	
	canv.Print('VBF_CutFlowDiagram2017.png')

	f.Close()
	
############################
#TO BE TESTED
############################

def readTree(inputFile):

	f = ROOT.TFile.Open(inputFile, 'UPDATE')
	
	event_count_before = 0
	event_count_afterL1 = 0
	event_count_afterL1HLT = 0
	event_count_afterVBF = 0
	event_count_afterALL = 0

	for event in f.eventTree:
		
		event_count_before += 1
		
		# Reading the branches of eventTree		
		nJet = event.nJet		
		jet_pt = event.jet_pt
		jet_eta = event.jet_eta
		jet_energy = event.jet_energy
		jet_phi = event.jet_phi
		jet_px = event.jet_px
		jet_py = event.jet_py
		jet_pz = event.jet_pz

		histos['nJets_hist'].Fill(nJet)
		histos['leadingJetPt_hist'].Fill(jet_pt[0])
		histos['trailingJetPt_hist'].Fill(jet_pt[1])

		if nJet > 1:
		
			totalEnergy = jet_energy[0] + jet_energy[1]
			totalPx = jet_px[0] + jet_px[1]			
			totalPy = jet_py[0] + jet_py[1]			
			totalPz = jet_pz[0] + jet_pz[1]			
			
			mjj = sqrt(totalEnergy**2 - totalPx**2 - totalPy**2 - totalPz**2) #Invariant mass of two leading jets

			histos['mjj_hist'].Fill(mjj)

		nElectron = event.nElectron
		electron_pt = event.electron_pt
		electron_phi = event.electron_phi
		electron_eta = event.electron_eta

		nMuon = event.nMuon
		muon_pt = event.muon_pt
		muon_phi = event.muon_phi
		muon_eta = event.muon_eta
		
		nTau = event.nTau
		tau_pt = event.tau_pt
		tau_phi = event.tau_phi
		tau_eta = event.tau_eta

		nParticles = event.nParticles
		pdgId = event.pdgId

		if applyL1Selection(event): #L1 selection only

			event_count_afterL1 += 1
		
		if applyHLTSelection(event, 'HLT_DiJet110_35_Mjj650_PFMET110_v2'): #L1 + HLT selection
			
			event_count_afterL1HLT += 1
		
		if applyVBFSelections(event): #VBF selections only
	
			event_count_afterVBF += 1
	
		if applyAllSelections(event, 'HLT_DiJet110_35_Mjj650_PFMET110_v2'):
			
			event_count_afterALL += 1

	histos['nJets_hist'].Write('nJets_hist')
	histos['mjj_hist'].Write('mjj_hist')
	histos['leadingJetPt_hist'].Write('leadingJetPt_hist')
	histos['trailingJetPt_hist'].Write('trailingJetPt_hist')

	f.Close()

	print('\n')			
	print('*******************')
	print('Event Yield Results')
	print('*******************\n')
	print('Total number of events read                              : {0:6d}'.format(event_count_before))
	print('Total number of events passed L1 seed                    : {0:6d}        Passing Ratio: {1:6.2f}%'.format(event_count_afterL1, event_count_afterL1*100/event_count_before))
	print('Total number of events passed L1 seed + HLT              : {0:6d}        Passing Ratio: {1:6.2f}%'.format(event_count_afterL1HLT, event_count_afterL1HLT*100/event_count_before))
	print('Total number of events passed VBF selections             : {0:6d}        Passing Ratio: {1:6.2f}%'.format(event_count_afterVBF, event_count_afterVBF*100/event_count_before)) 
	print('Total number of events passed L1 + HLT + VBF selections  : {0:6d}        Passing Ratio: {1:6.2f}%\n'.format(event_count_afterALL, event_count_afterALL*100/event_count_before)) 
	print('Job finished')


if __name__ == '__main__':

	file_type = getFileType()
	
	if file_type.test:

		inputFile = 'inputs/VBF_HToInv_' + str(file_type.year) + '_test.root'
		print('Starting job')
		print('File: {}'.format(inputFile))

	elif file_type.shortTest:
		
		inputFile = 'inputs/VBF_HToInv_' + str(file_type.year) + '_shortTest.root'
		print('Starting job')
		print('File: {}'.format(inputFile))
	
	else:
 
		inputFile = 'inputs/VBF_HToInv_' + str(file_type.year) + '.root'
		print('Starting job')
		print('File: {}'.format(inputFile))
	
	#Define the histograms

	histos = declareHistos()

	#Clean the ROOT file if needed

	if file_type.clean:

		cleanROOTFile(inputFile, histos)

	#inputFile = 'inputs/VBF_HToInv_2017_test.root'

	#readTree(inputFile) 

	triggers = ['HLT_DiJet110_35_Mjj650_PFMET110_v5', 'HLT_DiJet110_35_Mjj650_PFMET120_v5', 'HLT_DiJet110_35_Mjj650_PFMET130_v5', 'HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v16', 'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v16', 'HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v15', 'HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v15']

	legendLabels = ['VBF_MET110', 'VBF_MET120', 'VBF_MET130', 'METNoMu110', 'METNoMu120', 'METNoMu130', 'METNoMu140']
	
	eff_graphs_MET = {}
	met_hist_withTriggers = {}	
	
	eff_graphs_mjj = {}
	mjj_hist_withTriggers = {}

	for count, trigger in enumerate(triggers):

		mjj_hist_withTriggers[trigger], eff_graphs_mjj[trigger] = drawTriggerEff_mjj(inputFile, trigger, file_type)

		met_hist_withTriggers[trigger], eff_graphs_MET[trigger] = drawTriggerEff_MET(inputFile, trigger, file_type)

	#drawCompGraph_MET(triggers[0], triggers[3], legendLabels[0], legendLabels[3], met_hist_withTriggers)

	#drawCutFlow(inputFile)
