import tkinter as tk
from tkinter import ttk, messagebox
from models import Budget
from storage import load_budgets, save_budgets
from ui_budget import open_budget_window

'''
ui_main.py: Denna fil hanterar huvudfönstret och huvudmenyn för budgethanteraren

__author__  = "Valter Carlens"
__version__ = "1.0.0"
__email__   = "valter.carlens@elev.ga.ntig.se"
'''

# Klass för att hantera huvudfönstret och menyn
class BudgetManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Manager")
        self.root.geometry("800x600")
        self.budgets = load_budgets() # Ladda befintliga budgetar från JSON-filen
        self.setup_main_menu()

    def setup_main_menu(self):
        # Rensa befintliga fönster och skapa huvudmenyn
        for widget in self.root.winfo_children():
            widget.destroy()
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        title_label = ttk.Label(main_frame, text="Budget Manager", font=("Helvetica", 24))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        new_budget_btn = ttk.Button(main_frame, text="Create New Budget", command=self.create_new_budget)
        new_budget_btn.grid(row=1, column=0, pady=10, padx=10)
        open_budget_btn = ttk.Button(main_frame, text="Open Existing Budget", command=self.show_budget_list)
        open_budget_btn.grid(row=1, column=1, pady=10, padx=10)

    def create_new_budget(self):
        # Öppna fönstret för att skapa en ny budget
        new_window = tk.Toplevel(self.root)
        new_window.title("Create New Budget")
        new_window.geometry("600x800")
        form_frame = ttk.Frame(new_window, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)
        # Formulär för allt innehåll i budgeten
        ttk.Label(form_frame, text="Basic Information", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Label(form_frame, text="Budget Name:").grid(row=1, column=0, pady=5, padx=5)
        name_entry = ttk.Entry(form_frame)
        name_entry.grid(row=1, column=1, pady=5, padx=5)
        ttk.Label(form_frame, text="Description:").grid(row=2, column=0, pady=5, padx=5)
        desc_entry = ttk.Entry(form_frame)
        desc_entry.grid(row=2, column=1, pady=5, padx=5)
        ttk.Label(form_frame, text="Saving Goal:").grid(row=3, column=0, pady=5, padx=5)
        goal_entry = ttk.Entry(form_frame)
        goal_entry.grid(row=3, column=1, pady=5, padx=5)
        ttk.Label(form_frame, text="Target Date (YYYY-MM-DD):").grid(row=4, column=0, pady=5, padx=5)
        date_entry = ttk.Entry(form_frame)
        date_entry.grid(row=4, column=1, pady=5, padx=5)
        # Checkboxes för alla olika sorters jobb
        ttk.Label(form_frame, text="Common Income Sources", font=("Helvetica", 12, "bold")).grid(row=5, column=0, columnspan=2, pady=10)
        income_sources = [
            "Full-time Job",
            "Part-time Job",
            "Freelance Work",
            "Investments",
            "Side Business",
            "Other"
        ]
        income_vars = {}
        for i, source in enumerate(income_sources):
            var = tk.BooleanVar()
            income_vars[source] = var
            ttk.Checkbutton(form_frame, text=source, variable=var).grid(row=6+i, column=0, columnspan=2, sticky="w", padx=20)
        # Checkboxes för alla olika sorters utgifter
        ttk.Label(form_frame, text="Common Expenses", font=("Helvetica", 12, "bold")).grid(row=13, column=0, columnspan=2, pady=10)
        expense_categories = [
            "Rent/Mortgage",
            "Utilities",
            "Groceries",
            "Transportation",
            "Entertainment",
            "Healthcare",
            "Education",
            "Shopping",
            "Other"
        ]
        expense_vars = {}
        for i, category in enumerate(expense_categories):
            var = tk.BooleanVar()
            expense_vars[category] = var
            ttk.Checkbutton(form_frame, text=category, variable=var).grid(row=14+i, column=0, columnspan=2, sticky="w", padx=20)

        def save_budget():
            try:
                # Skapa ett nytt budget objekt med användarens svar från formuläret
                budget = Budget(
                    name_entry.get(),
                    desc_entry.get(),
                    float(goal_entry.get()),
                    date_entry.get()
                )
                # Lägg till inkomstkällor
                for source, var in income_vars.items():
                    if var.get():
                        budget.income_streams.append({
                            "source": source,
                            "amount": 0.0,
                            "frequency": "Monthly"
                        })
                # Lägg till utgifter
                for category, var in expense_vars.items():
                    if var.get():
                        budget.expenses.append({
                            "category": category,
                            "amount": 0.0,
                            "frequency": "Monthly"
                        })
                # Lägg till den nya budgeten i JSON-filen för alla budgets och spara den
                self.budgets.append(budget)
                save_budgets(self.budgets)
                new_window.destroy()
                self.setup_main_menu()
                messagebox.showinfo("Success", "Budget created successfully!")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid values for all fields")
        save_btn = ttk.Button(form_frame, text="Save Budget", command=save_budget)
        save_btn.grid(row=24, column=0, columnspan=2, pady=20)

    # Öppna fönstret för att visa alla befintliga budgetar
    def show_budget_list(self):
        list_window = tk.Toplevel(self.root)
        list_window.title("Existing Budgets")
        list_window.geometry("600x400")
        search_frame = ttk.Frame(list_window)
        search_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        search_entry = ttk.Entry(search_frame)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        columns = ("Name", "Creation Date", "Description")
        tree = ttk.Treeview(list_window, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.grid(row=1, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(list_window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky="ns")
        list_window.grid_rowconfigure(1, weight=1)
        list_window.grid_columnconfigure(0, weight=1)
        # Fyll i Treeview(Hierarkisk lista) med befintliga budgetar
        for budget in sorted(self.budgets, key=lambda x: x.name):
            tree.insert("", tk.END, values=(
                budget.name,
                budget.creation_date,
                budget.description
            ))
        # Funktion för att söka i budgetar
        def search_budgets(event=None):
            search_term = search_entry.get().lower()
            tree.delete(*tree.get_children())
            for budget in sorted(self.budgets, key=lambda x: x.name):
                if (search_term in budget.name.lower() or 
                    search_term in budget.description.lower()):
                    tree.insert("", tk.END, values=(
                        budget.name,
                        budget.creation_date,
                        budget.description
                    ))
        search_entry.bind("<KeyRelease>", search_budgets)

        # Funktion för att öppna den valda budgeten
        def open_selected_budget():
            selected_item = tree.selection()
            if selected_item:
                budget_name = tree.item(selected_item[0])["values"][0]
                budget = next((b for b in self.budgets if b.name == budget_name), None)
                if budget:
                    open_budget_window(self.root, budget, self.budgets, save_budgets)

        # Funktion för att ta bort den valda budgeten
        def delete_selected_budget():
            selected_item = tree.selection()
            if selected_item:
                budget_name = tree.item(selected_item[0])["values"][0]
                if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the budget '{budget_name}'?"):
                    self.budgets = [b for b in self.budgets if b.name != budget_name]
                    save_budgets(self.budgets)
                    tree.delete(selected_item)
                    messagebox.showinfo("Success", "Budget deleted successfully!")
        # Knappar för att öppna eller ta bort den valda budgeten
        button_frame = ttk.Frame(list_window)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        open_btn = ttk.Button(button_frame, text="Open Selected Budget", command=open_selected_budget)
        open_btn.pack(side=tk.LEFT, padx=5)
        delete_btn = ttk.Button(button_frame, text="Delete Selected Budget", command=delete_selected_budget)
        delete_btn.pack(side=tk.LEFT, padx=5) 