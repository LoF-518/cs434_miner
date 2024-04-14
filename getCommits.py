import sys
from pydriller import Repository

def get_commits(path, last_n):
  count=0
  commit_reverse=[]
  repo_traverse = Repository(path,only_no_merge=True,order='reverse').traverse_commits()
  for commit in repo_traverse:
    if (commit.in_main_branch==True):
      count=count+1
      # print(commit.hash)
      commit_reverse.append(commit.hash)
    if count == last_n:
      break

  return commit_reverse[::-1]

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage: getCommits.py <repo-path> <last-n-commits>")
  commits = get_commits(sys.argv[1], int(sys.argv[2]))
  in_order='\n'.join(commits)
  print(in_order)
