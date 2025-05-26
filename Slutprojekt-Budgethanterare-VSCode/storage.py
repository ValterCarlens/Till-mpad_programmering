import json
import os
from models import Budget

'''
storage.py: Hanterar lagring och hämtning av budgetar via JSON-filen

__author__  = "Valter Carlens"
__version__ = "1.0.0"
__email__   = "valter.carlens@elev.ga.ntig.se"
'''
# Ladda budgets från en JSON-fil och returnera en lista av Budget objekt
def load_budgets(filename="budgets.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
            return [Budget.from_dict(budget_data) for budget_data in data]
    return []

#Spara en lista av Budget objekt till en JSON-fil
def save_budgets(budgets, filename="budgets.json"):
    with open(filename, "w") as f:
        json.dump([budget.to_dict() for budget in budgets], f, indent=4) 