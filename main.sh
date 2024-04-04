#!/bin/bash

# Reading py_projects.csv line-by-line
tail -n +2 py_projects.csv | while IFS= read -r line; do
	project=$line; 
	project=${project##*/}
	# Getting project name
	project=`echo $project | cut -d"," -f1`
	# Getting GitHub link
	line=`echo $line | cut -d"," -f2`
	# Cloning into the project from the given link
	git clone $line
	# Running the Miner
	bash getCWEInfo.sh $project
done
