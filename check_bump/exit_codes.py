"""
Error codes for check_bump
"""

from enum import Enum


class ExitCode(Enum):
    """
    Exit codes for check_bump
    """

    BUMP = 0
    NO_BUMP = 1

    VERSION_FILE_ERROR = 2
    GIT_ERROR = 3

    UNKNOWN_METHOD = 99
