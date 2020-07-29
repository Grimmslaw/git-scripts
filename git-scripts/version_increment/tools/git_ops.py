import os
from typing import List

from git import Repo, GitConfigParser, Actor, IndexFile, BaseIndexEntry, Commit


def get_author() -> Actor:
    info = {}

    gitconfig = GitConfigParser(os.path.expanduser('~/.gitconfig'))
    sections = gitconfig.sections()
    assert 'user' in sections
    user_items = gitconfig.items('user')

    for tup in user_items:
        info[tup[0]] = tup[1]
    assert 'name' in user_items and 'email' in user_items

    return Actor(name=info['name'], email=info['email'])


def get_repo(repo_filepath: str = None) -> Repo:
    if repo_filepath is not None:
        repo_abspath = os.path.abspath(repo_filepath)
    else:
        cwd = os.path.abspath(os.getcwd())
        assert '.git' in [x for x in os.listdir(cwd) if os.path.isdir(x)]
        repo_abspath = cwd
    return Repo(repo_abspath)


def get_head_commit(filepath: str):
    repo_path = os.path.abspath(filepath)
    repo = Repo(repo_path)

    return repo.head.commit


def get_unstaged_filenames(repo: Repo) -> list:
    untracked = repo.untracked_files
    other_unstaged = repo.index.diff(repo.head.commit) + repo.index.diff(None)
    return untracked + other_unstaged


def warn_master_commit(index: IndexFile):
    if index.repo.head.ref == index.repo.branches.master:
        warning_answer = input('Are you sure that you want to commit to the master branch? [y/N]')
        if warning_answer.lower() in ['y', 'yes', 'ye', 'yep', 'yeah']:
            print('Quitting...')
            raise RuntimeError


def git_add(index: IndexFile, files) -> List[BaseIndexEntry]:
    return index.add(files)


def git_commit(index: IndexFile, message: str) -> Commit:
    return index.commit(message, author=get_author())


def do_git_commit(message: str, filepath: str = None):
    repo = get_repo(filepath)
    index = repo.index
    unstaged_files = get_unstaged_filenames(repo)
    git_add(index, unstaged_files)
    warn_master_commit(index)
    commit = git_commit(index, message)
    print(commit.summary)
