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
            # Die bereitgestellte CSV-Datei verwendet ein Semikolon
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
        """
        Prüft, ob alle benötigten Spalten vorhanden sind.
        """

        required_columns = ["lat", "lon", "ele", "time"]

        for column in required_columns:
            if column not in self.data.columns:
                raise ValueError(
                    "Die benötigte Spalte '" + column + "' fehlt."
                )

    def prepare_data(self):
        """
        Bereitet die Daten für die spätere Berechnung vor.
        """

        # Zeitangaben in ein Datumsformat umwandeln
        self.data["time"] = pd.to_datetime(
            self.data["time"],
            errors="coerce"
        )

        # Ungültige Zeilen entfernen
        self.data = self.data.dropna(
            subset=["lat", "lon", "ele", "time"]
        )

        # Daten nach der Zeit sortieren
        self.data = self.data.sort_values("time")

        # Index neu nummerieren
        self.data = self.data.reset_index(drop=True)