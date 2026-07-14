"""Einfache Akkumodelle für LiPo und NMC."""

import logging
from math import sqrt
import numpy as np

from .config import SimulationConfig

LOGGER = logging.getLogger(__name__)