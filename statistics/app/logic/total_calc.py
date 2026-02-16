import numpy as np
import pandas as pd
from scipy.stats import poisson
import datetime

class TotalsEngine:
    def __init__(self, log_path="predictions_log.csv"):
        self.LEAGUE_AVG_PPG = 115.2
        self.log_path = log_path

    def predict_total(self, home_id, away_id, h_off, a_def, a_off, h_def, pace=1.0):
        h_exp = (h_off / self.LEAGUE_AVG_PPG) * (a_def / self.LEAGUE_AVG_PPG) * self.LEAGUE_AVG_PPG
        a_exp = (a_off / self.LEAGUE_AVG_PPG) * (h_def / self.LEAGUE_AVG_PPG) * self.LEAGUE_AVG_PPG
        
        predicted_total = (h_exp + a_exp) * pace

        new_data = {
            "timestamp": [datetime.datetime.now()],
            "matchup": [f"{away_id}@{home_id}"],
            "pred_total": [round(predicted_total, 2)],
            "prob_under_225": [round(poisson.cdf(225, predicted_total), 4)]
        }
        
        df = pd.DataFrame(new_data)
        df.to_csv(self.log_path, mode='a', header=not pd.io.common.file_exists(self.log_path), index=False)

        return {
            "total": round(predicted_total, 2),
            "home_exp": round(h_exp, 1),
            "away_exp": round(a_exp, 1)
        }
