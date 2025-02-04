"""
Check Bump Version

Command that verifies if version in pyproject.toml file was bumped
"""

import sys
import logging
import argparse
from enum import StrEnum, auto

from . import methods
from .git import is_git_repo, git_repo_path, is_git_present
from .exit_codes import ExitCode

logger = logging.getLogger(__name__)


class VersionChecker(StrEnum):
    """
    Available version checkers
    """

    TOML = auto()
    REGEX = auto()
    TOUCH = auto()


def _parse_args() -> argparse.Namespace:  # pragma: no cover
    parser = argparse.ArgumentParser(description="Detect and retrieve version bump")

    # create the parser for the "bar" command
    subparsers = parser.add_subparsers(title="Methods", help="Different methods for parsing files", dest="method")

    methods.toml.argparser(subparsers)
    methods.regex.argparser(subparsers)
    methods.touch.argparser(subparsers)

    args = parser.parse_args()
    if not args.method:  # Default to toml
        args = parser.parse_args([VersionChecker.TOML.value])
    return args


def main():  # pragma: no cover # pylint: disable=too-many-branches
    """
    Checking if version was bumped in pyproject.toml file in last git commit
    """
    if not is_git_present():
        logger.error("Git is not installed")
        sys.exit(ExitCode.GIT_ERROR.value)

    if not is_git_repo():
        logger.error("Not a git repository")
        sys.exit(ExitCode.GIT_ERROR.value)

    # Parse arguments
    args = _parse_args()

    match args.method:
        case VersionChecker.TOML:
            methods.toml.check(args)
        case VersionChecker.REGEX:
            methods.regex.check(args)
        case VersionChecker.TOUCH:
            methods.touch.check(args)
        case _:
            logger.error("Unknown method")
            sys.exit(ExitCode.UNKNOWN_METHOD.value)
