import pandas as pd




class EtatEnvironement():
    """
    This class will contain every state that is shared with all agents (
    the communication aspect of multi agent systems )
    * 52 semaine par an
    * mise à jour de plan de production chaque semaine
    * plan de production : 
                 0    1    2    3    4    5    6    7    8    9   ...   43   44
    Prevision    87  NaN  NaN  NaN  NaN  NaN  NaN  NaN  NaN  NaN  ...  NaN  NaN   
    Production  NaN  NaN  NaN  NaN  NaN  NaN  NaN  NaN  NaN  NaN  ...  NaN  NaN   
    Stock       NaN  NaN  NaN  NaN  NaN  NaN  NaN  NaN  NaN  NaN  ...  NaN  NaN   
    Etat System Prod (binary)
    """
    def __init__(self):
        columns = [i for i in range(53)] # semaine 0 = initial state
        rows = ["Prevision", "Production", "Stock", "Etat Systeme Prod"]
        self.plan_production_df = pd.DataFrame(index=rows, columns=columns)

