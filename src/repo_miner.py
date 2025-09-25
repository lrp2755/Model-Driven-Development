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

import argparse
import pandas as pd
from github import Github

def fetch_commits(repo_name: str, max_commits: int) -> pd.DataFrame:
    # No authentication needed for public repositories (rate limits apply)
    g = Github()

    repo = g.get_repo(repo_name)
    branches = repo.get_branches()
    i = 0

    commits = repo.get_commits()
    df = pd.DataFrame()
    shas = []
    author_names = []
    author_emails = []
    commit_dates = []
    messages = []
    # Iterate and print commit information
    for commit_val in commits:
        if (max_commits != None and i > max_commits):
            break
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

        #df[f'Commit #{i}'] = [sha, author_name, author_email, commit_date, message_first_line]
        shas.append(sha)
        author_names.append(author_name)
        author_emails.append(author_email)
        commit_dates.append(commit_date)
        messages.append(message_first_line)
        #df['SHA'] += sha
        #df['Author Name'] += author_name
        #df['Author Email'] += author_email
        #df['Commit Date'] += commit_date
        #df['Message'] += message_first_line

        print(current_commit)
        i += 1
    df['shas'] = shas
    df['author_names'] = author_names
    df['author_emails'] = author_emails
    df['commit_dates'] = commit_dates
    df['messages'] = messages

    return df

def main():
    """
    Parse command-line arguments and dispatch to sub-commands.
    """
    parser = argparse.ArgumentParser(
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
        print(f"Saved {len(df)} commits to {args.out}")

if __name__ == "__main__":
    main()
