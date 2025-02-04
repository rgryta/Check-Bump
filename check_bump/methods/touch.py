"""
This module contains the methods for the touch check bump.
"""

import sys
import shlex
import logging
import argparse
import subprocess

from ..path import get_file_path, get_repo_file
from ..exit_codes import ExitCode

logger = logging.getLogger(__name__)


def argparser(subparsers: argparse._SubParsersAction) -> None:  # pragma: no cover
    """
    Create argparse subparser for toml method
    """
    parser = subparsers.add_parser("touch", help="Touch file check")
    parser.add_argument("-p", "--path", type=str, default="pyproject.toml", help="Path to file that manages versions")


def check(args):
    """
    Check bump with touch method
    """
    file_path = get_file_path(args.path)

    # New version
    current_version = 0

    # Old version
    rel_path = get_repo_file(file_path)
    old_version = subprocess.run(
        shlex.split(f"git diff --quiet HEAD^ HEAD -- '{rel_path}'"), capture_output=True, check=False
    ).returncode

    # Check
    if old_version == current_version:
        sys.exit(ExitCode.BUMP.value)
    logger.info(f"Version was not bumped: [{current_version}]")
    sys.exit(ExitCode.NO_BUMP.value)
