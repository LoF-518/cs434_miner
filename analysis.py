from parse_metrics import *
import pandas as pd
import sys

def generate_plots(metrics, repo):
    df = pd.DataFrame.from_dict(metrics).T
    df.to_csv(f"{repo}_results/metrics.csv")
    

def iterate_and_get_dfs(lang, repo):
    # Iterate over the results of the repo
    # Get results in a DataFrame for each version
    versions = list_files(repo+"_results")
    dfs = []
    for version in versions:
        if ".commits" in version or ".csv" in version:
            continue
        if lang == "python":
            lcom = read_python_lcom_metrics(repo+"_results/"+version)
            vulture_issue_counts = read_python_vulture_report(repo+"_results/"+version)
            ccn = read_project_ccns(repo+"_results/"+version)
            dfs.append((version, lcom, ccn, vulture_issue_counts))
        elif lang == "java":
            lcom = read_java_lcom_metrics(repo+"_results/"+version)
            ccn = read_project_ccns(repo+"_results/"+version)
            dfs.append((version, lcom, ccn))
    return dfs

if __name__ == "__main__":
    lang = sys.argv[1]
    repo = sys.argv[2]
    metrics = dict()
    for item in sorted(iterate_and_get_dfs(lang, repo), key=lambda x: int(x[0][1:])):
        if lang == "python":
            converted = item[1].loc[:, 'LCOM4'].astype('int32')
            avg_lcom, count = converted.describe()[['mean', 'count']]
            lcom4_gte_2 = len(converted[converted >= 2])
            lcom4_lt_1 = len(converted[converted < 1])
            avg_ccn = item[2].loc[:, 'CCN'].describe()['mean']
            complex_method_count = len(item[2][(item[2]['CCN'] > 15) | (item[2]['PARAM'] > 10)])
            metrics.update({item[0]: item[3]})
            metrics[item[0]].update({
                'avg_lcom': avg_lcom, 
                'avg_ccn': avg_ccn, 
                'complex_method_count': complex_method_count, 
                'lcom4_gte_2': lcom4_gte_2,
                'lcom4_lt_1': lcom4_lt_1,
                'count': count
            })
        elif lang == "java":
            avg_lcom, count = item[1].loc[:, 'lcom*'].describe()[['mean', 'count']]
            avg_ccn = item[2].iloc[:, 1].describe()['mean']
            lcom5_gte_90 = len(item[1][item[1]['lcom*'] >= 0.9])
            complex_method_count = len(item[2][(item[2]['CCN'] > 15) | (item[2]['PARAM'] > 10)])
            metrics.update({item[0]: dict()})
            metrics[item[0]].update({
                'avg_lcom': avg_lcom, 
                'avg_ccn': avg_ccn, 
                'complex_method_count': complex_method_count,
                'lcom5_gte_90': lcom5_gte_90,
                'count': count
            })
    generate_plots(metrics, repo)
    