"""
The spotON_sdk package provides tools for interacting with the spotON API.

This package includes modules for authenticating with the API, sending requests,
and processing responses. It also includes utility functions for working with
the data returned by the API.
"""

from entsoe import Area

from .constants.geography import *
from .logic.Config import *

__version__ = "0.0.1.5"
__all__ = [name for name in dir() if not name.startswith('_')]