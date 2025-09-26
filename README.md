# Model-Driven-Development -- SWEN - 746 
# Lianna Pottgen -- lrp2755
# Homework #3

## Getting Started
Overall, this README will overlook how to run the 2 new python files repo_miner.py and test_repo.py and the additions from Homework #3!

## Usage

repo_miner.py can be run with the command  "python3 -m repo_miner fetch-commits --repo path --out commits.csv"
for my specific repo, the final command is: "python3 -m repo_miner fetch-commits --repo lrp2755/Model-Driven-Development --out commits.csv"

test_repo.py can be run directly from the python file!

## Contributing

This repository is based off of the first start of the homework from last week and builds upon the same topics. 
Compared to last week with just setting up the repository, I've updated repo_miner.py to have a couple of new methods based on the file we were given for our homework. More specifically, I edited the fetch_commits() method that will create a dataframe of commits from a given repository. The result of this method running is in commits.csv.
In addition with the repo_miner.py file, I also updated test_repo.py to include 2 new tests. These tests will test the validity of fetch_commits() including cases where max_commits is used and when there are no commits int the repo.

## License

Pandas, pytest, and PyGithub must be installed. 