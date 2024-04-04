import requests
import time
import csv
import sys
from typing import Callable, List
# import subprocess
from more_itertools import unique_everseen
from miner_models import GitHubProject

columns = ["Project_name", "URL", "stars"]

counter = 0


def fetch_projects(query, language, order_by=None, order=None):
    rows = []
    i = 1  # page number
    flag = 1
    page_count = 10
    per_page = 30

    session = requests.Session()
    session.headers.update({"Accept":"application/vnd.github+json"})
    
    while flag == 1:
        global counter
        counter += 1
        time.sleep(10)
        # print(counter)
        if order == None:
            url = f"https://api.github.com/search/repositories?q={query}+language:{language}&page={i}&per_page={per_page}"
        else:
            url = f"https://api.github.com/search/repositories?q={query}+language:{language}&sort={order_by}&order={order}&page={i}&per_page={per_page}"

        user_data_response = session.get(url)
        try:
            # print(user_data.status_code)
            if user_data_response.status_code == 200:
                # print(user_data_response.headers.get("Content-Type"))
                user_data = user_data_response.json()
            else:
                raise Exception("GET request failed")
        except Exception as e:
            print(user_data_response.text)
        j = 0
        # stars_flag=1
        while j < per_page:  # fetch 30 projects at a time
            if i > page_count:
                flag = 0
                break
            else:
                try:
                    name = (user_data["items"][j]).get("full_name")
                    url = (user_data["items"][j]).get("html_url")
                    stars = int((user_data["items"][j]).get("stargazers_count"))
                    # stars_flag=int(stars)
                    # print (name, url, stars)
                    if stars > 100:
                        rows.append(GitHubProject(stars, name, url))
                except:
                    pass
            j += 1
        i += 1
    session.close()
    return rows

if __name__ == "__main__":
    query = sys.argv[1]
    lang = sys.argv[2]
    file_name = sys.argv[3]
    rows = fetch_projects(query, lang, "stars", "desc")
    rows.extend(fetch_projects(query, lang, "stars", "asc"))
    rows.extend(fetch_projects(query, lang))

    # sorter: Callable[[GitHubProject], int] = lambda x : x.iter()[-1]

    # rows : List[GitHubProject] = sorted(unique_everseen(rows, key=lambda x : x.iter()[:2]), key=sorter, reverse=True)

    rows = sorted(unique_everseen(rows), reverse=True)

    with open(f"{file_name}.csv", "w") as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(columns)
        for row in rows:
            # print(r)
            writer.writerow(row.iter())

# remove duplicate rows

# with open("py_projects.csv", "r") as f, open("py_projects_unique.csv", "w") as out_file:
    # out_file.writelines(unique_everseen(f))

# subprocess.run(["rm", "-f", "py_projects.csv"])
# subprocess.run(["mv", "py_projects_unique.csv", "py_projects.csv"])
