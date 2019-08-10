# VBF Studies

Code used for VBF trigger study.

### Write to a tree from a MiniAOD file

Using writeTree\_2017MiniAOD.py, the contents of a MiniAOD file can be read and written into a tree. A new ROOT file containing this tree will be produced in the inputs/ directory. Declaration of the branches can be found at lib/vbf\_tree\_2017.py file. Only the information present in the current branches will be saved into the output tree.

writeTree\_2017MiniAOD.py is meant to read 2017 MiniAOD files, and some id requirements (e.g. tight jet id) are 2017 requirements. writeTree\_2018MiniAOD.py is out of date and it is not updated properly, so it's not recommended to use that script.

writeTree\_2017MiniAOD.py takes several command line options:

- `-t`, `--test`       : For testing, script called with this option will only run over the first two files in the list.
- `-s`, `--shortTest`  : For even shorter testing, script called with this option will run over the first 100 events in the first two files in the list. Meant for very quick tests/debugging.
- `-l`, `--local`      : If specified, the script will run over the local 2017 signal samples placed in evaluateJetPairs/inputs/ROOT\_MCFiles directory. (not on GitHub)
- `-b`, `--background` ; If specified, the script will run over background files. These background files are listed in the .txt files in inputs/backgroundFiles. 
- `-c`, `--counter`    : Must be specified if the script is to be run over background files, otherwise not neccessary. Used to divide the background samples in .txt files into chunks of 5.  
						 counter=0 will run over the files 1-5 in the given txt file.
						 counter=1 will run over the files 6-10 in the given txt file.
						 and so on.
- `-f`, `--fileIdx`    : Must be specified if the script is to be run over background files, otherwise not neccessary. Used to identify which txt file in inputs/backgroundFiles will be considered.
						 fileIdx=0 will run over the first .txt file in inputs/backgroundFiles.
						 fileIdx=1 will run over the second .txt file in inputs/backgroundFiles.
						 and so on.	
 
