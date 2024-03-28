"""
Check Bump Version

Command that verifies if version in pyproject.toml file was bumped
"""

import os
import sys
import shlex
import pathlib
import subprocess

from tomlkit import parse


def main():
    file_name = "pyproject.toml"
    path = pathlib.Path(os.getcwd()) / file_name

    with open(path) as file:
        current_version = parse(file.read())["project"]["version"]

    result = subprocess.run(
        shlex.split(f"git show HEAD~1:{file_name}"), capture_output=True, check=True
    )
    old_version = parse(result.stdout.decode().strip())["project"]["version"]

    if old_version != current_version:
        print(current_version)
        sys.exit(0)
    sys.exit(1)
