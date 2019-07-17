import ROOT
import os
from math import sqrt

def applyVBFSelections(tree, cuts, drawHisto=False):

	'''
	Applies VBF selections and tracks the number of events throughout each cut.
	Cuts to be applied must be given in the cuts list.
	Also draws histograms for variables of interest at each cut level and saves them in a ROOT file, if drawHisto option is True.
	Returns the list of labels and event counts at different stages in the cut flow.
	'''
	labels = ['total', 'METCut', 'LeadJetPt', 'TrailJetPt', 'MinPhiJetMET', 'NegEtaProd', 'EtaDiff', 'bJetCut', 'LeptonVeto', 'PhotonVeto', 'mjjCut']

 	eventCounter = [0 for label in labels] 

	mjj_cut = cuts[0]
	leadingJetPt_cut = cuts[1]
	trailingJetPt_cut = cuts[2]
	met_cut = cuts[3]

	out = ROOT.TFile('output/distributions.root', 'RECREATE')

	eventCounter[0] = tree.GetEntries() #Total number of entries

	tree.Draw('met>>met_hist0')
	tree.Draw('mjj>>mjj_hist0')
	tree.Draw('jet_pt[0]>>leadingJetPt_hist0')
	tree.Draw('jet_pt[1]>>trailingJetPt_hist0')
	tree.Draw('nJet>>numJets_hist0')

	#Retrieve the histograms so that Python knows about them
	#met_hist0 = ROOT.gDirectory.Get('met_hist0')
	#mjj_hist0 = ROOT.gDirectory.Get('mjj_hist0')
	#leadingJetPt_hist0 = ROOT.gDirectory.Get('leadingJetPt_hist0')
	#trailingJetPt_hist0 = ROOT.gDirectory.Get('trailingJetPt_hist0')
	#numJets_hist0 = ROOT.gDirectory.Get('numJets_hist0')

	cut = 'minPhi_jetMET > 0.5'
	
	eventCounter[1] = tree.GetEntries(cut)
	tree.Draw('met>>met_hist1', cut, '')
	tree.Draw('mjj>>mjj_hist1', cut, '')
	tree.Draw('jet_pt[0]>>leadingJetPt_hist1', cut, '')
	tree.Draw('jet_pt[1]>>trailingJetPt_hist1', cut, '')
	tree.Draw('nJet>>numJets_hist1', cut, '')	

	#met_hist1 = ROOT.gDirectory.Get('met_hist1')
	#mjj_hist1 = ROOT.gDirectory.Get('mjj_hist1')
	#leadingJetPt_hist1 = ROOT.gDirectory.Get('leadingJetPt_hist1')
	#trailingJetPt_hist1 = ROOT.gDirectory.Get('trailingJetPt_hist1')
	#numJets_hist1 = ROOT.gDirectory.Get('numJets_hist1')
	
	cut += ' && jet_eta[0]*jet_eta[1] < 0'

	eventCounter[2] = tree.GetEntries(cut)
	tree.Draw('met>>met_hist2', cut, '')
	tree.Draw('mjj>>mjj_hist2', cut, '')
	tree.Draw('jet_pt[0]>>leadingJetPt_hist2', cut, '')
	tree.Draw('jet_pt[1]>>trailingJetPt_hist2', cut, '')
	tree.Draw('nJet>>numJets_hist2', cut, '')	
	
	#met_hist2 = ROOT.gDirectory.Get('met_hist2')
	#mjj_hist2 = ROOT.gDirectory.Get('mjj_hist2')
	#leadingJetPt_hist2 = ROOT.gDirectory.Get('leadingJetPt_hist2')
	#trailingJetPt_hist2 = ROOT.gDirectory.Get('trailingJetPt_hist2')
	#numJets_hist2 = ROOT.gDirectory.Get('numJets_hist2')
	
	cut += ' && abs(jet_eta[0] - jet_eta[1]) > 2.5'

	eventCounter[3] = tree.GetEntries(cut)
	tree.Draw('met>>met_hist3', cut, '')
	tree.Draw('mjj>>mjj_hist3', cut, '')
	tree.Draw('jet_pt[0]>>leadingJetPt_hist3', cut, '')
	tree.Draw('jet_pt[1]>>trailingJetPt_hist3', cut, '')
	tree.Draw('nJet>>numJets_hist3', cut, '')	
	
	#met_hist3 = ROOT.gDirectory.Get('met_hist3')
	#mjj_hist3 = ROOT.gDirectory.Get('mjj_hist3')
	#leadingJetPt_hist3 = ROOT.gDirectory.Get('leadingJetPt_hist3')
	#trailingJetPt_hist3 = ROOT.gDirectory.Get('trailingJetPt_hist3')
	#numJets_hist3 = ROOT.gDirectory.Get('numJets_hist3')
	
	cut += ' && contains_bJet == 0'

	eventCounter[4] = tree.GetEntries(cut)
	tree.Draw('met>>met_hist4', cut, '')
	tree.Draw('mjj>>mjj_hist4', cut, '')
	tree.Draw('jet_pt[0]>>leadingJetPt_hist4', cut, '')
	tree.Draw('jet_pt[1]>>trailingJetPt_hist4', cut, '')
	tree.Draw('nJet>>numJets_hist4', cut, '')	

	#met_hist4 = ROOT.gDirectory.Get('met_hist4')
	#mjj_hist4 = ROOT.gDirectory.Get('mjj_hist4')
	#leadingJetPt_hist4 = ROOT.gDirectory.Get('leadingJetPt_hist4')
	#trailingJetPt_hist4 = ROOT.gDirectory.Get('trailingJetPt_hist4')
	#numJets_hist4 = ROOT.gDirectory.Get('numJets_hist4')
	
	cut += ' && containsLepton == 0'
	
	eventCounter[5] = tree.GetEntries(cut)
	tree.Draw('met>>met_hist5', cut, '')
	tree.Draw('mjj>>mjj_hist5', cut, '')
	tree.Draw('jet_pt[0]>>leadingJetPt_hist5', cut, '')
	tree.Draw('jet_pt[1]>>trailingJetPt_hist5', cut, '')
	tree.Draw('nJet>>numJets_hist5', cut, '')	
	
	#met_hist5 = ROOT.gDirectory.Get('met_hist5')
	#mjj_hist5 = ROOT.gDirectory.Get('mjj_hist5')
	#leadingJetPt_hist5 = ROOT.gDirectory.Get('leadingJetPt_hist5')
	#trailingJetPt_hist5 = ROOT.gDirectory.Get('trailingJetPt_hist5')
	#numJets_hist5 = ROOT.gDirectory.Get('numJets_hist5')
	
	cut += ' && containsPhoton == 0'

	eventCounter[6] = tree.GetEntries(cut)
	tree.Draw('met>>met_hist6', cut, '')
	tree.Draw('mjj>>mjj_hist6', cut, '')
	tree.Draw('jet_pt[0]>>leadingJetPt_hist6', cut, '')
	tree.Draw('jet_pt[1]>>trailingJetPt_hist6', cut, '')
	tree.Draw('nJet>>numJets_hist6', cut, '')	
	
	#met_hist6 = ROOT.gDirectory.Get('met_hist6')
	#mjj_hist6 = ROOT.gDirectory.Get('mjj_hist6')
	#leadingJetPt_hist6 = ROOT.gDirectory.Get('leadingJetPt_hist6')
	#trailingJetPt_hist6 = ROOT.gDirectory.Get('trailingJetPt_hist6')
	#numJets_hist6 = ROOT.gDirectory.Get('numJets_hist6')
	
	cut += ' && mjj > ' + str(mjj_cut)
	
	eventCounter[7] = tree.GetEntries(cut)
	tree.Draw('met>>met_hist7', cut, '')
	tree.Draw('mjj>>mjj_hist7', cut, '')
	tree.Draw('jet_pt[0]>>leadingJetPt_hist7', cut, '')
	tree.Draw('jet_pt[1]>>trailingJetPt_hist7', cut, '')
	tree.Draw('nJet>>numJets_hist7', cut, '')	
	
	#met_hist7 = ROOT.gDirectory.Get('met_hist7')
	#mjj_hist7 = ROOT.gDirectory.Get('mjj_hist7')
	#leadingJetPt_hist7 = ROOT.gDirectory.Get('leadingJetPt_hist7')
	#trailingJetPt_hist7 = ROOT.gDirectory.Get('trailingJetPt_hist7')
	#numJets_hist7 = ROOT.gDirectory.Get('numJets_hist7')
	
	cut += ' && jet_pt[0] > ' + str(leadingJetPt_cut)
	
	eventCounter[8] = tree.GetEntries(cut)
	tree.Draw('met>>met_hist8', cut, '')
	tree.Draw('mjj>>mjj_hist8', cut, '')
	tree.Draw('jet_pt[0]>>leadingJetPt_hist8', cut, '')
	tree.Draw('jet_pt[1]>>trailingJetPt_hist8', cut, '')
	tree.Draw('nJet>>numJets_hist8', cut, '')	
	
	#met_hist8 = ROOT.gDirectory.Get('met_hist8')
	#mjj_hist8 = ROOT.gDirectory.Get('mjj_hist8')
	#leadingJetPt_hist8 = ROOT.gDirectory.Get('leadingJetPt_hist8')
	#trailingJetPt_hist8 = ROOT.gDirectory.Get('trailingJetPt_hist8')
	#numJets_hist8 = ROOT.gDirectory.Get('numJets_hist8')
	
	cut += ' && jet_pt[1] > ' + str(trailingJetPt_cut)
	
	eventCounter[9] = tree.GetEntries(cut)
	tree.Draw('met>>met_hist9', cut, '')
	tree.Draw('mjj>>mjj_hist9', cut, '')
	tree.Draw('jet_pt[0]>>leadingJetPt_hist9', cut, '')
	tree.Draw('jet_pt[1]>>trailingJetPt_hist9', cut, '')
	tree.Draw('nJet>>numJets_hist9', cut, '')	
	
	#met_hist9 = ROOT.gDirectory.Get('met_hist9')
	#mjj_hist9 = ROOT.gDirectory.Get('mjj_hist9')
	#leadingJetPt_hist9 = ROOT.gDirectory.Get('leadingJetPt_hist9')
	#trailingJetPt_hist9 = ROOT.gDirectory.Get('trailingJetPt_hist9')
	#numJets_hist9 = ROOT.gDirectory.Get('numJets_hist9')
	
	cut += ' && met > ' + str(met_cut)

	eventCounter[10] = tree.GetEntries(cut)
	tree.Draw('met>>met_hist10', cut, '')
	tree.Draw('mjj>>mjj_hist10', cut, '')
	tree.Draw('jet_pt[0]>>leadingJetPt_hist10', cut, '')
	tree.Draw('jet_pt[1]>>trailingJetPt_hist10', cut, '')
	tree.Draw('nJet>>numJets_hist10', cut, '')	
	
	#met_hist10 = ROOT.gDirectory.Get('met_hist10')
	#mjj_hist10 = ROOT.gDirectory.Get('mjj_hist10')
	#leadingJetPt_hist10 = ROOT.gDirectory.Get('leadingJetPt_hist10')
	#trailingJetPt_hist10 = ROOT.gDirectory.Get('trailingJetPt_hist10')
	#numJets_hist10 = ROOT.gDirectory.Get('numJets_hist10')
	
	#Create the output directory for png files if not created before

	outputDir = 'histos_pngFiles'

	if not os.path.isdir(outputDir):

		os.mkdir(outputDir)

	hist_names = ['met_hist', 'mjj_hist', 'leadingJetPt_hist', 'trailingJetPt_hist', 'numJets_hist']

	#Label and save the histograms

	for hist_name in hist_names:

		for num in range(11):

			histo_label = hist_name + str(num)
			
			#Retrieve the histogram so that Python knows about it 
			hist = ROOT.gDirectory.Get(histo_label)

			print(hist)
			print(type(hist))

			x_label = histo_label.split('_')[0]
		
			if x_label != 'numJets':
				x_label += ' [GeV]'	
				hist.GetXaxis().SetTitle(x_label)
		
			else:
				hist.GetXaxis().SetTitle(x_label)
			
			hist.GetYaxis().SetTitle('Number of Events')
			hist.SetTitle('')

			#Save the histgrams as png files
			
			canv = ROOT.TCanvas('canv', 'canv')
			hist.Draw()
			pngFile = os.path.join(outputDir, histo_label+'.png')

			canv.Print(pngFile)

	out.Write()
	out.Close()

	#print(eventCounter)
	#print(labels)

	return labels, eventCounter

def applyL1Selection(event):
	
	'''
	Applies L1 selection to a given event.
	Returns True if event passes the L1 trigger, otherwise returns False.
	'''

	if event.L1_nJet < 2: return False

	else:
		
		L1_totalEnergy = event.L1_jet_energy[0] + event.L1_jet_energy[1]
		L1_totalPx = event.L1_jet_px[0] + event.L1_jet_px[1]			
		L1_totalPy = event.L1_jet_py[0] + event.L1_jet_py[1]			
		L1_totalPz = event.L1_jet_pz[0] + event.L1_jet_pz[1]			
		
		L1_mjj = sqrt(L1_totalEnergy**2 - L1_totalPx**2 - L1_totalPy**2 - L1_totalPz**2) #Invariant mass of two leading jets at L1 level

		if not (event.L1_jet_pt[0] > 115 and event.L1_jet_pt[1] > 40 and L1_mjj > 620): return False #Simulating the L1 trigger

	return True

def applyHLTSelection(event, HLT_path):

	'''
	Applies L1 + HLT trigger selections for a given event.
	Returns True if event passes the L1 trigger and HLT trigger specified, otherwise returns False.
	'''
	
	if applyL1Selection(event):
	
		if getattr(event, HLT_path) == 1: return True

		else: return False
	
	return False

def applyAllSelections(event, HLT_path):

	'''
	Applies L1 + HLT + VBF selections for a given event and HLT_path.
	Returns True if event passes all the selections, otherwise returns False.
	'''

	return applyHLTSelection(event, HLT_path) and applyVBFSelections(event)
	
