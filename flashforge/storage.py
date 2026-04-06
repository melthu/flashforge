import json
from pathlib import Path
from flashforge.models import Deck

STORAGE_DIR = Path.home() / ".flashforge"


def _ensure_dir() -> Path:
    STORAGE_DIR.mkdir(exist_ok=True)
    return STORAGE_DIR


def save_deck(deck: Deck) -> None:
    path = _ensure_dir() / f"{deck.name}.json"
    path.write_text(json.dumps(deck.to_dict(), indent=2), encoding="utf-8")


def load_deck(name: str) -> Deck:
    path = _ensure_dir() / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"No deck named '{name}' found in {STORAGE_DIR}")
    data = json.loads(path.read_text(encoding="utf-8"))
    return Deck.from_dict(data)


def list_decks() -> list[Deck]:
    _ensure_dir()
    decks = []
    for path in sorted(STORAGE_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            decks.append(Deck.from_dict(data))
        except Exception as e:
            print(f"Warning: could not load {path.name}: {e}")
    return decks
