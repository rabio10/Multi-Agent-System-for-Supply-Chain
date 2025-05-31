import numpy as np
from etats_environement_commun import EtatEnvironement


class Entrepot():
    def __init__(self, etat_env: EtatEnvironement):
        self.plan_prod_df = etat_env.plan_production_df
        self.prevision = self.plan_prod_df.loc["Prevision"].to_numpy()