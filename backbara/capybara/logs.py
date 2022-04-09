import logging

from sys import stdout

LOGGER = logging.getLogger("capylife")
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(logging.StreamHandler(stdout))
