import numpy as np
from etats_environement_commun import EtatEnvironement
import pandas as pd


class Detailant():
    def __init__(self, etat_env: EtatEnvironement, week, idx):
        """
        * make_decision
        * compute_unfulfiled..
        * get_reward
        * update_qtable
        """
        self.idx_detailant = idx
        self.current_week = week
        self.etat_env = etat_env
        self.q_table = np.full((4*4*4,4),0)
        
        # constants
        self.MAX_inventory_qte = 60
        self.holding_cost = 5
        self.non_fulfilement_cost = 10
        self.order_cost = 2
        # current things => state (on_hand_inventory, qte_not_fulfilled, customer_demand_in_current_week) (0,1,2,3) for each one
        self.on_hand_inventory = 50
        self.qte_not_fulfilled = 0
        self.customer_demand_in_current_week = 30
        self.current_reward = 0

        self.order_to_warehouse = 0

        self.shipement_from_warehouse = self.etat_env.shipement_warehouse_to_detailants[self.idx_detailant]

        # next things
        self.next_on_hand_inventory = 0
        self.next_qte_not_fulfilled = 0

    def make_decision(self):
        # building what's the current state 
        state = [0,0,0]
        if self.on_hand_inventory <= 0:
            state[0] = 0
        elif 0 < self.on_hand_inventory <= 20:
            state[0] = 1
        elif 20 < self.on_hand_inventory <= 40:
            state[0] = 2
        elif 40 < self.on_hand_inventory <= 60:
            state[0] = 3
        
        if self.qte_not_fulfilled <= 0:
            state[1] = 0
        elif 0 < self.qte_not_fulfilled <= 20:
            state[1] = 1
        elif 20 < self.qte_not_fulfilled <= 40:
            state[1] = 2
        elif 40 < self.qte_not_fulfilled <= 60:
            state[1] = 3

        if self.customer_demand_in_current_week <= 0:
            state[2] = 0
        elif 0 < self.customer_demand_in_current_week <= 20:
            state[2] = 1
        elif 20 < self.customer_demand_in_current_week <= 40:
            state[2] = 2
        elif 40 < self.customer_demand_in_current_week <= 60:
            state[2] = 3

        # now we have the state, let's get the row idx
        row_idx = (state[0] * (4**2)) + (state[1] * (4**1)) + (state[2] * (4**0))

        action_idx = np.argmax(self.q_table[row_idx:])
        # action idx is the same as what it is (0 : none , 1 : low ...)

        # make the order based on action 
        if action_idx == 0:
            self.order_to_warehouse = 0
        elif action_idx == 1:
            self.order_to_warehouse = 20
        elif action_idx == 2:
            self.order_to_warehouse = 40
        elif action_idx == 3:
            self.order_to_warehouse = 60
        
        # send order to warehouse
        self.etat_env.qte_ordered_from_detaillants_to_warehouse.append(self.order_to_warehouse)


    def compute_unfulfiled_demand(self):
        self.next_on_hand_inventory = self.on_hand_inventory + self.shipement_from_warehouse - self.customer_demand_in_current_week

        if self.on_hand_inventory < self.customer_demand_in_current_week:
            self.next_qte_not_fulfilled = self.qte_not_fulfilled + (self.customer_demand_in_current_week - self.on_hand_inventory)
        else:
            self.next_qte_not_fulfilled = self.qte_not_fulfilled

    def get_reward(self):
        v_holding = self.holding_cost * self.on_hand_inventory
        v_non_fulfilement = self.non_fulfilement_cost * self.qte_not_fulfilled
        v_ordering = self.order_to_warehouse * self.order_cost

        r = -(v_holding + v_non_fulfilement + v_ordering)
        self.current_reward = r

    def update_q_table(self):
        pass