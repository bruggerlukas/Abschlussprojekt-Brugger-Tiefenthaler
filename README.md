# E-Bike-Abschlussprojekt

Python-Anwendung zur Auslegung und Simulation eines E-Bikes anhand von GPS-Daten.

Das Programm liest eine aufgezeichnete Route aus einer CSV-Datei ein. Anschließend werden wichtige Werte wie Strecke, Geschwindigkeit, Beschleunigung, Steigung, Leistung, Drehmoment und Motorstrom berechnet.

Zusätzlich wird der Ladezustand von zwei verschiedenen Akkutypen simuliert:

* LiPo-Akku
* NMC-Akku

## Projektmitglieder

* Brugger
* Tiefenthaler

## Voraussetzungen

Für das Projekt wird Python 3 benötigt.

Die benötigten Python-Pakete stehen in der Datei `requirements.txt`.

## Installation unter Windows

Zuerst den Projektordner im Terminal öffnen.

Eine virtuelle Python-Umgebung erstellen:

```powershell
python -m venv .venv
```

Die virtuelle Umgebung aktivieren:

```powershell
.venv\Scripts\activate
```

Die benötigten Pakete installieren:

```powershell
python -m pip install -r requirements.txt
```

## Installation unter macOS oder Linux

Zuerst den Projektordner im Terminal öffnen.

Eine virtuelle Python-Umgebung erstellen:

```bash
python3 -m venv .venv
```

Die virtuelle Umgebung aktivieren:

```bash
source .venv/bin/activate
```

Die benötigten Pakete installieren:

```bash
python3 -m pip install -r requirements.txt
```

## Programm starten

Unter Windows:

```powershell
python main.py
```

Unter macOS oder Linux:

```bash
python3 main.py
```

## Tests starten

Unter Windows:

```powershell
python -m pytest
```

Unter macOS oder Linux:

```bash
python3 -m pytest
```

Wenn alle bisherigen Tests erfolgreich sind, sollte ungefähr folgende Meldung erscheinen:

```text
4 passed
```

## Eingangsdaten

Die GPS-Daten befinden sich in dieser Datei:

```text
data/final_project_input_data.csv
```

Die Datei enthält unter anderem:

* Zeitstempel
* Breitengrad
* Längengrad
* Höhe
* Temperatur
