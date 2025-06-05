"""
File            : indolocate/__init__.py  
Description     : Indoor localization using Wi-Fi.  
Author          : Aravind Potluri <aravindp23@iitk.ac.in>  
"""

# Imports 
import os
import logging
from .algorithms import init
from .web import webserver

# Macros
LOG_LEVEL = logging.INFO
LOG_FORMAT = '[Indolocate] %(levelname)s - %(message)s'

# Env settings
os.environ["NUMEXPR_MAX_THREADS"] = str(int(3/4 * os.cpu_count()))          # MAX threads set to 3/4 of total cores
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'                                    # Ignore tensorflow Warnings

# Global Settings
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

__all__ = ['utils', 'analysis']
