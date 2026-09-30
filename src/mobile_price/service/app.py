import time
import uuid
from contextlib import asynccontextmanager

import joblib
import pandas as pd
from fastapi import BackgroundTasks, FastAPI, HTTPException
from pydantic import BaseModel,Field

from mobile_price.config import settings
from mobile_price import db

# curl ‐X POST localhost:8080/v1/predict ‐H "Content‐Type: application/json" ‐d @test.json

class Features(BaseModel):
    model_config = {'extra':'forbid'}

    battery_power: int
    blue: int
    clock_speed:float
    dual_sim: int
    fc: int
    four_g: int
    int_memory:int
    m_dep: float
    mobile_wt: int
    n_cores: int
    pc:int
    px_height: int
    px_width: int
    ram: int
    sc_h: int
    sc_w: int
    talk_time: int
    three_g: int
    touch_screen: int
    wifi:int

class Prediction(BaseModel):

    mobile_price: float
    model_version:str
    request_id: str
    latency_ms: float
    status_code: int

@asynccontextmanager
async def lifespan(app: FastAPI):
    bundle = joblib.load(settings.model_path)
    app.state.pipeline = bundle['model']
    app.state.meta = bundle['metadata']
    app.state.version = bundle['metadata']['version']

    db.init()
    yield
    app.state.pipeline = None

app = FastAPI(title="Mobile Price Prediction API", version="1.0", lifespan=lifespan)

@app.get('/health')
def health():
    return {'status': 'ok', 'model_version': getattr(app.state, 'version', "unknown")}

@app.get('/ready')
def ready():
    if getattr(app.state, 'pipeline', None) is None:
        raise HTTPException(status_code=503, detail="Pipeline not loaded")

    return {'status': 'ok'}

@app.post('/v1/predict')
def predict(x: Features, bg: BackgroundTasks):
    t0 = time.perf_counter()
    request_id = str(uuid.uuid4())
    payload = x.model_dump()
    frame = pd.DataFrame([payload]).reindex(columns=app.state.meta['features'])

    mobile_price = float(app.state.pipeline.predict(frame)[0])

    latency_ms = time.perf_counter() - t0

    # Пока костыль, чтобы позже написать полноценно рабочую логику
    status_code = 200
    bg.add_task(
        db.save_prediction,
        request_id=request_id,
        features = payload,
        mobile_price = mobile_price,
        model_version = app.state.version,
        latency_ms = latency_ms,
        status_code = status_code)


    return Prediction(mobile_price=mobile_price, model_version = app.state.version, request_id=request_id, latency_ms=latency_ms, status_code = status_code)