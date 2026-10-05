import os

import psycopg
import pytest

DATABASE_URL = os.getenv("DATABASE_URL")

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(not DATABASE_URL, reason="нужен Postgres: задайте DATABASE_URL"),
]


def test_prediction_is_logged(client, test_row):
    body = client.post("/v1/predict", json=test_row).json()

    with psycopg.connect(DATABASE_URL) as conn:
        row = conn.execute(
            "SELECT model_version, mobile_price, features->>'blue', status_code "
            "FROM predictions WHERE request_id = %s",
            (body["request_id"],),
        ).fetchone()

    assert row is not None
    assert row[0] == body["model_version"]
    assert row[1] == pytest.approx(body["mobile_price"])
    assert row[2] == str(test_row["blue"])
    assert row[3] == 200

def test_empty_prediction_is_logged(client):
    response = client.post("/v1/predict", json={})
    assert response.status_code == 422

    request_id = response.headers["X-Request-ID"]

    with psycopg.connect(DATABASE_URL) as conn:
        row = conn.execute(
            "SELECT model_version, mobile_price, status_code "
            "FROM predictions WHERE request_id = %s",
            (request_id,),
        ).fetchone()

    assert row is not None
    assert row[0] == client.get("/health").json()["model_version"]
    assert row[1] is None
    assert row[2] == 422
