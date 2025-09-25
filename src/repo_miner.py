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
        print(branch)
        # remove Branch(name="
        branch_name = str(branch)[13:len(str(branch))-2]
        commits = repo.get_commits(sha=branch_name)

        # Iterate and print commit information
        for commit in commits:
            print("Branch: "+str(branch))
            print(f"SHA: {commit.sha}")
            print(f"Author: {commit.author.login if commit.author else 'N/A'}")
            print(f"Date: {commit.commit.author.date}")
            print(f"Message: {commit.commit.message}")
            print("-" * 20)
        i += 1


'''
def fetch_commits(repo_name: str, max_commits: int = None) -> pd.DataFrame:
    """
    Fetch up to `max_commits` from the specified GitHub repository.
    Returns a DataFrame with columns: sha, author, email, date, message.
    """
    # 1) Read GitHub token from environment
    github_token = os.getenv("GITHUB_TOKEN")

    # 2) Initialize GitHub client
    # it is public sooooo we don't need to do auth?
    github_auth = Github()
    owner = "lrp2755"
    repo_name = "Model-Driven-Development"

    try:
        # 2) get the repo
        repo = github_auth.get_user(owner).get_repo(repo_name)

        # 3) Fetch commit objects (paginated by PyGitHub)
        # TODO
        main_commits = repo.get_commits(sha="main")
        for commit_val in main_commits:
            # SHA (hexsha)
            #sha = commit_val.hexsha

            # Author name and email
            author_name = commit_val.author.name
            author_email = commit_val.author.email

            # Commit date in ISO-8601 format
            # Convert timestamp to datetime object, then format to ISO-8601
            #commit_datetime = datetime.fromtimestamp(commit_val.committed_date)
            #commit_date_iso = commit_datetime.isoformat()

            # First line of the commit message
            #message_first_line = commit_val.message.splitlines()[0]

            current_commit = ["t", author_name, author_email, "t", ""]
            print(current_commit)
            #final_commits.append(current_commit)
        rm0_commits = repo.get_commits(sha="rm0-dev")

        # 4) Normalize each commit into a record dict
        # TODO
        final_commits = []

        # sha, author, email, date (ISO-8601), message (first line)
        for commit_val in repo.iter_commits():
            # SHA (hexsha)
            sha = commit_val.hexsha

            # Author name and email
            author_name = commit_val.author.name
            author_email = commit_val.author.email

            # Commit date in ISO-8601 format
            # Convert timestamp to datetime object, then format to ISO-8601
            commit_datetime = datetime.fromtimestamp(commit_val.committed_date)
            commit_date_iso = commit_datetime.isoformat()

            # First line of the commit message
            message_first_line = commit_val.message.splitlines()[0]

            current_commit = [sha, author_name, author_email, commit_date_iso, message_first_line]
            final_commits.append(current_commit)

        ''''''for commit_val in rm0_commits:
            # SHA (hexsha)
            sha = commit_val.hexsha

            # Author name and email
            author_name = commit_val.author.name
            author_email = commit_val.author.email

            # Commit date in ISO-8601 format
            # Convert timestamp to datetime object, then format to ISO-8601
            commit_datetime = datetime.fromtimestamp(commit_val.committed_date)
            commit_date_iso = commit_datetime.isoformat()

            # First line of the commit message
            message_first_line = commit_val.message.splitlines()[0]
            current_commit = [sha, author_name, author_email, commit_date_iso, message_first_line]
            rm0_commits_normalized.append(current_commit)
        ''''''

        # 5) Build DataFrame from records
        # TODO
        df = pd.DataFrame()

        df['commits'] = final_commits

        print(df)

    except Exception as e:
        print(f"Error getting repository: {e}")
'''

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
