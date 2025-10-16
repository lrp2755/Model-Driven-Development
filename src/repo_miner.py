''''
Lianna Pottgen - lrp2755
Model Driven Development - SWEN.746
Homework #5
repo_miner.py
'''

import argparse
from collections import Counter
from datetime import datetime
import pandas as pd
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
    merge_and_summarize is a method that will take in 2 data frames and determine
    the top 5 committers by commit count, issue closing rate, and average open duration
    for closed issues. This will utilize the dataframes from the commits.csv and issues.csv
    files and will print out the data to the user!
'''
def merge_and_summarize(commits_df: pd.DataFrame, issues_df: pd.DataFrame) -> None:
    """
    Takes two DataFrames (commits and issues) and prints:
      - Top 5 committers by commit count
      - Issue close rate (closed/total)
      - Average open duration for closed issues (in days)
    """
    # Copy to avoid modifying original data
    commits = commits_df.copy()
    issues  = issues_df.copy()


    # 1) Normalize date/time columns to pandas datetime
    commits['date'] = pd.to_datetime(commits['date'], errors='coerce')
    issues['created_at'] = pd.to_datetime(issues['created_at'], errors='coerce')
    issues['closed_at'] = pd.to_datetime(issues['closed_at'], errors='coerce')

    commits_per_day = commits.groupby('date').size().reset_index(name='commits_count')
    issues_created_per_day = issues.groupby('created_at').size().reset_index(name='issues_created')
    issues_closed_per_day = issues.groupby('closed_at').size().reset_index(name='issues_closed')

    merged = (
        commits_per_day
        .merge(issues_created_per_day, left_on='date', right_on='created_at', how='outer')
        .merge(issues_closed_per_day, left_on='date', right_on='closed_at', how='outer')
    )

    issues_created_at_array = issues['created_at']
    issues_closed_at_array = issues['closed_at']

    users_array = commits['author']
    issues_closed = 0
    average_days_open = 0
    for i in range(0, len(issues_closed_at_array)):
        if(str(issues_closed_at_array[i]) != "nan" and str(issues_closed_at_array[i]) != "None" and str(issues_closed_at_array[i]) != "NaT"):
            issues_closed += 1
        if (issues_closed_at_array[i] is None or str(issues_closed_at_array[i]) == "nan" or str(issues_closed_at_array[i]) == "NaT"):
            closed_at = datetime.now().isoformat()
        else:
            closed_at = issues_closed_at_array[i].isoformat()

        date_one = datetime.fromisoformat(closed_at)
        date_two = datetime.fromisoformat(str(issues_created_at_array[i]))

        date_one = date_one.replace(tzinfo=None)
        date_two = date_two.replace(tzinfo=None)

        difference = abs((date_two.date() - date_one.date()).days)
        average_days_open += difference

        #average_days_open += issues_days_open_array[i]

    # 2) Top 5 committers
    author_counts = Counter(users_array)
    top_five_committers = author_counts.most_common(5)
    author_name = ""

    print("Top 5 committers: ")
    if(len(top_five_committers) >= 5):
        for i in range(0, 5):
            if ("GitAuthor" in top_five_committers[i][0]):
                author_name = top_five_committers[i][0].split("\"")[1]
            else:
                author_name = top_five_committers[i][0]
            print("\t"+str(author_name) + ": " + str(top_five_committers[i][1]) + " commits")
    else:
        for author in top_five_committers:
            if ("GitAuthor" in author[0]):
                author_name = author[0].split("\"")[1]
            else:
                author_name =  author[0]
            print("\t"+str(author_name)+": "+str(author[1])+" commits")
        print("NOTE: There are less than 5 unique committers.")

    if(issues_closed == 0):
        # 3) Calculate issue close rate
        print("\nIssue close rate: 0.0")
        # 4) Compute average open duration (days) for closed issues
        print("Avg. issue open duration: " + str(average_days_open)+" days\n")
    else:
        # 3) Calculate issue close rate
        print("\nIssue close rate: "+str(round((issues_closed/len(issues_closed_at_array)),2)))
        # 4) Compute average open duration (days) for closed issues
        print("Avg. issue open duration: " + str(average_days_open / issues_closed)+" days\n")


'''
    the method fetch_issues() used in order to get all of the issues from the given
    repository. This will ignore pull requests as well. This also has 2 optional parameters, 
    state which will only get that specific state of the issue from that repo and max_issues
    which will only get up to that max number of issues from the repository
'''
def fetch_issues(repo_name: str, state: str = "open", max_issues: int = None) -> pd.DataFrame:
    # no authentication needed for public repositories so i didn't use a public key
    # 1) Read GitHub token
    g = Github()
    # 2) Get repo
    repo = g.get_repo(repo_name)
    # 3) Fetch issues, filtered by state ('all', 'open', 'closed')
    #print(state)
    if(state == "all"):
        issues = repo.get_issues(state="all")
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

    days_between = []

    i = 0

    # 4) Normalize each issue (skip PRs)
    for idx, issue in enumerate(issues):
        # checks if it's NOT a pull request
        if issue.pull_request is None:
            if max_issues is not None and i >= max_issues:
                break

            # id, number, title, user, state, created_at, closed_at, comments.
            ids.append(issue.id)
            numbers.append(issue.number)
            titles.append(issue.title)
            users.append(issue.user.login)
            states.append(issue.state)
            if(issue.closed_at is None):
                closed_ats.append('')
            else:
                closed_ats.append(issue.closed_at.isoformat())
            created_ats.append(issue.created_at.isoformat())
            comments.append(issue.comments)

            # updating the days inbetween
            if(issue.closed_at is None):
                closed_at = datetime.now()
            else:
                closed_at = issue.closed_at

            date_one = datetime.fromisoformat(closed_at.isoformat())
            date_two = datetime.fromisoformat(issue.created_at.isoformat())

            date_one = date_one.replace(tzinfo=None)
            date_two = date_two.replace(tzinfo=None)

            difference = abs((date_two.date() - date_one.date()).days)
            days_between.append(difference)

            i += 1

    # 5) Build DataFrame
    df['ids'] = ids
    df['numbers'] = numbers
    df['titles'] = titles
    df['user'] = users
    df['states'] = state
    df['created_at'] = created_ats
    df['open_duration_days'] =days_between
    df['closed_at'] = closed_ats
    df['comments'] = comments

    # return dataframe
    return df

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
        sha = commit_val.sha
        # author name and email
        author_name = commit_val.commit.author
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
    df['author'] = author_names
    df['author_emails'] = author_emails
    df['date'] = commit_dates
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

    # Sub-command: summarize
    c3 = subparsers.add_parser("summarize", help="Summarize commits and issues")
    c3.add_argument("--commits", required=True, help="Path to commits CSV file")
    c3.add_argument("--issues",  required=True, help="Path to issues CSV file")

    args = parser.parse_args()

    # Dispatch based on selected command
    if args.command == "fetch-commits":
        df = fetch_commits(args.repo, args.max_commits)
        df.to_csv(args.out, index=False)
        print(f"Saved {len(df)} commits to {args.out}")

    elif args.command == "fetch-issues":
        df = fetch_issues(args.repo, args.state, args.max_issues)
        df.to_csv(args.out, index=False)
        print(f"Saved {len(df)} issues to {args.out}")

    if args.command == "summarize":
        # Read CSVs into DataFrames
        commits_df = pd.read_csv(args.commits)
        issues_df  = pd.read_csv(args.issues)
        # Generate and print the summary
        merge_and_summarize(commits_df, issues_df)

if __name__ == "__main__":
    main()
