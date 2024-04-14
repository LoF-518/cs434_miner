#!/bin/bash

# Reading py_projects.csv line-by-line
tail -n +2 $1 | while IFS= read -r line; do
	project=$line; 
	project=${project##*/}
	# Getting project name
	project=`echo $project | cut -d"," -f1`
	# Getting GitHub link
	line=`echo $line | cut -d"," -f2`
	# Cloning into the project from the given link
	git clone $line
	# Running the Miner
	cond=$1
	cond=${cond:0:2}
	if [[ $cond == "ja" ]];
	then
		bash java_getCWEInfo.sh $project $2
		# echo "java"
	elif [[ $cond == "py" ]];
	then
		bash py_getCWEInfo.sh $project $2
		# echo "python"
	fi
done
