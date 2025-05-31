from etats_environement_commun import EtatEnvironement
import numpy as np

class Producteur():
    """
    we compute the reward after each year (52 week), until we don't have previsions (we have reality of demand) and all stocks
    """
    def __init__(self, etat_env: EtatEnvironement):
        self.plan_production_df = etat_env.plan_production_df
        self.current_week = 1

    def make_plan_prod(self):
        for week in range(self.current_week, 53):
            v = self.plan_production_df["Prevision", week] - self.plan_production_df["Stock", week-1]
            if v < 0:
                self.plan_production_df["Production", week] = 0
            else:
                self.plan_production_df["Production", week] = v
            # if it's negative ( there's enough stock for the demand) turn it to 0
            # update stock
            self.plan_production_df["Stock", week] = self.plan_production_df["Stock", week-1] - self.plan_production_df["Prevision", week] + self.plan_production_df["Production", week] 
