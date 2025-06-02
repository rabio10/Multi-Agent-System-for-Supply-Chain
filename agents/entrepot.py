import numpy as np
from etats_environement_commun import EtatEnvironement
import pandas as pd


class Entrepot():
    def __init__(self, etat_env: EtatEnvironement, week):
        """
        workflow : 
        * see state (stock_level, qte_level_needed)
        * take an action (shipement_level_of_fulfilement, order_to_prod)
        * execute it
        * ... other simulations...
        * compute reward
        * update Q table
        """
        self.etat_env = etat_env
        self.plan_prod_df = etat_env.plan_production_df
        self.prevision = self.plan_prod_df.loc["Prevision"].to_numpy()

        self.current_week = week
        self.qte_stock = self.plan_prod_df["Stock", week - 1]
        self.shipement_from_prod = self.plan_prod_df["Production", self.current_week-1]

        #self.qte_in_transit_to_retailer = 5 # TODO : get it from somwhere
        #self.etat_env.qte_in_transit_to_retailers = self.qte_in_transit_to_retailer
        
        self.list_cmds_from_detailants = []

        self.nbr_detailant = 2
        self.q_table = np.full((4*4, 4 * 4**(self.nbr_detailant)),0)
        self.stock_lvl_dict = {"rupture":0, "low":200, "mid":400, "high":600} # i.e. 200 < stock <= 400 : mid

        # costs
        self.shipping_cost = 0.5
        self.stockout_cost = 20

        self.current_reward = 0
    


    def make_decision(self):
        # see state
        stock_total = self.qte_stock
        total_order = sum(self.list_cmds_from_detailants)
        
        # build the state 
        state = [0,0]
        if self.qte_stock <= 0:
            state[0] = 0
        elif 0 < self.qte_stock <= 200:
            state[0] = 1
        elif 200 < self.qte_stock <= 400:
            state[0] = 2
        elif 400 < self.qte_stock <= 600:
            state[0] = 3

        if total_order <= 0:
            state[1] = 0
        elif 0 < total_order <= 200:
            state[1] = 1
        elif 200 < total_order <= 400:
            state[1] = 2
        elif 400 < total_order <= 600:
            state[1] = 3

        # now we have the state, let's get the row idx
        row_idx = (state[0] * (4**1)) + (state[1] * (4**0))

        action_idx = np.argmax(self.q_table[row_idx:])

        # build the action vect
        action = [0, 0, 0]
        action[0] = (action_idx // 4) // 4
        action[1] = (action_idx // 4) % 4
        action[2] = action_idx % 4

        # execute the action
        self.etat_env.shipement_warehouse_to_detailants[0] = self.helper_func(action[0])
        self.etat_env.shipement_warehouse_to_detailants[1] = self.helper_func(action[1])
        self.etat_env.order_warehouse_to_prod = self.helper_func(action[2]) * 10

    def helper_func(value):
        if value == 0:
            return 0
        elif value == 1:
            return np.random.choice([np.random.uniform(low=0.0, high=20), np.random.uniform(low=20.0, high=40.0), np.random.uniform(low=40.0, high=60.0)], p=[0.7, 0.2, 0.1])
        elif value == 2:
            return np.random.choice([np.random.uniform(low=0.0, high=20), np.random.uniform(low=20.0, high=40.0), np.random.uniform(low=40.0, high=60.0)], p=[0.2, 0.7, 0.1])
        elif value == 3:
            return np.random.choice([np.random.uniform(low=0.0, high=20), np.random.uniform(low=20.0, high=40.0), np.random.uniform(low=40.0, high=60.0)], p=[0.1, 0.2, 0.7])


    def get_shipement(self):
        shipement_from_prod = self.etat_env.shipement_prod_to_warehouse
        # update stock
        self.qte_stock += shipement_from_prod
        self.etat_env.qte_stock_holding_in_warehouse = self.qte_stock

    def get_commands_from_detaillants(self):
        list_cmds = self.etat_env.qte_ordered_from_detaillants_to_warehouse
        sum_cmds = sum(list_cmds)
        self.list_cmds_from_detailants = list_cmds
        
        
    def get_reward(self):
        v_holding = self.etat_env.holding_cost * self.etat_env.qte_stock_holding_in_warehouse
        v_shipping = self.shipping_cost * sum(self.etat_env.shipement_warehouse_to_detailants[0:2])
        v_stockout = self.stockout_cost * np.max([0, sum(self.list_cmds_from_detailants) - self.qte_stock])

        r = -(v_holding + v_shipping + v_stockout)
        self.current_reward = r