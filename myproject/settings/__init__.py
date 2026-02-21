import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if value and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]
        os.environ.setdefault(key, value)


_raw_environment = os.getenv("DJANGO_ENV", "local").strip().lower()
ENVIRONMENT = "production" if _raw_environment in ("production", "prod") else "local"
_load_env_file(BASE_DIR / f".env.{ENVIRONMENT}")

if ENVIRONMENT == "production":
    from .prod import *  # noqa: F401,F403
else:
    from .local import *  # noqa: F401,F403
