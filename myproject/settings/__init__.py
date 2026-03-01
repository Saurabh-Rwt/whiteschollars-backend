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


custom_env_file = os.getenv("DJANGO_ENV_FILE", "").strip()
if custom_env_file:
    custom_path = Path(custom_env_file).expanduser()
    if not custom_path.is_absolute():
        custom_path = BASE_DIR / custom_path
    _load_env_file(custom_path)

_load_env_file(BASE_DIR / ".env.production")
_load_env_file(BASE_DIR / ".env")

from .base import *  # noqa: F401,F403
