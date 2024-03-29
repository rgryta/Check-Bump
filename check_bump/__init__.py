"""
Check Bump Version

Command that verifies if version in pyproject.toml file was bumped
"""

import os
import sys
import shlex
import logging
import pathlib
import argparse
import subprocess
from pathlib import Path

import tomlkit

logger = logging.getLogger(__name__)


def _is_git_present() -> bool:  # pragma: no cover
    """
    Check if git is installed
    """
    try:
        subprocess.run(shlex.split("git --version"), capture_output=True, check=True)
    except subprocess.CalledProcessError:
        return False
    return True


def _is_git_repo() -> bool:  # pragma: no cover
    """
    Check if current directory is a git repository
    """
    try:
        result = subprocess.run(shlex.split("git rev-parse --is-inside-work-tree"), capture_output=True, check=True)
    except subprocess.CalledProcessError:
        return False
    return result.stdout.decode().strip() == "true"


def _git_repo_path() -> Path:  # pragma: no cover
    """
    Get path to git repository
    """
    result = subprocess.run(shlex.split("git rev-parse --show-toplevel"), capture_output=True, check=True)
    return pathlib.Path(result.stdout.decode().strip())


def _parse_args() -> argparse.Namespace:  # pragma: no cover
    parser = argparse.ArgumentParser(description="Detect and retrieve version bump")
    parser.add_argument("-p", "--path", nargs=1, type=str, help="path to pyproject.toml file")
    args = parser.parse_args()
    return args


def main():  # pragma: no cover # pylint: disable=too-many-branches
    """
    Checking if version was bumped in pyproject.toml file in last git commit
    """
    if not _is_git_present():
        logger.error("Git is not installed")
        sys.exit(1)

    file_name = "pyproject.toml"

    curr_path = pathlib.Path(os.getcwd())

    # Parse arguments
    args = _parse_args()
    if args.path:
        file_path = pathlib.Path(args.path[0])
        if not file_path.is_absolute():
            file_path = curr_path / file_path
    else:
        file_path = curr_path / file_name

    # Check if file exists under path and if it is a `pyproject.toml` file
    if not file_path.exists():
        logger.error(f"File or directory does not exist: {file_path}")
        sys.exit(1)

    if not file_path.is_file():
        if file_path.is_dir() and (new_path := file_path / file_name).is_file():
            file_path = new_path
            logger.info(f"Provided path is a directory, using {file_path}")
        else:
            logger.error(f"[{file_path}] is not a path to `pyproject.toml`")
            sys.exit(1)

    if not str(file_path.parts[-1]).endswith(file_name):
        logger.error(f"Not a pyproject.toml file: {file_path}")
        sys.exit(1)

    if file_path.parent != curr_path:
        logger.info(f"Temporarily changing directory to {file_path.parent}")
        os.chdir(file_path.parent)
    base_path = _git_repo_path()

    if not _is_git_repo():
        logger.error("Not a git repository")
        sys.exit(1)

    # New version
    with open(file_path, encoding="utf-8") as file:
        current_version = tomlkit.parse(file.read())["project"]["version"]

    # Old version
    rel_path = os.path.relpath(file_path, start=base_path)
    try:
        subprocess.run(shlex.split("git fetch --deepen=1"), capture_output=True, check=True)
        result = subprocess.run(shlex.split(f"git show HEAD^:{rel_path}"), capture_output=True, check=True)
    except subprocess.CalledProcessError as exc:
        logger.error(f"{exc.stdout=}")
        logger.error(f"{exc.stderr=}")
        raise exc
    old_version = tomlkit.parse(result.stdout.decode().strip())["project"]["version"]

    # Check
    if old_version != current_version:
        sys.stdout.write(current_version)
        sys.exit(0)
    logger.info(f"Version was not bumped: [{current_version}]")
    sys.exit(1)
