def test_predict_smoke(client, test_row):
    r = client.post("/v1/predict", json=test_row)
    assert r.status_code == 200
    body = r.json()
    assert body['status_code'] == 200
    assert 0.0 <= body["mobile_price"] <= 3.0
    assert body['latency_ms'] >= 0
    assert body['model_version']


def test_missing_value(client, test_row):
    test_row['n_cores'] = None
    r = client.post("/v1/predict", json=test_row)
    assert r.status_code == 422
