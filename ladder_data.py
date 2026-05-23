import json
import copy
from pathlib import Path

_CONFIG_PATH = Path.home() / ".gel_caption_ladders.json"

_BUILTIN = {
    "ladders": {
        "100bp DNA": [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1200, 1517],
        "1kb DNA":   [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0],
        "Protein":   [10, 15, 20, 25, 37, 50, 75, 100, 150, 250],
    },
    "units": {
        "100bp DNA": "bp",
        "1kb DNA":   "kb",
        "Protein":   "kDa",
    },
}

# Mutable module-level dicts — modified in-place so all importers see updates
LADDERS: dict[str, list] = {}
LADDER_UNITS: dict[str, str] = {}


def _load():
    # Always start from builtin so builtin ladders are always up-to-date
    LADDERS.update(copy.deepcopy(_BUILTIN["ladders"]))
    LADDER_UNITS.update(copy.deepcopy(_BUILTIN["units"]))
    if _CONFIG_PATH.exists():
        try:
            data = json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))
            l = data.get("ladders", {})
            u = data.get("units", {})
            # Merge only user-added (non-builtin) ladders from config
            for name in l:
                if name not in _BUILTIN["ladders"]:
                    LADDERS[name] = l[name]
                    LADDER_UNITS[name] = u.get(name, "bp")
        except Exception:
            pass


def save_ladders():
    _CONFIG_PATH.write_text(
        json.dumps({"ladders": LADDERS, "units": LADDER_UNITS},
                   ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


_load()
