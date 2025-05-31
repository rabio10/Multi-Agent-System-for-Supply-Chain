import pandas as pd




class EtatEnvironement():
    """
    * 52 semaine par an
    * mise à jour de plan de production chaque semaine
    """
    def __init__(self):
        columns = [i for i in range(53)] # semaine 0 = initial state
        rows = ["Prevision", "Production", "Stock"]
        plan_production_df = pd.DataFrame(index=rows, columns=columns)

        