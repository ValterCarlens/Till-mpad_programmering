import json
import os
from models import Budget
from tkinter import messagebox
from datetime import datetime

# Laddar budgetar från JSON-fil och returnerar en lista med Budget-objekt
# Om filen inte existerar eller är korrupt, returneras en tom lista
def load_budgets(filename="budgets.json"):
    try:
        if os.path.exists(filename):
            with open(filename, "r") as f:
                try:
                    data = json.load(f)
                    # Validerar att data är en lista
                    if not isinstance(data, list):
                        messagebox.showerror("Fel", "Budgetdata är korrupt. Startar med tom budgetlista.")
                        return []
                    # Validerar varje budgetpost
                    valid_budgets = []
                    for budget_data in data:
                        try:
                            # Kontrollerar obligatoriska fält
                            required_fields = ["name", "description", "saving_goal", "target_date", "creation_date"]
                            if not all(field in budget_data for field in required_fields):
                                continue
                            # Kontrollerar tal
                            if not isinstance(budget_data["saving_goal"], (int, float)):
                                continue
                            # Kontrollerar datumformat
                            try:
                                datetime.strptime(budget_data["target_date"], "%Y-%m-%d")
                            except ValueError:
                                continue
                            # Skapar budgetobjekt
                            budget = Budget.from_dict(budget_data)
                            valid_budgets.append(budget)
                        except Exception:
                            continue
                    return valid_budgets
                except json.JSONDecodeError:
                    messagebox.showerror("Fel", "Budgetfilen är korrupt. Startar med tom budgetlista.")
                    return []
    except Exception as e:
        messagebox.showerror("Fel", f"Fel vid laddning av budgetar: {str(e)}")
        return []
    return []

# Sparar en lista med Budget-objekt till en JSON-fil
# Varje Budget konverteras till en dictionary innan den sparas
def save_budgets(budgets, filename="budgets.json"):
    try:
        with open(filename, "w") as f:
            json.dump([budget.to_dict() for budget in budgets], f, indent=4)
    except Exception as e:
        messagebox.showerror("Fel", f"Fel vid sparande av budgetar: {str(e)}") 