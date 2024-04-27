import os
import pandas as pd
from collections import defaultdict

# This module contains support methods to read the files
# and return back DataFrames to better support plotting, analysis etc.
# Methods in this module work on a single version

lizard_csv_columns = "NLOC,CCN,token,PARAM,length,location,file,function,long_name,start,end".split(",")

def list_files(repo):
    """Return a list of files"""
    return os.listdir(repo)


def read_java_lcom_metrics(repo):
    """Read the ck.jar output to extract the LCOM4 metric for each class in the project"""
    # Read given version's data to find out the class.csv file
    # Return a DataFrame from this csv file
    if "class.csv" not in list_files(repo):
        raise FileNotFoundError(f"{repo}/class.csv does not exist")
    return pd.read_csv(f"{repo}/class.csv")

def read_python_lcom_metrics(repo):
    """Read the lcom output to extract the LCOM4 metric for each class in the project"""
    # First line and third line are of no significance.
    # Second Line: trim, split by "|" and trim each again to get the columns
    # Subsequent lines are all data
    # Until the last 3 lines, which form the footer
    # Make a DataFrame out of this for all versions and return
    if "lcom.txt" not in list_files(repo):
        raise FileNotFoundError(f"{repo}/lcom.txt does not exist")
    records = [["Method", "LCOM4"]]
    with open(f"{repo}/lcom.txt", 'r') as file:
        text = file.readlines()
        for line in text:
            if "+" in line or "LCOM" in line or "Average" in line:
                continue
            p_line = line.strip()
            if p_line == "":
                continue
            fields = list(map(str.strip, p_line.split("|")))[1:-1]
            fields[1] = int(fields[1])
            records.append(fields)
    return pd.DataFrame.from_records(records[1:], columns=records[0])

def read_python_vulture_report(repo):
    """Read the Vulture output to extract the unused variables and other safely-resolvable issues in the project"""
    # Read each line and keep track of the issues pointed out
    # Make a DataFrame out of this and return
    issue_count_dict = defaultdict(lambda: 0)
    with open(f"{repo}/vulture.txt", 'r') as file:
        for line in file.readlines():
            tokens = line.split()
            # file_name = tokens[0].split(":")[0]
            issue = tokens[1:-3]
            issue_count_dict[' '.join(issue)] += 1
        # print(issues_dict)
    return dict(issue_count_dict)


def read_project_ccns(repo):
    """Read the Lizard output to extract the CCN metric for each method in the project"""
    # Read the lizard.csv file for the given version and create a DataFrame
    if "lizard.csv" not in list_files(repo):
        raise FileNotFoundError(f"{repo}/lizard.csv does not exist")
    return pd.read_csv(f"{repo}/lizard.csv", names=lizard_csv_columns)

if __name__ == "__main__":
    print(read_python_vulture_report("python-driver_results/v0/"))