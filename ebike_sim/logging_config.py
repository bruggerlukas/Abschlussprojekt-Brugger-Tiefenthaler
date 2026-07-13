"""
Das Programm schreibt wichtige Informationen in eine Logdatei.
So kann später nachvollzogen werden, was beim Programmablauf passiert ist.
"""

import logging
import os


def setup_logging():
    """
    Richtet das Logging für das Projekt ein.
    """

    log_folder = "logs"

    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    logging.basicConfig(
        filename="logs/simulation.log",
        filemode="w",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logging.info("Logging wurde gestartet.")