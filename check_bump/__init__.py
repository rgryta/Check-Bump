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

from tomlkit import parse

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
    parser.add_argument("--path", type=str, help="Path to pyproject.toml file")
    args = parser.parse_args()
    return args


def main():  # pragma: no cover
    """
    Checking if version was bumped in pyproject.toml file in last git commit
    """
    if not _is_git_present():
        sys.stderr.write("Git is not installed\n")
        sys.exit(1)

    file_name = "pyproject.toml"

    curr_path = pathlib.Path(os.getcwd())

    args = _parse_args()
    if args.path:
        file_path = pathlib.Path(args.path)
        if not file_path.is_absolute():
            file_path = curr_path / file_path
    else:
        file_path = curr_path / file_name

    if not file_path.exists():
        sys.stderr.write(f"File does not exist: {file_path}\n")
        sys.exit(1)

    if not str(file_path.parts[-1]).endswith(file_name):
        sys.stderr.write(f"Not a pyproject.toml file: {file_path}\n")
        sys.exit(1)

    if not file_path.is_file():
        sys.stderr.write(f"Not a file: {file_path}\n")
        sys.exit(1)

    if file_path.parent != curr_path:
        sys.stderr.write(f"Temporarily changing directory to {file_path.parent}\n")
        os.chdir(file_path.parent)
    base_path = _git_repo_path()

    if not _is_git_repo():
        sys.stderr.write("Not a git repository\n")
        sys.exit(1)

    # New version
    with open(file_path, encoding="utf-8") as file:
        current_version = parse(file.read())["project"]["version"]

    # Old version
    rel_path = os.path.relpath(file_path, start=base_path)
    try:
        subprocess.run(shlex.split("git fetch --deepen=1"), capture_output=True, check=True)
        result = subprocess.run(shlex.split(f"git show HEAD^:{rel_path}"), capture_output=True, check=True)
    except subprocess.CalledProcessError as exc:
        sys.stderr.write(f"{exc.stdout=}\n")
        sys.stderr.write(f"{exc.stderr=}\n")
        raise exc
    old_version = parse(result.stdout.decode().strip())["project"]["version"]

    # Check
    if old_version != current_version:
        sys.stdout.write(current_version)
        sys.exit(0)
    sys.exit(1)
