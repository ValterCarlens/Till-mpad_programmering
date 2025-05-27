import tkinter as tk
from tkinter import ttk, messagebox
from models import Budget
from storage import load_budgets, save_budgets
from ui_budget import open_budget_window
import re
from datetime import datetime

'''
ui_main.py: Denna fil hanterar huvudfönstret och huvudmenyn för budgethanteraren

__author__  = "Valter Carlens"
__version__ = "1.0.0"
__email__   = "valter.carlens@elev.ga.ntig.se"
'''

# Klass som hanterar huvudfönstret, huvudmenyn och budgetlistan
class BudgetManagerApp:
    def __init__(self, root):
        # Initierar huvudfönstret och laddar budgetar
        self.root = root
        self.root.title("Budget Manager")
        self.root.geometry("800x600")
        self.budgets = load_budgets()
        self.setup_main_menu()

    def setup_main_menu(self):
        # Rensar alla befintliga widgets och visar huvudmenyn
        for widget in self.root.winfo_children():
            widget.destroy()
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        title_label = ttk.Label(main_frame, text="Budget Manager", font=("Helvetica", 24))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        # Skapa ny budget-knapp
        new_budget_btn = ttk.Button(main_frame, text="Skapa ny budget", command=self.create_new_budget)
        new_budget_btn.grid(row=1, column=0, pady=10, padx=10)
        # Öppna befintlig budget-knapp
        open_budget_btn = ttk.Button(main_frame, text="Öppna befintlig budget", command=self.show_budget_list)
        open_budget_btn.grid(row=1, column=1, pady=10, padx=10)
        # Avsluta-knapp för att stänga programmet
        exit_btn = ttk.Button(main_frame, text="Avsluta", command=self.root.quit)
        exit_btn.grid(row=2, column=0, columnspan=2, pady=30)

    def create_new_budget(self):
        # Visar formuläret för att skapa ny budget i huvudfönstret
        for widget in self.root.winfo_children():
            widget.destroy()
        form_frame = ttk.Frame(self.root, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)
        # Övre fält
        ttk.Label(form_frame, text="Ny Budget", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=4, pady=10)
        # Budgetnamn
        ttk.Label(form_frame, text="Budgetnamn").grid(row=1, column=0, padx=10, pady=5)
        name_entry = ttk.Entry(form_frame)
        name_entry.grid(row=2, column=0, padx=10, pady=5)
        # Beskrivning
        ttk.Label(form_frame, text="Beskrivning").grid(row=1, column=1, padx=10, pady=5)
        desc_entry = ttk.Entry(form_frame)
        desc_entry.grid(row=2, column=1, padx=10, pady=5)
        # Sparmål
        ttk.Label(form_frame, text="Sparmål (SEK)").grid(row=1, column=2, padx=10, pady=5)
        goal_entry = ttk.Entry(form_frame)
        goal_entry.grid(row=2, column=2, padx=10, pady=5)
        # Måldatum
        ttk.Label(form_frame, text="Måldatum (ÅÅÅÅ-MM-DD)").grid(row=1, column=3, padx=10, pady=5)
        date_entry = ttk.Entry(form_frame)
        date_entry.grid(row=2, column=3, padx=10, pady=5)
        # Inkomst- och utgiftstabeller
        income_label = ttk.Label(form_frame, text="Inkomstkällor", font=("Helvetica", 12, "bold"))
        income_label.grid(row=3, column=0, columnspan=2, pady=(20, 5))
        expense_label = ttk.Label(form_frame, text="Utgifter", font=("Helvetica", 12, "bold"))
        expense_label.grid(row=3, column=2, columnspan=2, pady=(20, 5))
        # Inkomsttabell
        income_tree = ttk.Treeview(form_frame, columns=("Namn", "Belopp", "Frekvens"), show="headings", height=6)
        for col in ("Namn", "Belopp", "Frekvens"):
            income_tree.heading(col, text=col)
            income_tree.column(col, width=100)
        income_tree.grid(row=4, column=0, columnspan=2, padx=10)
        # Utgiftstabell
        expense_tree = ttk.Treeview(form_frame, columns=("Namn", "Belopp", "Frekvens"), show="headings", height=6)
        for col in ("Namn", "Belopp", "Frekvens"):
            expense_tree.heading(col, text=col)
            expense_tree.column(col, width=100)
        expense_tree.grid(row=4, column=2, columnspan=2, padx=10)
        # Datalagring för ny budget
        new_incomes = []
        new_expenses = []
        # Inkomst-popup logik
        def popup_income(edit_idx=None):
            popup = tk.Toplevel(self.root)
            popup.title("Lägg till/Redigera inkomst")
            tk.Label(popup, text="Namn:").grid(row=0, column=0, padx=5, pady=5)
            name_entry_popup = tk.Entry(popup)
            name_entry_popup.grid(row=0, column=1, padx=5, pady=5)
            tk.Label(popup, text="Belopp (SEK):").grid(row=1, column=0, padx=5, pady=5)
            amount_entry_popup = tk.Entry(popup)
            amount_entry_popup.grid(row=1, column=1, padx=5, pady=5)
            tk.Label(popup, text="Frekvens:").grid(row=2, column=0, padx=5, pady=5)
            freq_var = tk.StringVar(value="Månadsvis")
            freq_combo = ttk.Combobox(popup, textvariable=freq_var, values=["Veckovis", "Månadsvis", "Årligen"])
            freq_combo.grid(row=2, column=1, padx=5, pady=5)
            # Om redigering, förifyll   
            if edit_idx is not None:
                income = new_incomes[edit_idx]
                name_entry_popup.insert(0, income["name"])
                amount_entry_popup.insert(0, str(income["amount"]))
                freq_var.set(income["frequency"])
            # Spara inkomst
            def save_income():
                name = name_entry_popup.get()
                amount_str = amount_entry_popup.get()
                freq = freq_var.get()
                if not name or not amount_str:
                    messagebox.showerror("Fel", "Vänligen ange både namn och belopp.", parent=popup)
                    return
                try:
                    amount = float(amount_str)
                except ValueError:
                    messagebox.showerror("Fel", "Beloppet måste vara ett nummer.", parent=popup)
                    return
                if amount < 0:
                    messagebox.showerror("Fel", "Beloppet måste vara positivt.", parent=popup)
                    return
                if edit_idx is not None:
                    new_incomes[edit_idx] = {"name": name, "amount": amount, "frequency": freq}
                else:
                    new_incomes.append({"name": name, "amount": amount, "frequency": freq})
                # Uppdatera tabell
                income_tree.delete(*income_tree.get_children())
                for inc in new_incomes:
                    income_tree.insert("", tk.END, values=(inc["name"], f"{inc['amount']:.2f} SEK", inc["frequency"]))
                popup.destroy()
            tk.Button(popup, text="Spara", command=save_income).grid(row=3, column=0, columnspan=2, pady=10)
        #Utgift-popup logik
        def popup_expense(edit_idx=None):
            popup = tk.Toplevel(self.root)
            popup.title("Lägg till/Redigera utgift")
            tk.Label(popup, text="Namn:").grid(row=0, column=0, padx=5, pady=5)
            name_entry_popup = tk.Entry(popup)
            name_entry_popup.grid(row=0, column=1, padx=5, pady=5)
            tk.Label(popup, text="Belopp (SEK):").grid(row=1, column=0, padx=5, pady=5)
            amount_entry_popup = tk.Entry(popup)
            amount_entry_popup.grid(row=1, column=1, padx=5, pady=5)
            tk.Label(popup, text="Frekvens:").grid(row=2, column=0, padx=5, pady=5)
            freq_var = tk.StringVar(value="Månadsvis")
            freq_combo = ttk.Combobox(popup, textvariable=freq_var, values=["Veckovis", "Månadsvis", "Årligen"])
            freq_combo.grid(row=2, column=1, padx=5, pady=5)
            # Om redigering, förifyll
            if edit_idx is not None:
                expense = new_expenses[edit_idx]
                name_entry_popup.insert(0, expense["name"])
                amount_entry_popup.insert(0, str(expense["amount"]))
                freq_var.set(expense["frequency"])
            def save_expense():
                name = name_entry_popup.get()
                amount_str = amount_entry_popup.get()
                freq = freq_var.get()
                if not name or not amount_str:
                    messagebox.showerror("Fel", "Vänligen ange både namn och belopp.", parent=popup)
                    return
                try:
                    amount = float(amount_str)
                except ValueError:
                    messagebox.showerror("Fel", "Beloppet måste vara ett nummer.", parent=popup)
                    return
                if amount < 0:
                    messagebox.showerror("Fel", "Beloppet måste vara positivt.", parent=popup)
                    return
                if edit_idx is not None:
                    new_expenses[edit_idx] = {"name": name, "amount": amount, "frequency": freq}
                else:
                    new_expenses.append({"name": name, "amount": amount, "frequency": freq})
                # Uppdatera tabell
                expense_tree.delete(*expense_tree.get_children())
                for exp in new_expenses:
                    expense_tree.insert("", tk.END, values=(exp["name"], f"{exp['amount']:.2f} SEK", exp["frequency"]))
                popup.destroy()
            tk.Button(popup, text="Spara", command=save_expense).grid(row=3, column=0, columnspan=2, pady=10)
        # Inkomstknappar
        def edit_income():
            selected = income_tree.selection()
            if not selected:
                messagebox.showerror("Fel", "Välj en inkomst att redigera.")
                return
            idx = income_tree.index(selected[0])
            popup_income(edit_idx=idx)
        def add_income():
            popup_income()
        def remove_income():
            selected = income_tree.selection()
            if not selected:
                messagebox.showerror("Fel", "Välj en inkomst att ta bort.")
                return
            idx = income_tree.index(selected[0])
            del new_incomes[idx]
            income_tree.delete(selected[0])
        ttk.Button(form_frame, text="Redigera inkomst", command=edit_income).grid(row=5, column=0, pady=5)
        ttk.Button(form_frame, text="Lägg till ny inkomst", command=add_income).grid(row=6, column=0, pady=5)
        ttk.Button(form_frame, text="Ta bort inkomst", command=remove_income).grid(row=7, column=0, pady=5)
        # Utgiftsknappar
        def edit_expense():
            selected = expense_tree.selection()
            if not selected:
                messagebox.showerror("Fel", "Välj en utgift att redigera.")
                return
            idx = expense_tree.index(selected[0])
            popup_expense(edit_idx=idx)
        def add_expense():
            popup_expense()
        def remove_expense():
            selected = expense_tree.selection()
            if not selected:
                messagebox.showerror("Fel", "Välj en utgift att ta bort.")
                return
            idx = expense_tree.index(selected[0])
            del new_expenses[idx]
            expense_tree.delete(selected[0])
        ttk.Button(form_frame, text="Redigera utgift", command=edit_expense).grid(row=5, column=2, pady=5)
        ttk.Button(form_frame, text="Lägg till ny utgift", command=add_expense).grid(row=6, column=2, pady=5)
        ttk.Button(form_frame, text="Ta bort utgift", command=remove_expense).grid(row=7, column=2, pady=5)
        # Spara och Tillbaka knappar
        def save_budget():
            try:
                # Kontrollera tomma fält
                name = name_entry.get().strip()
                description = desc_entry.get().strip()
                goal_str = goal_entry.get().strip()
                date_str = date_entry.get().strip()

                if not name:
                    messagebox.showerror("Fel", "Budgetnamn kan inte vara tomt.")
                    return
                if not description:
                    messagebox.showerror("Fel", "Beskrivning kan inte vara tom.")
                    return
                if not goal_str:
                    messagebox.showerror("Fel", "Sparmål kan inte vara tomt.")
                    return
                if not date_str:
                    messagebox.showerror("Fel", "Måldatum kan inte vara tomt.")
                    return

                # Kontrollera duplicerat budgetnamn
                if any(b.name == name for b in self.budgets):
                    messagebox.showerror("Fel", "En budget med detta namn finns redan.")
                    return

                # Validera datumformat
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
                    messagebox.showerror("Fel", "Måldatum måste vara i formatet ÅÅÅÅ-MM-DD")
                    return
                try:
                    datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Fel", "Måldatum är inte ett giltigt datum.")
                    return

                # Validera sparande
                try:
                    saving_goal = float(goal_str)
                    if saving_goal <= 0:
                        messagebox.showerror("Fel", "Sparmålet måste vara större än 0.")
                        return
                except ValueError:
                    messagebox.showerror("Fel", "Sparmålet måste vara ett nummer.")
                    return

                # Skapa ny budget
                new_budget = Budget(name, description, saving_goal, date_str)
                new_budget.income_streams = new_incomes
                new_budget.expenses = new_expenses
                self.budgets.append(new_budget)
                save_budgets(self.budgets)
                messagebox.showinfo("Framgång", "Budget skapad!")
                self.setup_main_menu()
            except Exception as e:
                messagebox.showerror("Fel", f"Ett fel uppstod: {str(e)}")

        ttk.Button(form_frame, text="Spara budget", command=save_budget).grid(row=8, column=1, pady=20)
        ttk.Button(form_frame, text="Tillbaka", command=self.setup_main_menu).grid(row=8, column=2, pady=20)

    def show_budget_list(self):
        # Visar budgetlistan i huvudfönstret
        for widget in self.root.winfo_children():
            widget.destroy()
        list_frame = ttk.Frame(self.root, padding="20")
        list_frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(list_frame, text="Välj en budget", font=("Helvetica", 16, "bold")).pack(pady=10)
        # Sökfält
        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill=tk.X, pady=10)
        ttk.Label(search_frame, text="Sök:").pack(side=tk.LEFT, padx=5)
        search_entry = ttk.Entry(search_frame)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        # Budgetlista
        tree = ttk.Treeview(list_frame, columns=("Namn", "Beskrivning", "Sparmål", "Måldatum"), show="headings")
        for col in ("Namn", "Beskrivning", "Sparmål", "Måldatum"):
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(fill=tk.BOTH, expand=True, pady=10)
        # Uppdatera listan
        def update_list():
            tree.delete(*tree.get_children())
            search_text = search_entry.get().lower()
            for budget in self.budgets:
                if (search_text in budget.name.lower() or
                    search_text in budget.description.lower()):
                    tree.insert("", tk.END, values=(
                        budget.name,
                        budget.description,
                        f"{budget.saving_goal:.2f} SEK",
                        budget.target_date
                    ))
        update_list()
        # Sökfunktion
        def search_budgets(event=None):
            update_list()
        search_entry.bind("<KeyRelease>", search_budgets)
        # Knappar
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(pady=20)
        def open_selected_budget():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Fel", "Välj en budget att öppna.")
                return
            idx = tree.index(selected[0])
            budget = self.budgets[idx]
            open_budget_window(self.root, budget, self.budgets)
        def delete_selected_budget():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Fel", "Välj en budget att ta bort.")
                return
            if messagebox.askyesno("Bekräfta", "Är du säker på att du vill ta bort denna budget?"):
                idx = tree.index(selected[0])
                del self.budgets[idx]
                save_budgets(self.budgets)
                update_list()
        ttk.Button(button_frame, text="Öppna", command=open_selected_budget).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Ta bort", command=delete_selected_budget).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Tillbaka", command=self.setup_main_menu).pack(side=tk.LEFT, padx=5) 
