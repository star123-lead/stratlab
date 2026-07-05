"""
StratLab backend.

Run from inside backend/:
    uvicorn main:app --reload
"""

from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backtest.engine import compute_metrics, run_backtest
from data.fetcher import fetch_history
from strategies import STRATEGY_REGISTRY
from strategies.metadata import STRATEGY_METADATA

from database import Base, engine, get_db
from models import User
import auth

# Create DB tables on startup if they don't exist yet.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="StratLab Backtester")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = auth.decode_access_token(token)
    if payload is None or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

    user = db.query(User).filter(User.email == payload["sub"]).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found.")

    return user


# ---------------------------------------------------------------------------
# Auth schemas + endpoints
# ---------------------------------------------------------------------------

class SignupRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@app.post("/api/signup", response_model=TokenResponse)
def signup(req: SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="An account with that email already exists.")

    if len(req.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters.")

    user = User(email=req.email, hashed_password=auth.hash_password(req.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    token = auth.create_access_token({"sub": user.email})
    return {"access_token": token}


@app.post("/api/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not auth.verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password.")

    token = auth.create_access_token({"sub": user.email})
    return {"access_token": token}


@app.get("/api/me")
def me(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email}


# ---------------------------------------------------------------------------
# Backtest endpoints (now require login)
# ---------------------------------------------------------------------------

class BacktestRequest(BaseModel):
    ticker: str
    strategy_id: str
    params: Dict[str, Any] = Field(default_factory=dict)
    start_date: str
    end_date: str
    initial_capital: float = 10000
    commission_pct: float = 0.1


@app.get("/api/strategies")
def get_strategies():
    return list(STRATEGY_METADATA.values())


@app.post("/api/backtest")
def backtest(req: BacktestRequest, current_user: User = Depends(get_current_user)):
    if req.strategy_id not in STRATEGY_REGISTRY:
        raise HTTPException(status_code=400, detail=f"Unknown strategy '{req.strategy_id}'.")

    if req.initial_capital <= 0:
        raise HTTPException(status_code=400, detail="Initial capital must be greater than zero.")

    try:
        df = fetch_history(req.ticker, req.start_date, req.end_date)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    strategy = STRATEGY_REGISTRY[req.strategy_id]
    params = req.params if req.params else STRATEGY_METADATA[req.strategy_id]["default_params"]
    signal = strategy.generate_signals(df, params)

    equity_curve, trades = run_backtest(df, signal, req.initial_capital, req.commission_pct)
    metrics = compute_metrics(equity_curve, req.initial_capital, trades)

    bh_strategy = STRATEGY_REGISTRY["buy_hold"]
    bh_signal = bh_strategy.generate_signals(df, {})
    bh_curve, bh_trades = run_backtest(df, bh_signal, req.initial_capital, req.commission_pct)
    bh_metrics = compute_metrics(bh_curve, req.initial_capital, bh_trades)

    price_data = [
        {"date": d.strftime("%Y-%m-%d"), "close": round(float(c), 2), "in_position": int(signal.loc[d])}
        for d, c in zip(df.index, df["Close"])
    ]

    return {
        "ticker": req.ticker.strip().upper(),
        "strategy_id": req.strategy_id,
        "strategy_name": STRATEGY_METADATA[req.strategy_id]["name"],
        "metrics": metrics,
        "benchmark_metrics": bh_metrics,
        "equity_curve": equity_curve,
        "benchmark_equity_curve": bh_curve,
        "price_data": price_data,
        "trades": trades,
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}