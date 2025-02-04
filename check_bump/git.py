"""
Check bump - git module
"""

import shlex
import pathlib
import subprocess

from .util import with_lockfile


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


def git_depth_check(depth: int = 1):
    """
    Check the depth of the git repository
    """

    result = subprocess.run(  # pylint:disable=subprocess-run-check
        shlex.split(f"git show HEAD~{depth}"), capture_output=True
    )
    if result.returncode != 0:
        return False
    return True


def git_deepen(depth: int = 1):
    """
    Deepen the git repository
    """

    depth_check = git_depth_check(depth)
    if depth_check:
        return

    @with_lockfile(path=str(git_repo_path() / ".git" / "check-bump.lock"))
    def _inner():
        try:
            subprocess.run(shlex.split(f"git fetch --deepen={depth}"), capture_output=True, check=True)
        except subprocess.CalledProcessError as exc:
            raise exc

    _inner()
