import psycopg
from psycopg.types.json import Json

from mobile_price.config import settings

DDL = """
CREATE TABLE IF NOT EXISTS predictions (

    request_id          uuid PRIMARY KEY,
    ts                  timestamptz NOT NULL DEFAULT now(),
    model_version       text NOT NULL,
    features            jsonb NOT NULL,
    mobile_price        double precision NOT NULL,
    latency_ms          real,
    status_code         integer NOT NULL
)
"""

def init() -> None:
    if not settings.database_url:
        return
    with psycopg.connect(settings.database_url) as conn:
        conn.execute(DDL)

def save_prediction(request_id : str, features : dict, mobile_price:float, model_version : str, latency_ms : float, status_code: int) -> None:
    if not settings.database_url:
        return
    with psycopg.connect(settings.database_url) as conn:
            conn.execute(
            "INSERT INTO predictions (request_id, model_version, mobile_price, features, latency_ms, status_code) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (request_id, model_version, mobile_price, Json(features), latency_ms, status_code),
        )
