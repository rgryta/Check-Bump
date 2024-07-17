"""
Check bump - git module
"""

import shlex
import pathlib
import subprocess


def is_git_present() -> bool:  # pragma: no cover
    """
    Check if git is installed
    """
    try:
        subprocess.run(shlex.split("git --version"), capture_output=True, check=True)
    except subprocess.CalledProcessError:
        return False
    return True


def is_git_repo() -> bool:  # pragma: no cover
    """
    Check if current directory is a git repository
    """
    try:
        result = subprocess.run(shlex.split("git rev-parse --is-inside-work-tree"), capture_output=True, check=True)
    except subprocess.CalledProcessError:
        return False
    return result.stdout.decode().strip() == "true"


def git_repo_path() -> pathlib.Path:  # pragma: no cover
    """
    Get path to git repository
    """
    result = subprocess.run(shlex.split("git rev-parse --show-toplevel"), capture_output=True, check=True)
    return pathlib.Path(result.stdout.decode().strip())
