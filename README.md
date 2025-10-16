# Model-Driven-Development -- SWEN - 746 
# Lianna Pottgen -- lrp2755
# Homework #5

## Getting Started
Overall, this README will overlook how to run the 2 python files repo_miner.py and test_repo.py and the additions from Homework 5!

## Usage

repo_miner.py for merge and summarize for HW #5 be run with the command: python3 -m repo_miner summarize --commits commits.csv --issues issues.csv

test_repo.py can be run directly from the python file or the CI. 

## Sample Results

For Homework #5, in order to sample the code I utilized the public MrB141107/Hacktoberfest_2022 repository. I googled "public repositories in github" and found that this one worked well! I tried the octocat hello world and it took too many attempts to find the system and get the issues so I decided to look for another one! 
I started by re-creating commits.csv and issues.csv to match MrB141107/Hacktoberfest_2022 and then I ran the merge and summarize command with the command " python3 -m repo_miner summarize --commits commits.csv --issues issues.csv "
The output of this command was: 
     
Top 5 committers: 
        IncrediblePro: 33 commits
        Yamilini2000: 3 commits
        Popstar Idhant: 3 commits
        Mr.B: 2 commits
        Anirban Saha: 2 commits

Issue close rate: 1.0
Avg. issue open duration: 3.0 days

In order to get accurate results the "python3 -m repo_miner fetch-issues --repo MrB141107/Hacktoberfest_2022 --out issues.csv" command and "python3 -m repo_miner fetch-commits --repo MrB141107/Hacktoberfest_2022 --out commits.csv" must be run with the MrB141107/Hacktoberfest_2022 repo so summarize will work correctly! 

Since the write up also says "Sample output (in your data/ directory) for a well-known repo." summarize will write to summarize.txt and summarize data so the sample output is in the directory as well. 

## Contributing

This repository is based off of the past couple of weeks of the homeworks from homework #1 to this most recent addition from homework #5. 
Compared to last week with adding in the fetch issues method, the merge and summarize method will utilize commits.csv and issues.csv in order to determine the top 5 committers, average open duration of closed issues, and the percent of closed issues. 
In addition with the repo_miner.py file, I also updated test_repo.py to include 1 new tests. This tests will access the validity of merge_and_summarize to confirm the acccuracy of the printed data.

## License

Pandas, pytest, and PyGithub must be installed. 