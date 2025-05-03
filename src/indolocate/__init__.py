# Project       : indolocate
# File          : __init__.py

# Imports 
import logging
from .algorithms import init
from .app import locator

# Macros
LOG_LEVEL = logging.INFO
LOG_FORMAT = '[Indolocate] %(levelname)s - %(message)s'

# Global Settings
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

__all__ = ['utils', 'analyze']
