import random


def deal_card(ranks="23456789JQKA", suits="SDCH"):
    return random.choice(ranks) + random.choice(suits)
