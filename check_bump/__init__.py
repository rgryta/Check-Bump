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
    path = pathlib.Path(os.getcwd()) / file_name

    with open(path, encoding="utf-8") as file:
        current_version = parse(file.read())["project"]["version"]
    
    try:
        result = subprocess.run(shlex.split(f"git show HEAD~1:{file_name}"), capture_output=True, check=True)
    except subprocess.CalledProcessError as exc:
        logger.exception(exc)
        raise exc
    old_version = parse(result.stdout.decode().strip())["project"]["version"]

    if old_version != current_version:
        sys.stdout.write(current_version)
        sys.exit(0)
    sys.exit(1)
