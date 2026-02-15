import numpy as np
import pandas as pd
from pydantic import BaseModel

class EloEngine:
    def __init__(self,k_factor=20,home_advantage=100):
        self.K = k_factor
        self.H = home_advantage
        self.B2B_penalty = 45
    
    def get_prediction(self,home_elo,away_elo, home_b2b=False,away_b2b=False,injury_impact=0):
        h_elo = np.array([home_elo], dtype=float)
        a_elo = np.array([away_elo], dtype=float)

        h_elo += self.H
        if home_b2b: h_elo -= self.B2B_penalty
        if away_b2b: a_elo -= self.B2B_penalty

        h_elo += injury_impact

        win_prob = 1 / (1 + np.power(10, (a_elo - h_elo) / 400))

        fair_spread = (win_prob - 0.5) * 30 

        return {
            "win_prob": float(win_prob[0]),
            "fair_spread": round(float(fair_spread[0]), 1)
        }