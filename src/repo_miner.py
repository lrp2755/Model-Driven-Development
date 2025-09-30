''''
Lianna Pottgen - lrp2755
Model Driven Development - SWEN.746
Homework #3
repo_miner.py
'''
import os
import argparse
import pandas as pd
from certifi.__main__ import args
from github import Github

# !/usr/bin/env python3
"""
repo_miner.py

A command-line tool to:
  1) Fetch and normalize commit data from GitHub

Sub-commands:
  - fetch-commits
"""

'''
    the method fetch_issues() is referenced in the given test_repo.py file for 
    this homework so i created a simple stubbed function as a temporary holder 
    for the future!
    this method will be developed further in future homeworks
'''
def fetch_issues(repo_name: str, state: str = "all", max_issues: int = None) -> pd.DataFrame:
    """
    Fetch up to `max_issues` from the specified GitHub repository (issues only).
    Returns a DataFrame with columns: id, number, title, user, state, created_at, closed_at, comments.
    """
    # no authentication needed for public repositories so i didn't use a public key

    # 1) Read GitHub token
    g = Github()

    # 2) Initialize client and get the repo
    # getting the repo
    repo = g.get_repo(repo_name)

    # 3) Fetch issues, filtered by state ('all', 'open', 'closed')
    if(state == "all"):
        issues = repo.get_issues()
    elif(state == "open"):
        issues = repo.get_issues(state="open")
    elif(state == "closed"):
        issues = repo.get_issues(state="closed")

    # starting dataframe and the columns for the dataframe
    df = pd.DataFrame()

    ids = []
    numbers = []
    titles = []
    users = []
    states = []
    created_ats = []
    closed_ats = []
    comments = []

    # 4) Normalize each issue (skip PRs)
    # TODO
    for idx, issue in enumerate(issues):
        if max_issues and idx >= max_issues:
            break

        # Skip pull requests
        # TODO

        # Append records
        # TODO
        # id, number, title, user, state, created_at, closed_at, comments.
        ids.append(issue.id)
        numbers.append(issue.number)
        titles.append(issue.title)
        users.append(issue.user.login)
        states.append(issue.state)
        created_ats.append(issue.created_at)
        closed_ats.append(issue.closed_at)
        comments.append(issue.comments)

    # 5) Build DataFrame
    # TODO: return statement
    # updating dataframe columns
    df['ids'] = ids
    df['numbers'] = numbers
    df['titles'] = titles
    df['users'] = users
    df['states'] = state
    df['create_ats'] = created_ats
    df['closed_ats'] = closed_ats
    df['comments'] = comments

    # return dataframe
    return df

'''
    the method merge_and_summarize() is referenced in the given test_repo.py file for 
    this homework so i created a simple stubbed function as a temporary holder 
    for the future!
    this method will be developed further in future homeworks
'''
def merge_and_summarize():
    # stubbed function since there is import requesting merge_and_summarize() in test_repo.py!
    return None

'''
    fetch_commits() is a method that will take in a repo name and a number of max
    commits and save all of the commits in a data frame. the data frame will have
    the commits sha, author name, author email, commit date, and the first line of 
    the commit message. The information is gained using the Github import since my 
    repository is a public repository!
    The method will return the dataframe of all the commits from this repository
'''
def fetch_commits(repo_name: str, max_commits: int) -> pd.DataFrame:
    # no authentication needed for public repositories so i didn't use a public key
    g = Github()

    # getting the repo
    repo = g.get_repo(repo_name)
    i = 0

    # getting the commits
    commits = repo.get_commits()

    # starting dataframe and the columns for the dataframe
    df = pd.DataFrame()
    shas = []
    author_names = []
    author_emails = []
    commit_dates = []
    messages = []

    # iterate through commits and save information!
    for commit_val in commits:
        if ((isinstance(max_commits, int) and (max_commits != None and i >= max_commits))):
            break
        # SHA
        sha = commit_val.commit.sha
        # author name and email
        author_name = commit_val.commit.author.name
        author_email = commit_val.commit.author.email
        # commit date in ISO-8601 format
        commit_date = commit_val.commit.author.date.isoformat()
        # commit message
        message_first_line = commit_val.commit.message.splitlines()[0]
        # adding to future dataframe columns
        shas.append(sha)
        author_names.append(author_name)
        author_emails.append(author_email)
        commit_dates.append(commit_date)
        messages.append(message_first_line)

        # increasing for max commits
        i += 1

    # updating dataframe columns
    df['shas'] = shas
    df['author_names'] = author_names
    df['author_emails'] = author_emails
    df['commit_dates'] = commit_dates
    df['messages'] = messages

    # return dataframe
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
    c1.add_argument("--max",  type=int, dest="max_commits",
                    help="Max number of commits to fetch")
    c1.add_argument("--out",  required=True, help="Path to output commits CSV")

    # Sub-command: fetch-issues
    c2 = subparsers.add_parser("fetch-issues", help="Fetch issues and save to CSV")
    c2.add_argument("--repo",  required=True, help="Repository in owner/repo format")
    c2.add_argument("--state", choices=["all","open","closed"], default="all",
                    help="Filter issues by state")
    c2.add_argument("--max",   type=int, dest="max_issues",
                    help="Max number of issues to fetch")
    c2.add_argument("--out",   required=True, help="Path to output issues CSV")

    # Dispatch based on selected command
    if args.command == "fetch-commits":
        df = fetch_commits(args.repo, args.max_commits)
        df.to_csv(args.out, index=False)
        print(f"Saved {len(df)} commits to {args.out}")

    elif args.command == "fetch-issues":
        df = fetch_issues(args.repo, args.state, args.max_issues)
        df.to_csv(args.out, index=False)
        print(f"Saved {len(df)} issues to {args.out}")

if __name__ == "__main__":
    main()