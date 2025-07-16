import numpy as np
from logging_config import log
import datetime

from agents.detailant import Detailant
from agents.entrepot import Entrepot
from agents.producteur import Producteur
from etats_environement_commun import EtatEnvironement


# begining of the script
TODAY_DATE = datetime.datetime.now()
log.info(f"Today's date: {TODAY_DATE.strftime('%d %B %Y')}")
DATE_THRESHOLD = (TODAY_DATE - datetime.timedelta(days=2))
log.info(f"Date threshold: {DATE_THRESHOLD.strftime('%d %B %Y')}")

if __name__ == "__main__":
    log.info("--------debut simulation---------")
    log.info("52 semaine dans l'année")

    num_epoch = 5
    environement1 = EtatEnvironement()

    # initialize q tables
    log.info("initialize q tables")
    prod1_qtable = 0 # TODO
    entrp_qtable = 0
    det1_qtable = 0
    det2_qtable = 0

    for ep in range(num_epoch):
        log.info(f"--------epoch {ep}---------")
        producteur1 = Producteur(environement1,1)
        entrepot1 = Entrepot(environement1, 1)
        detailant1 = Detailant(environement1,1,0)
        detailant2 = Detailant(environement1,1,1)

        producteur1.q_table = prod1_qtable
        entrepot1.q_table = entrp_qtable
        detailant1.q_table = det1_qtable
        detailant2.q_table = det2_qtable

        for week in range(52):
            producteur1.current_week = week+1
            entrepot1.current_week = week+1
            detailant1.current_week = week+1
            detailant2.current_week = week+1
            
            # observe and select action
            producteur1.next_week_decision()
            entrepot1.make_decision()
            detailant1.make_decision()
            detailant2.make_decision()

            # run simulator
            producteur1.produce()
            producteur1.prepare_shipement()

            detailant1.compute_unfulfiled_demand()
            detailant2.compute_unfulfiled_demand()

            entrepot1.get_shipement()
            entrepot1.get_commands_from_detaillants()

            # get rewards
            producteur1.get_reward()
            detailant1.get_reward()
            detailant2.get_reward()
            entrepot1.get_reward()

            # update Q tables
            producteur1.update_q_table()
            detailant1.update_q_table()
            detailant2.update_q_table()
            entrepot1.update_q_table()
            
        
        # get the q tables to the next epoch
        prod1_qtable = producteur1.q_table
        entrp_qtable = entrepot1.q_table
        det1_qtable = detailant1.q_table
        det2_qtable = detailant2.q_table
    
    # TODO : extract optimal policy from q table of each agent