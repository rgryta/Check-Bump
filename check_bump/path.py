"""
Common path methods
"""

import os
import sys
import logging
import pathlib

from .git import git_repo_path
from .exit_codes import ExitCode

logger = logging.getLogger(__name__)


def get_file_path(path: str) -> pathlib.Path:
    """
    Get file path from provided path. If path is a directory, check for `pyproject.toml` file.
    """
    curr_path = pathlib.Path(os.getcwd())

    file_path = pathlib.Path(path)
    if not file_path.is_absolute():
        file_path = curr_path / file_path

    # Check if file exists under path and if it is a `pyproject.toml` file
    if not file_path.exists():
        logger.error(f"File or directory does not exist: {file_path}")
        sys.exit(ExitCode.VERSION_FILE_ERROR.value)

    if not file_path.is_file():
        if file_path.is_dir() and (new_path := file_path / "pyproject.toml").is_file():
            file_path = new_path
            logger.info(f"Provided path is a directory, using {file_path}")
        else:
            logger.error(f"[{file_path}] is not a path to `pyproject.toml`")
            sys.exit(ExitCode.VERSION_FILE_ERROR.value)

    if str(file_path.parts[-1]) != "pyproject.toml":
        logger.warning(f"Not a pyproject.toml file: {file_path}")
    return file_path


def get_repo_file(file_path: pathlib.Path):
    """
    Set the repository path and return the relative path to the file
    """
    base_path = git_repo_path()
    rel_path = os.path.relpath(file_path, start=base_path)
    return rel_path
