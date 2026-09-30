import pytest
from fastapi.testclient import TestClient

from mobile_price.service.app import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def test_row():
    return {
  "battery_power": 1043,
  "blue": 1,
  "clock_speed": 1.8,
  "dual_sim": 1,
  "fc": 14,
  "four_g": 0,
  "int_memory": 5,
  "m_dep": 0.1,
  "mobile_wt": 193,
  "n_cores": 3,
  "pc": 16,
  "px_height": 226,
  "px_width": 1412,
  "ram": 3476,
  "sc_h": 12,
  "sc_w": 7,
  "talk_time": 2,
  "three_g": 0,
  "touch_screen": 1,
  "wifi": 0
}

