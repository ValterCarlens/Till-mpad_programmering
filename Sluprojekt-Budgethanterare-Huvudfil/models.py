from datetime import datetime

# Budget klass
class Budget:
    #Initiera variabler för budgeten
    def __init__(self, name, description, saving_goal, target_date):
        self.name = name
        self.description = description
        self.saving_goal = saving_goal
        self.target_date = target_date
        self.creation_date = datetime.now().strftime("%Y-%m-%d")
        self.income_streams = []
        self.expenses = []

    def to_dict(self):
        # Konverterar budget-objekt till en dictionary för att sparas som JSON
        return {
            "name": self.name,
            "description": self.description,
            "saving_goal": self.saving_goal,
            "target_date": self.target_date,
            "creation_date": self.creation_date,
            "income_streams": self.income_streams,
            "expenses": self.expenses
        }

    @classmethod
    def from_dict(cls, data):
        # Skapar ett Budget-objekt från en dictionary (för att tex ladda från JSON)
        budget = cls(
            data["name"],
            data["description"],
            data["saving_goal"],
            data["target_date"]
        )
        budget.creation_date = data["creation_date"]
        budget.income_streams = data["income_streams"]
        budget.expenses = data["expenses"]
        return budget 