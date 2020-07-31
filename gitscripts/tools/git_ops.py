import os, logging
from typing import List

from git import Repo, GitConfigParser, Actor, IndexFile, BaseIndexEntry, Commit

LOGGER = logging.getLogger(__name__)


def get_author() -> Actor:
    info = {}

    gitconfig = GitConfigParser(os.path.expanduser('~/.gitconfig'))
    print(f'gitconfig={gitconfig}')
    sections = gitconfig.sections()
    assert 'user' in sections
    user_items = gitconfig.items('user')
    print(f'user_items={user_items}')

    for tup in user_items:
        info[tup[0]] = tup[1]
    print(info)
    assert 'name' in info and 'email' in info

    return Actor(name=info['name'], email=info['email'])


def get_repo(repo_filepath: str = None) -> Repo:
    LOGGER.debug(f'repo_filepath={repo_filepath}')
    if repo_filepath is not None:
        repo_abspath = os.path.abspath(repo_filepath)
    else:
        cwd = os.path.abspath(os.getcwd())
        assert '.git' in os.listdir(cwd)
        repo_abspath = cwd
    return Repo(repo_abspath)


def get_head_commit(filepath: str):
    LOGGER.debug(f'filepath={filepath}')
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


def do_git_commit(message: str, dirpath: str = None):
    LOGGER.debug(f'dirpath={dirpath}')
    repo = get_repo(dirpath)
    index = repo.index

    for x in repo.index.diff('HEAD'):
        LOGGER.debug(f'x={x}')
        LOGGER.debug(f'x.new_file={x.new_file}')
        LOGGER.debug(f'x.b_path={x.b_path}')
    # unstaged_files = get_unstaged_filenames(repo)
    # LOGGER.debug(f'unstaged_files={unstaged_files}, type={type(unstaged_files)}')
    # git_add(index, unstaged_files)
    repo.git.add(update=True)
    warn_master_commit(index)
    commit = git_commit(index, message)
    print(f'\nCommit summary: {commit.summary}\n')
