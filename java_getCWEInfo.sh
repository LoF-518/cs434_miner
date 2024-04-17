#!/bin/bash

#pre-clean and setup
echo "performing pre-clean and setup..."
rm -rf temp
rm -rf $1_results
rm -f *.xml *.dot
mkdir $1_results

#collect last 100 non-merge commits
python3 getCommits.py $1 $2 > $1_results/$1.commits
#python3 getCommitsInfo.py $1

ver=0
cat $1_results/$1.commits | while IFS= read -r line; do
	
	#checkout commit
	python3 checkout.py $1 $line
	
	# cp -r $1 $1_results/v${ver}
	mkdir $1_results/v${ver}
	# cd $1_results/v${ver}/
	# mkdir analysis
	# cd -
	# vulture --min-confidence 80 $file > ${file}_vulture.txt
	echo "executing CK for [v${ver}]..."
	java -jar ~/Downloads/ck-ck-0.7.0/target/ck-0.7.0-jar-with-dependencies.jar $1 false 0 false $1_results/v${ver}/ #analysis/
	
	echo "executing Lizard for [v${ver}]..."
	# bandit -iii -r $file > ${file}bandit.txt
	lizard -m $1 > $1_results/v${ver}/lizard.txt #${file}analysis/lizard.txt
	ver=$((ver+1))
done

# #run SATs on each version
# collection=`ls -d $1_results/*/`
# for file in ${collection};
# do
# 	echo "executing Lizard on [$file]..."
# 	# bandit -iii -r $file > ${file}bandit.txt
# 	lizard -m $file > ${file}analysis/lizard.txt
	
# done 

rm -rf $1

