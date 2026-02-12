import os

ENVIRONMENT = os.getenv('DJANGO_ENV', 'local').lower()
use_sqlite_env = os.getenv('USE_SQLITE')
USE_SQLITE = (
    use_sqlite_env.lower() in ('1', 'true', 'yes', 'on')
    if use_sqlite_env is not None
    else ENVIRONMENT != 'production'
)

if not USE_SQLITE:
    try:
        import pymysql
    except ImportError as exc:
        raise ImportError(
            "pymysql is required for MySQL. Install it or set USE_SQLITE=1."
        ) from exc
    pymysql.install_as_MySQLdb()
