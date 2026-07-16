"""Plot- und Kartenfunktionen für das Abschlussprojekt."""
from pathlib import Path
import logging

import matplotlib.pyplot as plt
import pandas as pd

LOGGER = logging.getLogger(__name__)


def _save_current_figure(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()

    LOGGER.info("Diagramm gespeichert: %s", path)


def plot_speed(route_data: pd.DataFrame, output_dir: str | Path) -> Path:
    path = Path(output_dir) / "speed_over_time.png"

    time_minutes = route_data["delta_time_s"].cumsum() / 60

    plt.figure(figsize=(9, 4.8))

    plt.plot(
        time_minutes,
        route_data["velocity_km_h"]
    )

    plt.xlabel("Fahrzeit / min")
    plt.ylabel("Geschwindigkeit / km/h")
    plt.title("Geschwindigkeit über die Fahrzeit")
    plt.grid(True, alpha=0.3)

    _save_current_figure(path)

    return path


def plot_power(route_data: pd.DataFrame, output_dir: str | Path) -> Path:
    path = Path(output_dir) / "power_over_time.png"

    time_minutes = route_data["delta_time_s"].cumsum() / 60

    plt.figure(figsize=(9, 4.8))

    plt.plot(
        time_minutes,
        route_data["power_w"]
    )

    plt.axhline(0, linewidth=0.8)
    plt.xlabel("Fahrzeit / min")
    plt.ylabel("Leistung / W")
    plt.title("Leistung über die Fahrzeit")
    plt.grid(True, alpha=0.3)

    _save_current_figure(path)

    return path


def plot_elevation(
    route_data: pd.DataFrame,
    output_dir: str | Path
) -> Path:
    path = Path(output_dir) / "elevation_profile.png"

    distance_km = route_data["distance_total_m"] / 1000

    plt.figure(figsize=(9, 4.8))

    plt.plot(
        distance_km,
        route_data["ele"]
    )

    plt.xlabel("Strecke / km")
    plt.ylabel("Höhe / m")
    plt.title("Höhenprofil der Fahrt")
    plt.grid(True, alpha=0.3)

    _save_current_figure(path)

    return path


def plot_soc_comparison(
    route_data: pd.DataFrame,
    output_dir: str | Path
) -> Path:
    path = Path(output_dir) / "soc_comparison.png"

    time_minutes = route_data["delta_time_s"].cumsum() / 60

    plt.figure(figsize=(9, 4.8))

    plt.plot(
        time_minutes,
        route_data["lipo_soc"] * 100,
        label="LiPo"
    )

    plt.plot(
        time_minutes,
        route_data["nmc_soc"] * 100,
        label="NMC"
    )

    plt.xlabel("Fahrzeit / min")
    plt.ylabel("Ladezustand / %")
    plt.title("Ladezustand der Akkutypen")
    plt.ylim(0, 105)
    plt.grid(True, alpha=0.3)
    plt.legend()

    _save_current_figure(path)

    return path