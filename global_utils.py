"""
This file handles global python utilities :)
"""
import os
import warnings

from dotenv import load_dotenv

# Load my .env file :)
load_dotenv()


def get_debug_mode() -> bool:
    """
    Get the env variable for debug mode to see if it should be enabled.

    :return: weather debug should be on :)
    """
    debug_mode = os.environ.get('DEBUG_MODE', None)
    if debug_mode is None: # Writing false for readability for my 1 braincell
        warnings.warn("Debug mode environment variable not detected, defaulting to false.")
        return False

    if debug_mode.lower() == 'true':
        warnings.warn("Debug mode is enabled. DO NOT ENABLE DEBUG MODE IN PROD IM BEGGING.")
        return True

    if debug_mode.lower() == 'false':
        return False

    warnings.warn("Debug mode environment variable does not state 'true' or 'false.' Defaulting to false.")
    return False