"""A module containing git-specific operations that may be used by any of the scripts in the larger, outer module."""

import os
import logging
from typing import List

from git import Repo, GitConfigParser, Actor, IndexFile, BaseIndexEntry, Commit

LOGGER = logging.getLogger(__name__)


def get_author() -> Actor:
    """
    Get the name and email information in the user's .gitconfig.

    :return: the git author information as an :py:class:`~git.util.Actor`
    """
    info = {}

    gitconfig = GitConfigParser(os.path.expanduser('~/.gitconfig'))
    sections = gitconfig.sections()
    assert 'user' in sections, 'No "user" field in .gitconfig'
    user_items = gitconfig.items('user')

    for tup in user_items:
        info[tup[0]] = tup[1]
    assert 'name' in info and 'email' in info, 'Incomplete information (name and/or email) in .gitconfig'

    return Actor(name=info['name'], email=info['email'])


def get_repo(repo_filepath: str = None) -> Repo:
    """
    Retrieves a :py:class:`~git.repo.base.Repo` from the given filepath.

    :param str repo_filepath:
        [Opt] the path at which there may be a git repo, or nothing to use the current working directory's path
    :return:
        a `Repo` at the given filepath or at the current working directory if none at the former
    """
    LOGGER.debug(f'repo_filepath={repo_filepath}')
    if repo_filepath is not None:
        repo_abspath = os.path.abspath(repo_filepath)
    else:
        cwd = os.path.abspath(os.getcwd())
        assert '.git' in os.listdir(cwd)
        repo_abspath = cwd
    return Repo(repo_abspath)


def get_head_commit(filepath: str) -> Commit:
    """
    Get the head commit at the given filepath.

    :param str filepath:
        the path to the git repo whose head commit should be gotten
    :return:
        the :py:class:`~git.objects.commit.Commit` of the repo at the given path
    """
    LOGGER.debug(f'filepath={filepath}')
    repo = Repo(filepath)

    return repo.head.commit


def get_unstaged_filenames(repo: Repo) -> list:
    """
    Get the names of the files in this repo that are either unstaged or untracked.

    :param Repo repo:
        the repo to check for unstaged/untracked files
    :return:
        a list of diffs (`List[Union[DiffIndex, DiffIndex[Diff]]]`)
    """
    untracked = repo.untracked_files
    other_unstaged = repo.index.diff(repo.head.commit) + repo.index.diff(None)
    return untracked + other_unstaged


def warn_master_commit(index: IndexFile) -> None:
    """
    Ask the user if they truly wish to commit, in the case that they are on the master branch, halting
    execution if not.

    :param IndexFile index:
        the current index of the current branch of the current repo
    """
    if index.repo.head.ref == index.repo.branches.master:
        warning_answer = input('Are you sure that you want to commit to the master branch? [y/N]')
        if warning_answer.lower() in ['y', 'yes', 'ye', 'yep', 'yeah']:
            print('Quitting...')
            raise RuntimeError


def git_add(index: IndexFile, files) -> List[BaseIndexEntry]:
    """
    `git add` all of the given files within the current repo

    :param IndexFile index:
        the current index of the current branch of the current repo
    :param files:
        the files to be `git-add`'ed
    :return:
        the entries just added
    """
    return index.add(files)


def git_commit(index: IndexFile, message: str) -> Commit:
    """
    Commit all staged files in the current repo.

    :param IndexFile index:
        the current index of the current branch of the current repo
    :param message:
        the commit message to include with the files to be committed
    :return:
        a record of the commit (:py:class:`~git.objects.commit.Commit`), itself
    """
    return index.commit(message, author=get_author())


def do_git_commit(message: str, dirpath: str = None) -> None:
    """
    Perform the necessary functions to commit the files in the repo at the given path.

    :param str message:
        the commit message
    :param str dirpath:
        [Opt] the path to the repo to commit files to
    """
    LOGGER.debug(f'dirpath={dirpath}')
    repo = get_repo(dirpath)
    index = repo.index
    repo.git.add(update=True)
    warn_master_commit(index)
    commit = git_commit(index, message)
    print(f'\nCommit summary: {commit.summary}\n')
