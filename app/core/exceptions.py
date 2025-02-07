"""Utility functions for handling exceptions with logging.

This module provides functions for raising HTTP exceptions with logging capabilities.

Functions:
- raise_with_log: Wrapper function for logging and raising HTTP exceptions.
- runner_info: Retrieve information about the caller of a function.
"""

import inspect
from fastapi.exceptions import HTTPException

from app.core.logger import get_logger
logger = get_logger(__name__)

def raise_with_log(status_code: int, detail: str) -> None:
    """
    Wrapper function for logging and raising exceptions.

    Parameters:
    - status_code (int): The HTTP status code of the exception.
    - detail (str): A detailed message describing the exception.

    Raises:
    - HTTPException: An HTTP exception with the specified status code and detail message.
    """

    desc = f"<HTTPException status_code={status_code} detail={detail}>"
    logger.info(f"{desc} | runner={runner_info()}")
    raise HTTPException(status_code, detail)

def runner_info() -> str:
    """
    Retrieve information about the caller of the function.

    Returns:
    - str: A    string containing information about the caller's filename,
                function name, and line number.
    """
    info = inspect.getframeinfo(inspect.stack()[2][0])
    return f"{info.filename}:{info.function}:{info.lineno}"
