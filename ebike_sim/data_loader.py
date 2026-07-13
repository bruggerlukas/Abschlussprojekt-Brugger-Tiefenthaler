"""
Einlesen und Prüfen der GPS-Daten.
"""

import logging

import pandas as pd


class GPSDataLoader:
    """
    Lädt die GPS-Daten aus einer CSV-Datei.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.logger = logging.getLogger(__name__)

    def load_data(self):
        """
        Liest die CSV-Datei ein.
        """

        self.logger.info("GPS-Daten werden eingelesen.")

        try:
            # Die bereitgestellte CSV-Datei verwendet einen Strichpunkt
            self.data = pd.read_csv(self.file_path, sep=";")

        except FileNotFoundError:
            self.logger.error("Die GPS-Datei wurde nicht gefunden.")
            raise

        self.check_columns()
        self.prepare_data()

        self.logger.info(
            "GPS-Daten wurden erfolgreich eingelesen. Anzahl Datenpunkte: %s",
            len(self.data)
        )

        return self.data

    def check_columns(self):

        required_columns = ["lat", "lon", "ele", "time"]

        for column in required_columns:
            if column not in self.data.columns:
                raise ValueError(
                    "Die benötigte Spalte '" + column + "' fehlt."
                )

