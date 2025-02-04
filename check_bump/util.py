"""
Utility functions
"""

import os
import sys
import time
import logging
import functools

logger = logging.getLogger(__name__)


def with_lockfile(path: str, retries: int = 3, sleep: int = 3):
    """
    Wraps a function with a given lockfile - ensure that multiple
    processes don't execute the same thing at the same time.
    """

    def inner(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if os.name in ["posix", "nt"]:
                retry_count = retries if retries > 0 else 1
                for _ in range(retry_count):
                    try:
                        os.open(path, os.O_CREAT | os.O_EXCL)
                        break
                    except FileExistsError:
                        logging.warning(f"File {path} already exists, retrying...")
                        time.sleep(sleep)
                    except IOError as exc:
                        logging.error(f"Error when trying to create a lockfile: {exc}.")
                        sys.exit(4)
                else:
                    sys.exit(5)

            try:
                return func(*args, **kwargs)
            except BaseException as exc:  # This works even if you do sys.exit(CUSTOM_CODE)
                raise exc
            finally:
                os.remove(path)

        return wrapper

    return inner
