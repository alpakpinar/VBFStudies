# Helper script to call writeTree script 
# 5 times in a row

from subprocess import Popen
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--txtFileCounter', help='''Determines which txt file to be run over.
                                                 file=0: File will run over the first .txt file in the backgroundFiles dir
                                                 file=1: File will run over the second .txt file in the backgroundFiles dir
                                                 and so on.''', type = int)

parser.add_argument('-c', '--rootFileCounter', help = '''Determines the index of the first ROOT file to be run over. 
                                                     counter=0: File will run over files 1-5, 6-10, ... up to 21-25 in 5 steps 
                                                     counter=1: File will run over files 6-10, 11-15, ... up to 26-30 in 5 steps 
                                                     and so on.''', type = int)

args = parser.parse_args()

txtFile_counter = args.txtFileCounter
rootFile_counter= args.rootFileCounter

for numIter in range(5):

	file_idx = rootFile_counter*5 + 1
	
	logFile_path = 'logFiles/log{}/log{}_{}-{}.log'.format(txtFile_counter, txtFile_counter, file_idx, file_idx+4)

	logFile = file(logFile_path, 'w')

	command_as_aList = ['python', '-u', 'writeTree_2017MiniAOD.py', '-b', '-c', str(rootFile_counter), '-f', str(txtFile_counter)]

	print(' '.join(command_as_aList))

	command = Popen(command_as_aList, stdout=logFile)
	
	rootFile_counter += 1



