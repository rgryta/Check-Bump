"""
This module contains the methods for the regex check bump.
"""

import re
import sys
import shlex
import logging
import argparse
import subprocess

from ..git import git_deepen
from ..path import get_file_path, get_repo_file
from ..exit_codes import ExitCode

logger = logging.getLogger(__name__)


def argparser(subparsers: argparse._SubParsersAction) -> None:  # pragma: no cover
    """
    Create argparse subparser for toml method
    """
    parser = subparsers.add_parser("regex", help="Regex file parsing")
    parser.add_argument("-p", "--path", type=str, default="pyproject.toml", help="Path to file that manages versions")
    parser.add_argument(
        "-r",
        "--regex",
        type=str,
        default=r".*(\d+\.\d+\.\d+).*",
        help="Regex to capture version within file",
    )


def _get_version(file_content: str, args: argparse.Namespace) -> str:
    """
    Get version from toml file
    """
    match = re.match(args.regex, file_content, flags=re.DOTALL)
    if not match:
        logger.error("Version not found in file")
        sys.exit(2)
    return match.group(1)


def check(args):
    """
    Check bump with regex method
    """
    file_path = get_file_path(args.path)

    # New version  # pylint:disable=R0801
    with open(file_path, encoding="utf-8") as file:
        current_version = _get_version(file.read(), args)

    # Old version
    rel_path = get_repo_file(file_path)
    try:
        git_deepen(depth=1)
        result = subprocess.run(shlex.split(f"git show HEAD^:{rel_path}"), capture_output=True, check=True)
    except subprocess.CalledProcessError as exc:
        logger.error(f"{exc.stdout=}")
        logger.error(f"{exc.stderr=}")
        sys.exit(ExitCode.GIT_ERROR.value)

    old_version = _get_version(result.stdout.decode().strip(), args)

    # Check
    if old_version != current_version:
        sys.stdout.write(current_version)
        sys.exit(ExitCode.BUMP.value)
    logger.info(f"Version was not bumped: [{current_version}]")
    sys.exit(ExitCode.NO_BUMP.value)
