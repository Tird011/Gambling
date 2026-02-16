from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from app.logic.elo_calc import EloEngine
from app.logic.total_calc import TotalsEngine

app = FastAPI(title="NBA Quant Brain 2026")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

elo_engine = EloEngine()
total_engine = TotalsEngine()

class PredictionRequest(BaseModel):
    home_id: str
    away_id: str
    home_elo: float
    away_elo: float
    home_off_rtg: float
    away_def_rtg: float
    away_off_rtg: float
    home_def_rtg: float
    home_is_b2b: bool = False
    away_is_b2b: bool = False
    injury_impact: float = 0.0 
    pace_factor: float = 1.0

@app.post("/predict")
async def get_full_prediction(data: PredictionRequest):
    try:
        elo_results = elo_engine.get_prediction(
            home_elo=data.home_elo,
            away_elo=data.away_elo,
            home_b2b=data.home_is_b2b,
            away_b2b=data.away_is_b2b,
            injury_impact=data.injury_impact
        )

        total_results = total_engine.predict_total(
            home_id=data.home_id,
            away_id=data.away_id,
            h_off=data.home_off_rtg,
            a_def=data.away_def_rtg,
            a_off=data.away_off_rtg,
            h_def=data.home_def_rtg,
            pace=data.pace_factor
        )

        return {
            "matchup": f"{data.away_id} vs {data.home_id}",
            "probability": elo_results["win_prob"],
            "fair_spread": elo_results["fair_spread"],
            "predicted_total": total_results["total"],
            "over_under_verdict": "OVER" if total_results["total"] > 225 else "UNDER",
            "confidence_score": abs(elo_results["win_prob"] - 0.5) * 2 # 0 to 1 scale
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "online", "engine": "v1.0-Feb2026"}

