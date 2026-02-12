import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('export '):
            line = line[len('export '):].strip()
        if '=' not in line:
            continue
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip()
        if value and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]
        os.environ.setdefault(key, value)


ENVIRONMENT = os.getenv('DJANGO_ENV', 'local').lower()
_load_env_file(BASE_DIR / f'.env.{ENVIRONMENT}')
ENVIRONMENT = os.getenv('DJANGO_ENV', ENVIRONMENT).lower()

use_sqlite_env = os.getenv('USE_SQLITE')
USE_SQLITE = (
    use_sqlite_env.lower() in ('1', 'true', 'yes', 'on')
    if use_sqlite_env is not None
    else ENVIRONMENT != 'production'
)

if USE_SQLITE:
    from .local import *  # noqa: F401,F403
else:
    from .prod import *  # noqa: F401,F403
