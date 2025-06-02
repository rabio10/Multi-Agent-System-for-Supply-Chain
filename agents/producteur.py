from etats_environement_commun import EtatEnvironement
import numpy as np

class Producteur():
    """
    we compute the reward after each year (52 week), until we don't have previsions (we have reality of demand) and all stocks.
    workflow : 
    * next_week_decision()
    * produce()
    * prepare_shipement()
    * ... simulations of other agents ...
    * get_reward()
    * update Q table
    """
    def __init__(self, etat_env: EtatEnvironement, week):
        self.etat_env = etat_env
        self.plan_production_df = etat_env.plan_production_df
        self.current_week = week
        self.machines_health = 1
        self.proba_downtime = 0.1 # it changes depending on health
        self.health_decay = 0.995
        self.downtime_increase_rate = 1.01

        # state is (production_level, machines_status, order_from_warehouse) + global state (prevision_demande) 
        # TODO : should add to the state "order_from_warehouse" and modify the whole class 
        self.production_level = {"none":[0] , "low": [0,50] , "mid": [50, 200], "high": [200, 450]}
        self.prod_level_dict = {0:"none", 1:"low", 2:"mid", 3:"high"}
        self.machines_status_dict = {"up":1, "down":0}
        self.machine_status = 1
        # actions (production_level, repair)
        self.repaire = 0

        self.qte_prod_to_ship = -1
        self.current_production_qte = -1
        self.prod_cost = 7 # TODO: to be determined 

        # next actions
        self.next_prod_level = 1
        self.next_repaire = 0

        self.current_reward = 0
        self.q_table = np.full((8,8),0.0)
        self.rows_dict = {
            (0,0):0,
            (1,0):1,
            (2,0):2,
            (3,0):3,
            (0,1):4,
            (1,1):5,
            (2,1):6,
            (3,1):7,
        }
        self.actions_dict = {
            0:(0,0),
            1:(1,0),
            2:(2,0),
            3:(3,0),
            4:(0,1),
            5:(1,1),
            6:(2,1),
            7:(3,1),
        }

    def produce(self):
        """
        produce and updates values in current week
        """
        alpha = np.random.rand()
        if alpha < self.proba_downtime:
            # machine go down
            self.machine_status = 0
            self.current_production_qte = 0
        else :
            self.machine_status = 1
            # produce depending on action
            v = 0
            if self.next_prod_level == "none":
                v = 0
            elif self.next_prod_level == "low":
                v = np.random.choice([np.random.uniform(low=0.0, high=50), np.random.uniform(low=50.0, high=200.0), np.random.uniform(low=200.0, high=450.0)], p=[0.7, 0.2, 0.1])
            elif self.next_prod_level == "mid":
                v = np.random.choice([np.random.uniform(low=0.0, high=50), np.random.uniform(low=50.0, high=200.0), np.random.uniform(low=200.0, high=450.0)], p=[0.2, 0.7, 0.1])
            elif self.next_prod_level == "high":
                v = np.random.choice([np.random.uniform(low=0.0, high=50), np.random.uniform(low=50.0, high=200.0), np.random.uniform(low=200.0, high=450.0)], p=[0.1, 0.2, 0.7])
            self.current_production_qte = self.plan_production_df["Production", self.current_week] = v
            # machine still up, apply health decay
            decay_power = 1
            if v == 0:
                self.machines_health = self.machines_health
                self.proba_downtime = self.proba_downtime
            elif 0 < v <= 50:
                decay_power = 1
            elif 50 < v <= 200:
                decay_power = 2
            elif 200 < v <= 450:
                decay_power = 3
            self.machines_health *= self.health_decay**decay_power
            self.proba_downtime *= self.downtime_increase_rate**decay_power
            

    def prepare_shipement(self):
        # lead time : 1 week
        self.qte_prod_to_ship = self.plan_production_df["Production", self.current_week] # TODO: warehouse agent should take shipement of previous week
        self.etat_env.shipement_prod_to_warehouse = self.qte_prod_to_ship

    def next_week_decision(self):
        next_week = self.current_week + 1
        # so we know the current machine status + current prod qte
        state = self.encode_state()
        row_id = self.rows_dict[state]
        # make decision 
        indx = np.argmax(self.q_table[row_id:])
        action = self.actions_dict[indx]
        self.next_prod_level = self.prod_level_dict[action[0]]
        self.next_repaire = action[1]



    def make_plan_prod(self):
        """
        NOT USED: matan3wlch 3lih in production row , only prevision and stock
        """
        for week in range(self.current_week, 53):
            v = self.plan_production_df["Prevision", week] - self.plan_production_df["Stock", week-1]
            if v < 0:
                self.plan_production_df["Production", week] = self.production_level["none"][0]
            else:
                # decide nv prod
                if v <= self.production_level["low"][1] and v > self.production_level["low"][1]:
                    # low
                    v = np.random.choice([np.random.uniform(low=0.0, high=50), np.random.uniform(low=50.0, high=200.0), np.random.uniform(low=200.0, high=450.0)], p=[0.7, 0.2, 0.1])
                elif v <= self.production_level["mid"][1] and v > self.production_level["mid"][1]:
                    # mid
                    v = np.random.choice([np.random.uniform(low=0.0, high=50), np.random.uniform(low=50.0, high=200.0), np.random.uniform(low=200.0, high=450.0)], p=[0.2, 0.7, 0.1])
                elif v <= self.production_level["high"][1] and v > self.production_level["high"][1]:
                    # high
                    v = np.random.choice([np.random.uniform(low=0.0, high=50), np.random.uniform(low=50.0, high=200.0), np.random.uniform(low=200.0, high=450.0)], p=[0.1, 0.2, 0.7])
                # set the prod value in the week
                self.plan_production_df["Production", week] = v
            # update stock
            self.plan_production_df["Stock", week] = self.plan_production_df["Stock", week-1] - self.plan_production_df["Prevision", week] + self.plan_production_df["Production", week] 
        
        # TODO: add proba alpha of machine failure in the simulation function

    def get_reward(self):
        v_stock = self.etat_env.holding_cost * self.etat_env.qte_stock_holding_in_warehouse
        v_prod = self.current_production_qte * self.prod_cost
        v_downtime = 5
        v_non_fulfiled = self.etat_env.qte_in_transit_to_retailers * self.etat_env.transit_cost

        r = -(v_stock + v_prod + v_downtime + v_non_fulfiled)
        self.current_reward = r

    def encode_state(self):
        # state is (production_level, machines_status) + global state (prevision_demande) # TODO :: add oerder in state
        state = (0,0)
        # production_level
        v = self.current_production_qte
        if v <= 0:
            state[0] = 0
        elif v <= self.production_level["low"][1] and v > self.production_level["low"][0]:
            # low
            state[0] = 1
        elif v <= self.production_level["mid"][1] and v > self.production_level["mid"][0]:
            # mid
            state[0] = 2
        elif v <= self.production_level["high"][1] and v > self.production_level["high"][0]:
            # high
            state[0] = 3
        
        # mahcine status
        if self.machine_status == 0:
            state[1] = 0
        else:
            state[1] = 1
        
        return state

# TODO : def update_q_table()