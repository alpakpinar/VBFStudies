from __future__ import division
import ROOT
import os
import argparse
import numpy as np
from math import sqrt
from array import array

from lib.histos import declareHistos
from lib.selections import *
from lib.drawTriggerEff import *
from lib.drawCompGraph import *

def getArgs():

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
    Removes the first 30 versions of the given histograms from the ROOT file.
    Called only if -c option is specified while running the script.
    '''
    print('Cleaning the ROOT file')

    f = ROOT.TFile.Open(inputFile, 'UPDATE')

    for histo in histos:

        deleteHistos(histo)

    f.Close()
    
    print('Cleaning done')

def deltaR(prt1, prt2):
    
    eta1, eta2 = prt1.eta, prt2.eta
    phi1, phi2 = prt1.phi, prt2.phi
    eta_diff = eta1 - eta2
    phi_diff = phi1 - phi2
    
    return sqrt((eta_diff)**2 + (phi_diff)**2) 

def drawCutFlow(inputFile):

    '''
    Draws the cut flow diagram for VBF cuts, given an input tree.
    '''

    f = ROOT.TFile.Open(inputFile, 'UPDATE')
    tree = f.eventTree

    labels, eventCounts = applyVBFSelections(tree, cuts, drawHisto=True)    

    canv = ROOT.TCanvas('canv', 'canv', 800, 600)
    canv.SetGrid()

    cutFlowGraph = ROOT.TGraph(len(eventCounts)-1)

    cutFlowGraph.SetNameTitle('evtCounts', 'Event Counts After Each VBF Cut')

    x_ax = cutFlowGraph.GetXaxis()

    x_ax.Set(len(eventCounts)-1, 1, len(eventCounts))

    for i in range(1, len(eventCounts)):
        
        x_ax.SetBinLabel(i, labels[i]) #Labeling the x-axis

        cutFlowGraph.SetPoint(i, i, eventCounts[i]*100/eventCounts[0]) #Filling the graph with percentage of events passing through each cut
        print(x_ax.GetBinLabel(i))

    print(x_ax.GetXmax())

    x_ax.LabelsOption("v")
    x_ax.SetTitle('Cuts')
    x_ax.SetTitleOffset(1.4)
    x_ax.SetLabelSize(0.03)
    
    cutFlowGraph.GetYaxis().SetTitle('% Events Passing')

    cutFlowGraph.SetMarkerStyle(20)

    cutFlowGraph.Draw("AP")
    
    canv.Print('VBF_CutFlowDiagram2017.png')

    print('*'*10 + ' RESULTS ' + '*'*10)
    print('Total number of events                                      : {0:>6}'.format(eventCounts[0]))
    print('Number of events after minPhi_jetMET > 0.5 cut              : {0:>6}'.format(eventCounts[1]))
    print('Number of events after jet_eta[0]*jet_eta[1] < 0 cut        : {0:>6}'.format(eventCounts[2]))
    print('Number of events after abs(jet_eta[0]-jet_eta[1]) > 2.5 cut : {0:>6}'.format(eventCounts[3]))
    print('Number of events after b-jet veto                           : {0:>6}'.format(eventCounts[4]))
    print('Number of events after lepton veto                          : {0:>6}'.format(eventCounts[5]))
    print('Number of events after photon veto                          : {0:>6}'.format(eventCounts[6]))
    print('Number of events after mjj > {0} cut                        : {1:>6}'.format(cuts[0], eventCounts[7]))
    print('Number of events after jet_pt[0] > {0} cut                  : {1:>6}'.format(cuts[1], eventCounts[8]))
    print('Number of events after jet_pt[1] > {0:<3} cut                  : {1:>6}'.format(cuts[2], eventCounts[9]))
    print('Number of events after MET > {0} cut                        : {1:>6}'.format(cuts[-1], eventCounts[10]))
    print('*'*29)

    f.Close()
    
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

def drawTriggerEff_mjjRange(inputFile, args, leadingJetPtCuts, trailingJetPtCuts, triggers):

    '''
    Given the leadingJetPtCuts, trailingJetPtCuts and triggers lists, draws and saves trigger efficiency plots for each of the given cuts for the given triggers.
    '''
    
    for leadingJetPtCut in leadingJetPtCuts:

        for trailingJetPtCut in trailingJetPtCuts:

            for trigger in triggers:

                drawTriggerEff_mjj(inputFile, trigger, args, leadingJetPtCut, trailingJetPtCut)    
    


if __name__ == '__main__':

    args = getArgs()
    
    if args.test:

        inputFile = 'inputs/VBF_HToInv_' + str(args.year) + '_test.root'
        print('Starting job')
        print('File: {}'.format(inputFile))

    elif args.shortTest:
        
        inputFile = 'inputs/VBF_HToInv_' + str(args.year) + '_shortTest.root'
        print('Starting job')
        print('File: {}'.format(inputFile))
    
    else:
 
        inputFile = 'inputs/VBF_HToInv_' + str(args.year) + '.root'
        print('Starting job')
        print('File: {}'.format(inputFile))
    
    #Define the histograms

    #histos = declareHistos()

    #inputFile = 'inputs/VBF_HToInv_2017_test.root'

    #readTree(inputFile) 

    triggers = ['HLT_DiJet110_35_Mjj650_PFMET110_v5', 'HLT_DiJet110_35_Mjj650_PFMET120_v5', 'HLT_DiJet110_35_Mjj650_PFMET130_v5', 'HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v16', 'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v16', 'HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v15', 'HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v15']

    histos = []
    
    ##############################
    #Clean the ROOT file if needed
    ##############################

    if args.clean:
        
        for trigger in triggers:

            histos.append('eff_graph_' + trigger + '_MET')
            histos.append('eff_graph_' + trigger + '_mjj')
            histos.append('met_hist_afterVBFCutsAndTrigger_' + trigger)
            histos.append('met_hist_afterVBFCuts')
            histos.append('met_hist')
            histos.append('mjj_hist_afterVBFCutsAndTrigger_' + trigger)
            histos.append('mjj_hist_afterVBFCuts')
            histos.append('mjj_hist')

        cleanROOTFile(inputFile, histos)

    ###############################

    legendLabels = ['VBF_MET110', 'VBF_MET120', 'VBF_MET130', 'METNoMu110', 'METNoMu120', 'METNoMu130', 'METNoMu140']
    
    eff_graphs_MET = {}
    met_hist_withTriggers = {}    
    
    eff_graphs_mjj = {}
    mjj_hist_withTriggers = {}

    eff_graphs_leadingJetPt = {}
    leadingJetPt_hist_withTriggers = {}
    
    eff_graphs_trailingJetPt = {}
    trailingJetPt_hist_withTriggers = {}
    
    cuts = [1000, 160, 50, 150] #Cuts that will be applied: mjj, leadingJetPt, trailingJetPt, MET

    #for count, trigger in enumerate(triggers):

        #mjj_hist_withTriggers[trigger], eff_graphs_mjj[trigger] = drawTriggerEff_mjj(inputFile, trigger, args, cuts[1], cuts[2])
        
        #leadingJetPt_hist_withTriggers[trigger], eff_graphs_leadingJetPt[trigger] = drawTriggerEff_leadingJetPt(inputFile, trigger, args, cuts[0])

        #trailingJetPt_hist_withTriggers[trigger], eff_graphs_trailingJetPt[trigger] = drawTriggerEff_trailingJetPt(inputFile, trigger, args, cuts[0], cuts[1])
        
        #met_hist_withTriggers[trigger], eff_graphs_MET[trigger] = drawTriggerEff_MET(inputFile, trigger, args, cuts[0], cuts[1], cuts[2])

	#For testing
    #drawTriggerEff_mjj(inputFile, 'HLT_DiJet110_35_Mjj650_PFMET110_v5', args, cuts[1], cuts[2])

    #Draw all the comparison graphs 

    #for i in range(3):

    #    for j in range(3, 7):

    #        drawCompGraph_MET(inputFile, triggers[i], triggers[j], legendLabels[i], legendLabels[j], cuts)
            #drawCompGraph_leadingJetPt(inputFile, triggers[i], triggers[j], legendLabels[i], legendLabels[j], cuts)
            #drawCompGraph_trailingJetPt(inputFile, triggers[i], triggers[j], legendLabels[i], legendLabels[j], cuts)
            #drawCompGraph_mjj(inputFile, triggers[i], triggers[j], legendLabels[i], legendLabels[j], cuts)

    #drawCompGraph_MET(inputFile, triggers[0], triggers[3], legendLabels[0], legendLabels[3], cuts)
    #drawCompGraph_leadingJetPt(inputFile, triggers[0], triggers[3], legendLabels[0], legendLabels[3], cuts)
    #drawCompGraph_trailingJetPt(inputFile, triggers[0], triggers[3], legendLabels[0], legendLabels[3], cuts)
    #drawCompGraph_mjj(inputFile, triggers[0], triggers[3], legendLabels[0], legendLabels[3], cuts)

    #drawCutFlow(inputFile)
