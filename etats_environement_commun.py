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
        self.plan_production_df["Production", 0] = 50 # baseline prod
        self.plan_production_df["Stock", 0] = 50

        self.holding_cost = 5 # constant to be defined

        # TODO: to get it from warehouse agent
        self.qte_stock_holding_in_warehouse = 2 
        self.qte_in_transit_to_retailers = 2
        self.transit_cost = 0.2

        # comms : prod - warehouse
        self.shipement_prod_to_warehouse = -1
        self.order_warehouse_to_prod = -1

        # comms : detaillant - warehouse
        self.qte_ordered_from_detaillants_to_warehouse = [] #depends on how many retailer (it get appended)
        self.shipement_warehouse_to_detailants = [0,0] # TODO

