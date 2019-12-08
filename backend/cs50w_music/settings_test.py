"""Settings for testing. Disable api rate limiting."""

from .settings import *
REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = {}
REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {}