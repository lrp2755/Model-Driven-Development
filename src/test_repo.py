''''
Lianna Pottgen - lrp2755
Model Driven Development - SWEN.746
Homework #3
test_repo.py
'''

# tests/test_repo_miner.py

import os
import pandas as pd
import pytest
from datetime import datetime, timedelta
from src.repo_miner import fetch_commits, fetch_issues, merge_and_summarize

# --- Helpers for dummy GitHub API objects ---

class DummyAuthor:
    def __init__(self, name, email, date):
        self.name = name
        self.email = email
        self.date = date

class DummyCommitCommit:
    def __init__(self, author, message):
        self.author = author
        self.message = message

class DummyCommit:
    def __init__(self, sha, author, email, date, message):
        self.sha = sha
        self.commit = DummyCommitCommit(DummyAuthor(author, email, date), message)

class DummyUser:
    def __init__(self, login):
        self.login = login

class DummyIssue:
    def __init__(self, id_, number, title, user, state, created_at, closed_at, comments, is_pr=False):
        self.id = id_
        self.number = number
        self.title = title
        self.user = DummyUser(user)
        self.state = state
        self.created_at = created_at
        self.closed_at = closed_at
        self.comments = comments
        # attribute only on pull requests
        self.pull_request = DummyUser("pr") if is_pr else None

class DummyRepo:
    def __init__(self, commits, issues):
        self._commits = commits
        self._issues = issues

    def get_commits(self):
        return self._commits

    def get_issues(self, state="all"):
        # filter by state
        if state == "all":
            return self._issues
        return [i for i in self._issues if i.state == state]

class DummyGithub:
    def __init__(self, token):
        assert token == "fake-token"
        self._repo = None
    def set_repo(self, DummyRepo):
        self._repo = DummyRepo
    def get_repo(self, repo_name):
        # ignore repo_name; return repo set in test fixture
        return self._repo

@pytest.fixture(autouse=True)
def patch_env_and_github(monkeypatch):
    # Set fake token
    monkeypatch.setenv("GITHUB_TOKEN", "fake-token")
    # Patch Github class
    # TODO

# Helper global placeholder
gh_instance = DummyGithub("fake-token")

# --- Tests for fetch_commits ---
# An example test case

def test_fetch_commits_basic(monkeypatch):
    # Setup dummy commits
    now = datetime.now()
    commits = [
        DummyCommit("sha1", "Alice", "a@example.com", now, "Initial commit\nDetails"),
        DummyCommit("sha2", "Bob", "b@example.com", now - timedelta(days=1), "Bug fix")
    ]
    gh_instance._repo = DummyRepo(commits, [])
    df = fetch_commits("any/repo")
    assert list(df.columns) == ["sha", "author", "email", "date", "message"]
    assert len(df) == 2
    assert df.iloc[0]["message"] == "Initial commit"

# TODO： Test that fetch_commits respects the max_commits limit.
'''
    the test_fetch_commits_basic() function is a function that will test if the fetch_commits
    method from repo_miner will accurately respect the max_commit parameter. 
    This is tested by utilizing pytest.mark.vcr() and a smaller repo like the one suggested
    int the write up (octocat/Hello-World) with no max_commits parameter to get the total number 
    of commits and a number less than that total commits number.
'''
@pytest.mark.vcr()
def test_fetch_commits_limit(monkeypatch):
    df_no_max = fetch_commits("octocat/Hello-World", "")
    df_no_max.to_csv()

    df_set_max = fetch_commits("octocat/Hello-World", 2)
    df_set_max.to_csv()

    assert len(df_set_max) == 2 and (len(df_no_max)  > len(df_set_max))

# TODO: Test that fetch_commits returns empty DataFrame when no commits exist.
'''
    test_fetch_commits_empty() is a method that will check that if there are 0 commits
    in the repo there is still a data set returned. I tested this by setting the max commits
    to 0 which will replicate a case in which there is no iteration in the method for each 
    commit, and the df_set_max_.to_csv() in addition to the length of df_set_max check will 
    show that an empty dataframe is returned!
'''
@pytest.mark.vcr()
def test_fetch_commits_empty(monkeypatch):
    # setting a max of 0 commits
    df_set_max = fetch_commits("octocat/Hello-World", 0)
    df_set_max.to_csv()

    assert len(df_set_max) == 0


#PRs are excluded.
#Dates parse correctly.
#open_duration_days is computed accurately.
@pytest.mark.vcr()
def test_fetch_issues_pr_excluded(monkeypatch):
    #ids,numbers,titles,users,states,create_ats,open_duration_days,closed_ats,comments

    now = datetime.now()
    issues = [
        DummyIssue(1, 101, "Issue A", "alice", "open", now, None, 0),
        DummyIssue(2, 102, "Issue B", "bob", "closed", now - timedelta(days=2), now, 2)
    ]
    gh_instance._repo = DummyRepo([], issues)
    df = fetch_issues("any/repo", state="all")
    assert {"id", "number", "title", "user", "state", "created_at", "closed_at", "comments"}.issubset(df.columns)
    assert len(df) == 2
    # Check date normalization
    # TODO

def test_fetch_issues_date_parse_correct(monkeypatch):
    now = datetime.now()
    issues = [
        DummyIssue(1, 101, "Issue A", "alice", "open", now, None, 0),
        DummyIssue(2, 102, "Issue B", "bob", "closed", now - timedelta(days=2), now, 2)
    ]
    gh_instance = DummyGithub("fake-token")
    gh_instance.set_repo(DummyRepo([], issues))
    df = fetch_issues("any/repo", state="all")

    # Check date normalization
    # TODO
    # for all dates in date coloumn
    # check format is
    create_ats = df['create_ats']
    closed_ats = df['closed_ats']
    print(create_ats)

@pytest.mark.vcr()
def test_fetch_issues_open_duration_days(monkeypatch):
    now = datetime.now()
    issues = [
        DummyIssue(1, 101, "Issue A", "alice", "open", now, None, 0),
        DummyIssue(2, 102, "Issue B", "bob", "closed", now - timedelta(days=2), now, 2)
    ]

    gh_instance._repo = DummyRepo([], issues)
    df = fetch_issues("any/repo", state="all")
    assert {"id", "number", "title", "user", "state", "created_at", "closed_at", "comments"}.issubset(df.columns)
    assert len(df) == 2
    # Check date normalization
    # TODO
