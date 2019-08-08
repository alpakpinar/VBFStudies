#!/bin/bash

inputFile="inputs/MiniAOD_files2017.txt"

while read -r line; 
do 
	echo "Working on $line"
	xrdcp $line ./inputs/ROOT_MCFiles

done < $inputFile

