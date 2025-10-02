# Model-Driven-Development -- SWEN - 746 
# Lianna Pottgen -- lrp2755
# Homework #4

## Getting Started
Overall, this README will overlook how to run the 2 new python files repo_miner.py and test_repo.py and the additions from Homework 43!

## Usage

repo_miner.py can be run with the command: python -m src.repo_miner fetch-issues --repo owner/repo [--state all|open|closed] [--max 50] --out issues.csv

for my specific repo, the final command is:  "python3 -m repo_miner fetch-commits --repo lrp2755/Model-Driven-Development --out commits.csv"

test_repo.py can be run directly from the python file!

## Contributing

This repository is based off of the past 2 weeks of the homeworks from last week and builds upon the same topics. 
Compared to last week with just setting up the repository, I've updated repo_miner.py to have a new fetch_issues method based on the file we were given for our homework. This method  will create a dataframe of issues that are not PRs from a given repository. The result of this method running is in issues.csv.
In addition with the repo_miner.py file, I also updated test_repo.py to include 3 new tests. These tests will access the validity of fetch_issues() by testing if the duration days are accurate, confirming that PRs are not included, and that the date is parsed and ISO correctly.

## License

Pandas, pytest, and PyGithub must be installed. 