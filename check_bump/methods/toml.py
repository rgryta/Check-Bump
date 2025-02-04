"""
This module contains the methods for the toml file format.
"""

import sys
import shlex
import logging
import argparse
import subprocess

import tomlkit
from jsonpath_ng import parse

from ..git import git_deepen
from ..path import get_file_path, get_repo_file
from ..exit_codes import ExitCode

logger = logging.getLogger(__name__)


def argparser(subparsers: argparse._SubParsersAction) -> None:  # pragma: no cover
    """
    Create argparse subparser for toml method
    """
    parser = subparsers.add_parser("toml", help="Parsing toml file")
    parser.add_argument(
        "-p", "--path", type=str, default="pyproject.toml", help="Path to toml file that manages versions"
    )
    parser.add_argument(
        "-j",
        "--jsonpath",
        type=str,
        default="$.project.version",
        help="Path to version in toml file <- jsonpath format",
    )


def _get_version(file_content: str, args: argparse.Namespace) -> str:
    """
    Get version from toml file
    """
    jsonpath_expr = parse(args.jsonpath)
    toml = tomlkit.parse(file_content)
    match = jsonpath_expr.find(toml)
    return match[0].value


def check(args: argparse.Namespace):  # pragma: no cover
    """
    Check bump for toml method
    """
    file_path = get_file_path(args.path)

    if str(file_path.parts[-1]) != "pyproject.toml":
        logger.warning(f"Not a pyproject.toml file: {file_path}")

    # New version
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
