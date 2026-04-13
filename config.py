import sys
import json
from pathlib import Path


def get_base_path() -> Path:
    """Retourne le dossier racine — compatible mode dev et exe PyInstaller."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent


ROOT_DIR = get_base_path()
PROJETS_JSON = ROOT_DIR / "projets.json"
CHOIX_JSON = ROOT_DIR / "choix.json"


def charger_choix() -> dict:
    """Charge les options des listes déroulantes depuis choix.json."""
    try:
        with open(get_base_path() / "choix.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"⚠️ Impossible de charger choix.json : {e}")
        return {}
