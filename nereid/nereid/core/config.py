import os
from pathlib import Path

from nereid.core.io import load_cfg


API_V1_STR = "/api/v1"
API_LATEST = API_V1_STR
APP_CONTEXT = load_cfg(Path(__file__).parent / "base_config.yml")

_NEREID_FORCE_FOREGROUND = os.getenv("NEREID_FORCE_FOREGROUND", "")
NEREID_FORCE_FOREGROUND = _NEREID_FORCE_FOREGROUND not in ["", "0"]
