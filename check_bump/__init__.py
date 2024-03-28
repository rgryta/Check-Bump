"""
Check Bump Version

Command that verifies if version in pyproject.toml file was bumped
"""

import os
import sys
import shlex
import logging
import pathlib
import subprocess

from tomlkit import parse

logger = logging.getLogger(__name__)


def main():  # pragma: no cover
    """
    Checking if version was bumped in pyproject.toml file in last git commit
    """
    file_name = "pyproject.toml"

    # New version
    path = pathlib.Path(os.getcwd()) / file_name
    with open(path, encoding="utf-8") as file:
        current_version = parse(file.read())["project"]["version"]

    # Old version
    try:
        subprocess.run(shlex.split("git fetch --deepen=1"), capture_output=True, check=True)
        result = subprocess.run(shlex.split(f"git show HEAD^:{file_name}"), capture_output=True, check=True)
    except subprocess.CalledProcessError as exc:
        sys.stderr.write(f"{exc.stdout=}")
        sys.stderr.write(f"{exc.stderr=}")
        raise exc
    old_version = parse(result.stdout.decode().strip())["project"]["version"]

    # Check
    if old_version != current_version:
        sys.stdout.write(current_version)
        sys.exit(0)
    sys.exit(1)
