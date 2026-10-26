
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


def build_database_url(
    *,
    username: str,
    password: str,
    host: str,
    port: int,
    database_name: str,
) -> URL:
    """Build a PostgreSQL connection URL for a company's database."""

    return URL.create(
        drivername="postgresql+psycopg",
        username=username,
        password=password,
        host=host,
        port=port,
        database=database_name,
    )


def test_company_connection(
    *,
    username: str,
    password: str,
    host: str,
    port: int,
    database_name: str,
) -> bool:
    """Check whether a company's PostgreSQL database is reachable."""

    database_url = build_database_url(
        username=username,
        password=password,
        host=host,
        port=port,
        database_name=database_name,
    )

    engine = create_engine(
        database_url,
        pool_pre_ping=True,
        pool_size=1,
        max_overflow=0,
        pool_timeout=5,
        connect_args={"connect_timeout": 5},
    )

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    finally:
        engine.dispose()
