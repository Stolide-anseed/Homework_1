def test_determinizm(client, test_row):
    s1 = client.post('/v1/predict', json=test_row).json()['mobile_price']
    s2 = client.post('/v1/predict', json=test_row).json()['mobile_price']
    assert s1 == s2
