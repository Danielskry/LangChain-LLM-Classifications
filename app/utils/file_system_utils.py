"""
Utility functions for file system operations.

This module provides utility functions related to file system operations, including the 
creation of directories while ensuring security (e.g., against directory traversal attacks).
"""
import os

from app.core.logger import get_logger
logger = get_logger(__name__)

def create_directory(base_path : str, directory_name : str) -> None:
    """
    Create a directory at the specified path if it does not already exist.

    Parameters:
    - base_path (str): The base path where the directory should be created.
    - directory_name (str): The name of the directory to be created.

    Raises:
    - RuntimeError: If there is an issue creating the directory.

    Note:
    If the directory already exists, the function takes no action.

    Example:
    >>> create_directory('/path/to', 'new_directory')
    Directory '/path/to/new_directory' created successfully.
    """
    try:
        directory_path = os.path.join(base_path, directory_name)

        # Ensure the resulting path is within the specified base path
        if not os.path.abspath(directory_path).startswith(os.path.abspath(base_path)):
            raise ValueError("Invalid directory path. Directory traversal detected.")

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            logger.info("Directory %s created successfully.", directory_path)
        else:
            pass  # Directory already exists
    except Exception as e:
        raise RuntimeError(f"Failed to create directory {directory_path}: {e}") from e
