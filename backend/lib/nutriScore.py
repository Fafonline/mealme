import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_factor(nutriscore):
    nutriscore_factors = {"A": 1, "B": 0.75, "C": 0.5, "D": 0.25, "E": 0.125}
    return nutriscore_factors[nutriscore]
