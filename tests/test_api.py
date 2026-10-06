def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert "model_version" in r.json()
    assert r.json()['path'] == 'artifacts/model.joblib'

def test_ready(client):
    assert client.get("/ready").status_code == 200


def test_empty(client):
    r = client.post('/v1/predict', json={})
    assert r.status_code == 422

def test_garbage(client, test_row):
    r = client.post('/v1/predict', json={**test_row, 'unknown_garbage_field': 'value'})
    assert r.status_code == 422


def test_missing_column(client, test_row):
    test_row = dict(test_row)
    del test_row['n_cores']
    r = client.post("/v1/predict", json=test_row)
    assert r.status_code == 422
