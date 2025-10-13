''''
Lianna Pottgen - lrp2755
Model Driven Development - SWEN.746
Homework #4
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
        self.author = author
        self.email = email
        self.date = date
        self.message = message

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

    def set_repo(self, repo):
        self._repo = repo

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

'''
    test_fetch_commits_basic is a test that will determine if all of the columns are correct in 
    the csv file that we get from the method, check both commits are in the csv file, and 
    the first message. This utilizes monkeypatch to use the dummy GitHub classes.
'''
def test_fetch_commits_basic(monkeypatch):
    # Setup dummy commits
    now = datetime.now()
    commits = [
        DummyCommit("sha1", "Alice", "a@example.com", now, "Initial commit\nDetails"),
        DummyCommit("sha2", "Bob", "b@example.com", now - timedelta(days=1), "Bug fix")
    ]
    gh_instance = DummyGithub("fake-token")
    gh_instance.set_repo(DummyRepo(commits, []))

    # monkeypatch fetch_issues to use our dummy instance
    import src.repo_miner as repo_miner
    monkeypatch.setattr(repo_miner, "Github", lambda: gh_instance)

    df = fetch_commits("any/repo", None)

    assert list(df.columns) == ["shas", "author_names", "author_emails", "commit_dates", "messages"]
    assert len(df) == 2
    first_commit = df['messages'][0]
    assert first_commit == "Initial commit"

'''
    the test_fetch_commits_basic() function is a function that will test if the fetch_commits
    method from repo_miner will accurately respect the max_commit parameter. 
    This is tested by utilizing pytest.mark.vcr() and a smaller repo like the one suggested
    int the write up (octocat/Hello-World) with no max_commits parameter to get the total number 
    of commits and a number less than that total commits number.
'''
@pytest.mark.vcr()
def test_fetch_commits_limit(monkeypatch):
    now = datetime.now()
    commits = [
        DummyCommit("sha1", "Alice", "a@example.com", now, "Initial commit\nDetails"),
        DummyCommit("sha2", "Bob", "b@example.com", now - timedelta(days=1), "Bug fix")
    ]
    gh_instance = DummyGithub("fake-token")
    gh_instance.set_repo(DummyRepo(commits, []))

    # monkeypatch fetch_issues to use our dummy instance
    import src.repo_miner as repo_miner
    monkeypatch.setattr(repo_miner, "Github", lambda: gh_instance)

    df_with_commits = fetch_commits("any/repo", None)
    df_max_zero = fetch_commits("any/repo", 0)

    assert len(df_with_commits) == 2 and len(df_max_zero) == 0

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

'''
    test_fetch_issues_pr_excluded() is a test that will confirm that PRs are excluded in the 
    fetch issues method. This will create an issue that has a PR and one that does not and 
    confirmt that only 1 commit is actually included in the final csv file.
'''
@pytest.mark.vcr()
def test_fetch_issues_pr_excluded(monkeypatch):
    #ids,numbers,titles,users,states,create_ats,open_duration_days,closed_ats,comments

    now = datetime.now()
    issues = [
        DummyIssue(1, 101, "Issue A", "alice", "open", now, None, 0, False),
        DummyIssue(2, 102, "Issue B", "bob", "closed", now - timedelta(days=2), now, 2, True)
    ]

    gh_instance = DummyGithub("fake-token")
    gh_instance.set_repo(DummyRepo([], issues))

    # monkeypatch fetch_issues to use our dummy instance
    import src.repo_miner as repo_miner
    monkeypatch.setattr(repo_miner, "Github", lambda: gh_instance)

    df = fetch_issues("any/repo", state="all")

    assert len(df) == 1

'''
    test_fetch_issues_date_parse_correct() is a test that will confirm that the date of each of 
    the lines in the csv file have an ISO formatted date. I checked this by comparing strings
    and taking off extra data. 
'''
@pytest.mark.vcr()
def test_fetch_issues_date_parse_correct(monkeypatch):
    now = datetime.now()
    issues = [
        DummyIssue(1, 101, "Issue A", "alice", "open", now, None, 0),
        DummyIssue(2, 102, "Issue B", "bob", "closed", now - timedelta(days=2), now, 2)
    ]
    gh_instance = DummyGithub("fake-token")
    gh_instance.set_repo(DummyRepo([], issues))

    # monkeypatch fetch_issues to use our dummy instance
    import src.repo_miner as repo_miner
    monkeypatch.setattr(repo_miner, "Github", lambda: gh_instance)

    df = fetch_issues("any/repo", state="all")

    create_ats = df['create_ats']
    closed_ats = df['closed_ats']

    # assert
    assert closed_ats[0] == ''
    assert str(closed_ats[1]).split(".")[0] == now.isoformat().split(".")[0]
    assert str(create_ats[0]).split(".")[0]  == now.isoformat().split(".")[0]
    assert str(create_ats[1]).split(".")[0]  == ((now - timedelta(days=2)).isoformat()).split(".")[0]

'''
    test_fetch_issues_open_duration_days() is a test that will confirm that the days between
    idea is accurate in the fetch issues methods. This will check to compare the 2 dates in
    GitHub dummy issues and will ensure the final number on the csv file is accurate. This 
    goes for both issues that are closed and some that are still open. 
'''
@pytest.mark.vcr()
def test_fetch_issues_open_duration_days(monkeypatch):
    now = datetime.now()
    issues = [
        DummyIssue(1, 101, "Issue A", "alice", "open", now, None, 0),
        DummyIssue(2, 102, "Issue B", "bob", "closed", now - timedelta(days=2), now, 2)
    ]

    gh_instance = DummyGithub("fake-token")
    gh_instance.set_repo(DummyRepo([], issues))

    # monkeypatch fetch_issues to use our dummy instance
    import src.repo_miner as repo_miner
    monkeypatch.setattr(repo_miner, "Github", lambda: gh_instance)

    df = fetch_issues("any/repo", state="all")

    # Check date normalization
    time_between = df['open_duration_days']

    assert time_between[0] == 0 and time_between[1] == 2

def test_merge_and_summarize_output(capsys):
    # Prepare test DataFrames
    df_commits = pd.DataFrame({
        "sha": ["a", "b", "c", "d"],
        "author": ["X", "Y", "X", "Z"],
        "email": ["x@e", "y@e", "x@e", "z@e"],
        "date": ["2025-01-01T00:00:00", "2025-01-01T01:00:00",
                 "2025-01-02T00:00:00", "2025-01-02T01:00:00"],
        "message": ["m1", "m2", "m3", "m4"]
    })
    df_issues = pd.DataFrame({
        "id": [1,2,3],
        "number": [101,102,103],
        "title": ["I1","I2","I3"],
        "user": ["u1","u2","u3"],
        "state": ["closed","open","closed"],
        "created_at": ["2025-01-01T00:00:00","2025-01-01T02:00:00","2025-01-02T00:00:00"],
        "closed_at": ["2025-01-01T12:00:00",None,"2025-01-02T12:00:00"],
        "comments": [0,1,2]
    })
    # Run summarize
    merge_and_summarize(df_commits, df_issues)
    captured = capsys.readouterr().out
    # Check top committer
    assert "Top 5 committers" in captured
    assert "X: 2 commits" in captured
    # Check close rate
    assert "Issue close rate: 0.67" in captured
    # Check avg open duration
    assert "Avg. issue open duration:" in captured

