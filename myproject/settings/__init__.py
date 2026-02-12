import os

ENVIRONMENT = os.getenv('DJANGO_ENV', 'local').lower()
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
