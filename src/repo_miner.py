''''
Lianna Pottgen - lrp2755
Model Driven Development - SWEN.746
Homework #3
repo_miner.py
'''

# !/usr/bin/env python3
"""
repo_miner.py

A command-line tool to:
  1) Fetch and normalize commit data from GitHub

Sub-commands:
  - fetch-commits
"""

import os
import argparse
import pandas as pd
from github import Github
from datetime import datetime

def fetch_commits(repo_name: str, max_commits: int = None) -> pd.DataFrame:
    owner = "lrp2755"
    repo_name = "Model-Driven-Development"

    # No authentication needed for public repositories (rate limits apply)
    g = Github()

    repo = g.get_user(owner).get_repo(repo_name)
    branches = repo.get_branches()
    i = 0
    
    for branch in branches:
        if(max_commits != None):
            if(i > max_commits):
                break

        branch_name = str(branch)[13:len(str(branch))-2]
        commits = repo.get_commits(sha=branch_name)

        # Iterate and print commit information
        for commit_val in commits:
            # SHA
            sha = commit_val.commit.sha

            # Author name and email
            author_name = commit_val.commit.author.name
            author_email = commit_val.commit.author.email

            # Commit date in ISO-8601 format
            commit_date = commit_val.commit.author.date.isoformat()

            # First line of the commit message
            message_first_line = commit_val.commit.message.splitlines()[0]

            current_commit = [sha, author_name, author_email, commit_date, message_first_line]
            print(current_commit)
        i += 1

def main():
    fetch_commits("Model-Driven-Development",0)
    """
    Parse command-line arguments and dispatch to sub-commands.
    """
    '''parser = argparse.ArgumentParser(
        prog="repo_miner",
        description="Fetch GitHub commits/issues and summarize them"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Sub-command: fetch-commits
    c1 = subparsers.add_parser("fetch-commits", help="Fetch commits and save to CSV")
    c1.add_argument("--repo", required=True, help="Repository in owner/repo format")
    c1.add_argument("--max", type=int, dest="max_commits",
                    help="Max number of commits to fetch")
    c1.add_argument("--out", required=True, help="Path to output commits CSV")

    args = parser.parse_args()

    # Dispatch based on selected command
    if args.command == "fetch-commits":
        df = fetch_commits(args.repo, args.max_commits)
        df.to_csv(args.out, index=False)
        print(f"Saved {len(df)} commits to {args.out}")'''


if __name__ == "__main__":
    main()
