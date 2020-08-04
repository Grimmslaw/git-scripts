[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![PyPi Version](http://img.shields.io/pypi/v/git-scripts.svg)](https://pypi.org/project/git-scripts/) 

# git-scripts

This project is a collection of scripts that increase the functionality of git commands.

## Installation
To install git-scripts, in your terminal, type:
`pip install git-scripts`

## Scripts
* `rust-ver`: a script that reads a Rust project's Cargo.toml file to find its (semantic-versioned) version number,
increments the number, and adds any unstaged/untracked files in the working directory and commits them all
  * usage: `rust_ver.py [-h] [-d DIRPATH] [-l {CRITICAL,ERROR,WARN,INFO,DEBUG,NOTSET} 
    {major,minor,patch,subpatch,alpha,unalpha}]`
  * positional argument:
    * indicates the portion of the version number to be incremented; the choices are:
      * `major`
      * `minor`
      * `patch`
      * `subpatch`
      * `alpha` (alias for `subpatch`)
      * `unalpha` (doesn't increment anything but removes the the subpatch \[e.g. `-alpha0`\] suffix)
  * `-h` (`--help`): display the script's usage information
  * `-d` (`--dir`): use this flag and follow it with a directory path to indicate a git repository directory that is
  different from the current working directory
  * `-l` (`--log-level`): use this flag to set the lowest level of logs to actually log to the console; in decending
  order of strictness, these are the choices:
    * `critical`
    * `error`
    * `warn`
    * `info` (default)
    * `debug`
    * `notset`
  * Examples:
    * `rust-ver major -l debug`
      * assuming the project's version was `1.2.3-alpha2`, the script would update that to `2.0.0` and commit that
      change and anything else in the index
    *  `rust-ver unalpha -d ../some-project`
      * assuming that the project's version was `2.0.1-alpha1` and the current working directory is anything except
      `some-project`, the script would look into `some-project`, update the version to `2.0.1` and commit that change
      and anything else in the index
