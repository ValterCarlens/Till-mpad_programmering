import tkinter as tk
from tkinter import ttk, messagebox

'''
ui_budget.py: Denna fil hanterar UI:n för att hantera budget

__author__  = "Valter Carlens"
__version__ = "1.0.0"
__email__   = "valter.carlens@elev.ga.ntig.se"
'''

# Visar och redigerar budgetdetaljer
# root: huvudfönster
# budget: budget att visa/redigera
# budgets: alla budgetar
# save_budgets_callback: sparar budgetar
# go_back_callback: hanterar tillbaka-knapp

def open_budget_window(root, budget, budgets, save_budgets_callback, go_back_callback=None):
    # Rensar fönster och visar budget
    for widget in root.winfo_children():
        widget.destroy()
    root.title(f"Budget: {budget.name}")
    # Skapar flikgränssnitt
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Inkomstflik
    income_frame = ttk.Frame(notebook)
    notebook.add(income_frame, text="Inkomster")

    # Lägger till ny inkomst
    def add_income():
        popup = tk.Toplevel(root)
        popup.title("Lägg till inkomst")
        tk.Label(popup, text="Källa:").grid(row=0, column=0, pady=5, padx=5)
        source_entry = tk.Entry(popup)
        source_entry.grid(row=0, column=1, pady=5, padx=5)
        tk.Label(popup, text="Belopp (SEK):").grid(row=1, column=0, pady=5, padx=5)
        amount_entry = tk.Entry(popup)
        amount_entry.grid(row=1, column=1, pady=5, padx=5)
        tk.Label(popup, text="Frekvens:").grid(row=2, column=0, pady=5, padx=5)
        frequency_var = tk.StringVar(value="Månadsvis")
        frequency_combo = ttk.Combobox(popup, textvariable=frequency_var, values=["Engångs", "Veckovis", "Månadsvis", "Årligen"])
        frequency_combo.grid(row=2, column=1, pady=5, padx=5)
        def save_income():
            try:
                source = source_entry.get()
                amount_str = amount_entry.get()
                if not source or not amount_str:
                    messagebox.showerror("Fel", "Vänligen ange både källa och belopp.", parent=popup)
                    return
                amount = float(amount_str)
                frequency = frequency_var.get()
                if amount <= 0:
                    messagebox.showerror("Fel", "Beloppet måste vara större än 0.", parent=popup)
                    return
                income_stream = {"source": source, "amount": amount, "frequency": frequency}
                budget.income_streams.append(income_stream)
                save_budgets_callback(budgets)
                income_tree.insert("", tk.END, values=(source, f"{amount:.2f} SEK", frequency))
                update_summary()
                popup.destroy()
            except ValueError:
                messagebox.showerror("Fel", "Vänligen ange ett giltigt nummer för beloppet.", parent=popup)
            except Exception as e:
                messagebox.showerror("Fel", str(e), parent=popup)
        tk.Button(popup, text="Spara", command=save_income).grid(row=3, column=0, columnspan=2, pady=10)

    # Placera inkomstlistan och knappar
    income_list_frame = ttk.Frame(income_frame)
    income_list_frame.grid(row=0, column=0, columnspan=2, pady=10)
    columns = ("Källa", "Belopp", "Frekvens")
    income_tree = ttk.Treeview(income_list_frame, columns=columns, show="headings", height=10)
    for col in columns:
        income_tree.heading(col, text=col)
        income_tree.column(col, width=150)
    income_scrollbar = ttk.Scrollbar(income_list_frame, orient=tk.VERTICAL, command=income_tree.yview)
    income_tree.configure(yscrollcommand=income_scrollbar.set)
    income_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    income_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    add_income_btn = ttk.Button(income_frame, text="Lägg till inkomst", command=add_income)
    add_income_btn.grid(row=1, column=0, columnspan=2, pady=10)

    # Funktion för att redigera en inkomst
    def edit_income():
        selected = income_tree.selection()
        if not selected:
            messagebox.showerror("Fel", "Välj en inkomstström att redigera.")
            return
        item = income_tree.item(selected[0])
        values = item["values"]
        # Hitta index i budgetlistan
        for idx, stream in enumerate(budget.income_streams):
            if (stream["source"] == values[0] and
                f"{stream['amount']:.2f} SEK" == values[1] and
                stream["frequency"] == values[2]):
                break
        else:
            messagebox.showerror("Fel", "Kunde inte hitta den valda inkomstströmmen.")
            return
        # Popup för redigering
        edit_win = tk.Toplevel(root)
        edit_win.title("Redigera inkomst")
        tk.Label(edit_win, text="Källa:").grid(row=0, column=0)
        src_entry = tk.Entry(edit_win)
        src_entry.insert(0, budget.income_streams[idx]["source"])
        src_entry.grid(row=0, column=1)
        tk.Label(edit_win, text="Belopp (SEK):").grid(row=1, column=0)
        amt_entry = tk.Entry(edit_win)
        amt_entry.insert(0, str(budget.income_streams[idx]["amount"]))
        amt_entry.grid(row=1, column=1)
        tk.Label(edit_win, text="Frekvens:").grid(row=2, column=0)
        freq_var = tk.StringVar(value=budget.income_streams[idx]["frequency"])
        freq_combo = ttk.Combobox(edit_win, textvariable=freq_var, values=["Engångs", "Veckovis", "Månadsvis", "Årligen"])
        freq_combo.grid(row=2, column=1)
        #Sparar ändringar
        def save_edit():
            try:
                new_src = src_entry.get()
                new_amt = float(amt_entry.get())
                new_freq = freq_var.get()
                if not new_src or new_amt <= 0:
                    raise ValueError("Vänligen ange giltiga värden")
                budget.income_streams[idx] = {"source": new_src, "amount": new_amt, "frequency": new_freq}
                save_budgets_callback(budgets)
                # Uppdatera träd
                for i in income_tree.get_children():
                    income_tree.delete(i)
                for income in budget.income_streams:
                    income_tree.insert("", tk.END, values=(income["source"], f"{income['amount']:.2f} SEK", income["frequency"]))
                update_summary()
                edit_win.destroy()
            except Exception as e:
                messagebox.showerror("Fel", str(e))
        tk.Button(edit_win, text="Spara", command=save_edit).grid(row=3, column=0, columnspan=2)

    edit_income_btn = ttk.Button(income_frame, text="Redigera vald", command=edit_income)
    edit_income_btn.grid(row=2, column=0, columnspan=2, pady=5)

    # Utgiftsflik
    expenses_frame = ttk.Frame(notebook)
    notebook.add(expenses_frame, text="Utgifter")
    # Formulär för att lägga till en ny utgift
    ttk.Label(expenses_frame, text="Lägg till utgift", font=("Helvetica", 12)).grid(row=0, column=0, columnspan=2, pady=10)
    ttk.Label(expenses_frame, text="Kategori:").grid(row=1, column=0, pady=5, padx=5)
    category_entry = ttk.Entry(expenses_frame)
    category_entry.grid(row=1, column=1, pady=5, padx=5)
    ttk.Label(expenses_frame, text="Belopp (SEK):").grid(row=2, column=0, pady=5, padx=5)
    expense_amount_entry = tk.Entry(expenses_frame)
    expense_amount_entry.grid(row=2, column=1, pady=5, padx=5)
    ttk.Label(expenses_frame, text="Frekvens:").grid(row=3, column=0, pady=5, padx=5)
    expense_frequency_var = tk.StringVar(value="Månadsvis")
    expense_frequency_combo = ttk.Combobox(expenses_frame, textvariable=expense_frequency_var, values=["Engångs", "Veckovis", "Månadsvis", "Årligen"])
    expense_frequency_combo.grid(row=3, column=1, pady=5, padx=5)
    # Lista över utgifter
    expenses_list_frame = ttk.Frame(expenses_frame)
    expenses_list_frame.grid(row=4, column=0, columnspan=2, pady=10)
    columns = ("Kategori", "Belopp", "Frekvens")
    expenses_tree = ttk.Treeview(expenses_list_frame, columns=columns, show="headings", height=10)
    for col in columns:
        expenses_tree.heading(col, text=col)
        expenses_tree.column(col, width=150)
    expenses_scrollbar = ttk.Scrollbar(expenses_list_frame, orient=tk.VERTICAL, command=expenses_tree.yview)
    expenses_tree.configure(yscrollcommand=expenses_scrollbar.set)
    expenses_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    expenses_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Funktion för att lägga till en ny utgift i budgeten
    def add_expense():
        try:
            category = category_entry.get()
            amount_str = expense_amount_entry.get()
            if not category or not amount_str:
                messagebox.showerror("Fel", "Vänligen ange både kategori och belopp.")
                return
            amount = float(amount_str)
            frequency = expense_frequency_var.get()
            if amount <= 0:
                messagebox.showerror("Fel", "Beloppet måste vara större än 0.")
                return
            expense = {"category": category, "amount": amount, "frequency": frequency}
            budget.expenses.append(expense)
            save_budgets_callback(budgets)
            expenses_tree.insert("", tk.END, values=(category, f"{amount:.2f} SEK", frequency))
            category_entry.delete(0, tk.END)
            expense_amount_entry.delete(0, tk.END)
            expense_frequency_var.set("Månadsvis")
            update_summary()
        except ValueError:
            messagebox.showerror("Fel", "Vänligen ange ett giltigt nummer för beloppet.")
        except Exception as e:
            messagebox.showerror("Fel", str(e))

    # Funktion för att redigera en vald utgift
    def edit_expense():
        selected = expenses_tree.selection()
        if not selected:
            messagebox.showerror("Fel", "Välj en utgift att redigera.")
            return
        item = expenses_tree.item(selected[0])
        values = item["values"]
        for idx, exp in enumerate(budget.expenses):
            if (exp["category"] == values[0] and
                f"{exp['amount']:.2f} SEK" == values[1] and
                exp["frequency"] == values[2]):
                break
        else:
            messagebox.showerror("Fel", "Kunde inte hitta den valda utgiften.")
            return
        edit_win = tk.Toplevel(root)
        edit_win.title("Redigera utgift")
        tk.Label(edit_win, text="Kategori:").grid(row=0, column=0)
        cat_entry = tk.Entry(edit_win)
        cat_entry.insert(0, budget.expenses[idx]["category"])
        cat_entry.grid(row=0, column=1)
        tk.Label(edit_win, text="Belopp (SEK):").grid(row=1, column=0)
        amt_entry = tk.Entry(edit_win)
        amt_entry.insert(0, str(budget.expenses[idx]["amount"]))
        amt_entry.grid(row=1, column=1)
        tk.Label(edit_win, text="Frekvens:").grid(row=2, column=0)
        freq_var = tk.StringVar(value=budget.expenses[idx]["frequency"])
        freq_combo = ttk.Combobox(edit_win, textvariable=freq_var, values=["Engångs", "Veckovis", "Månadsvis", "Årligen"])
        freq_combo.grid(row=2, column=1)
        def save_edit():
            try:
                new_cat = cat_entry.get()
                new_amt = float(amt_entry.get())
                new_freq = freq_var.get()
                if not new_cat or new_amt <= 0:
                    raise ValueError("Vänligen ange giltiga värden")
                budget.expenses[idx] = {"category": new_cat, "amount": new_amt, "frequency": new_freq}
                save_budgets_callback(budgets)
                for i in expenses_tree.get_children():
                    expenses_tree.delete(i)
                for expense in budget.expenses:
                    expenses_tree.insert("", tk.END, values=(expense["category"], f"{expense['amount']:.2f} SEK", expense["frequency"]))
                update_summary()
                edit_win.destroy()
            except Exception as e:
                messagebox.showerror("Fel", str(e))
        tk.Button(edit_win, text="Spara", command=save_edit).grid(row=3, column=0, columnspan=2)

    add_expense_btn = ttk.Button(expenses_frame, text="Lägg till utgift", command=add_expense)
    add_expense_btn.grid(row=5, column=0, columnspan=2, pady=10)
    edit_expense_btn = ttk.Button(expenses_frame, text="Redigera vald", command=edit_expense)
    edit_expense_btn.grid(row=6, column=0, columnspan=2, pady=5)

    # --- Sammanfattningsflik ---
    summary_frame = ttk.Frame(notebook)
    notebook.add(summary_frame, text="Sammanfattning")
    # Etiketter för att visa sammanfattningsinformation
    ttk.Label(summary_frame, text="Budget Sammanfattning", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=20)
    total_income_label = ttk.Label(summary_frame, text="Total månadsinkomst: 0.00 SEK")
    total_income_label.grid(row=1, column=0, columnspan=2, pady=10)
    total_expenses_label = ttk.Label(summary_frame, text="Totala månadsutgifter: 0.00 SEK")
    total_expenses_label.grid(row=2, column=0, columnspan=2, pady=10)
    net_income_label = ttk.Label(summary_frame, text="Netto månadsinkomst: 0.00 SEK")
    net_income_label.grid(row=3, column=0, columnspan=2, pady=10)
    savings_goal_label = ttk.Label(summary_frame, text=f"Sparmål: {budget.saving_goal:.2f} SEK")
    savings_goal_label.grid(row=4, column=0, columnspan=2, pady=10)
    target_date_label = ttk.Label(summary_frame, text=f"Måldatum: {budget.target_date}")
    target_date_label.grid(row=5, column=0, columnspan=2, pady=10)

    # Funktion för att beräkna månadsbelopp baserat på frekvens
    def calculate_monthly_amount(amount, frequency):
        if frequency == "Engångs":
            return amount / 12  # Dela engångsbeloppet över året
        elif frequency == "Veckovis":
            return amount * 52 / 12  # Konvertera veckobelopp till månadsbelopp
        elif frequency == "Månadsvis":
            return amount
        elif frequency == "Årligen":
            return amount / 12  # Dela årsbeloppet över året
        return 0

    # Funktion för att uppdatera sammanfattningen
    def update_summary():
        total_monthly_income = sum(calculate_monthly_amount(inc["amount"], inc["frequency"])
                                 for inc in budget.income_streams)
        total_monthly_expenses = sum(calculate_monthly_amount(exp["amount"], exp["frequency"])
                                   for exp in budget.expenses)
        net_monthly_income = total_monthly_income - total_monthly_expenses

        total_income_label.config(text=f"Total månadsinkomst: {total_monthly_income:.2f} SEK")
        total_expenses_label.config(text=f"Totala månadsutgifter: {total_monthly_expenses:.2f} SEK")
        net_income_label.config(text=f"Netto månadsinkomst: {net_monthly_income:.2f} SEK")

    # Uppdatera sammanfattningen när fönstret öppnas
    update_summary()

    # Lägg till Tillbaka-knapp
    def go_back():
        if go_back_callback:
            go_back_callback()
        else:
            root.destroy()

    back_btn = ttk.Button(root, text="Tillbaka", command=go_back)
    back_btn.pack(pady=10) 
