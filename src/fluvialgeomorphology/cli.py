from pathlib import Path
import os
import runpy

import matplotlib


SRC_DIR = Path(__file__).resolve().parents[1]
SIM1_PATH = SRC_DIR / "1.py"
SIM2_PATH = SRC_DIR / "2.py"


def _configure_backend() -> None:
    # Prefer an interactive backend when a display is present and backend defaulted to Agg.
    has_display = bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))
    env_backend = os.environ.get("MPLBACKEND")
    current_backend = str(matplotlib.get_backend()).lower()
    if has_display and env_backend is None and current_backend == "agg":
        try:
            matplotlib.use("TkAgg", force=True)
        except Exception:
            # Keep Agg if interactive backend initialization fails.
            pass


def _run(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Simulation script not found: {path}")
    _configure_backend()
    runpy.run_path(str(path), run_name="__main__")


def sim1() -> None:
    _run(SIM1_PATH)


def sim2() -> None:
    _run(SIM2_PATH)
