import tkinter as tk
from tkinter import ttk, messagebox

# This function opens a window to view and edit a specific budget's details
# It allows the user to add income streams, expenses, and view a summary
# root: the main Tkinter root window
# budget: the Budget object to view/edit
# budgets: the list of all budgets (for saving)
# save_budgets_callback: function to call to save the budgets list

def open_budget_window(root, budget, budgets, save_budgets_callback):
    # Create a new window for the selected budget
    budget_window = tk.Toplevel(root)
    budget_window.title(f"Budget: {budget.name}")
    budget_window.geometry("800x600")

    # Use a notebook (tabbed interface) for Income, Expenses, and Summary
    notebook = ttk.Notebook(budget_window)
    notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # --- Income Tab ---
    income_frame = ttk.Frame(notebook)
    notebook.add(income_frame, text="Income")

    # Function to add a new income stream to the budget (now opens a popup)
    def add_income():
        popup = tk.Toplevel(budget_window)
        popup.title("Add Income Stream")
        tk.Label(popup, text="Source:").grid(row=0, column=0, pady=5, padx=5)
        source_entry = tk.Entry(popup)
        source_entry.grid(row=0, column=1, pady=5, padx=5)
        tk.Label(popup, text="Amount:").grid(row=1, column=0, pady=5, padx=5)
        amount_entry = tk.Entry(popup)
        amount_entry.grid(row=1, column=1, pady=5, padx=5)
        tk.Label(popup, text="Frequency:").grid(row=2, column=0, pady=5, padx=5)
        frequency_var = tk.StringVar(value="Monthly")
        frequency_combo = ttk.Combobox(popup, textvariable=frequency_var, values=["One-time", "Weekly", "Monthly", "Yearly"])
        frequency_combo.grid(row=2, column=1, pady=5, padx=5)
        def save_income():
            try:
                source = source_entry.get()
                amount_str = amount_entry.get()
                if not source or not amount_str:
                    messagebox.showerror("Error", "Please enter both source and amount.", parent=popup)
                    return
                amount = float(amount_str)
                frequency = frequency_var.get()
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be greater than 0.", parent=popup)
                    return
                income_stream = {"source": source, "amount": amount, "frequency": frequency}
                budget.income_streams.append(income_stream)
                save_budgets_callback(budgets)
                income_tree.insert("", tk.END, values=(source, f"${amount:.2f}", frequency))
                update_summary()
                popup.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for amount.", parent=popup)
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=popup)
        tk.Button(popup, text="Save", command=save_income).grid(row=3, column=0, columnspan=2, pady=10)

    # Place the income list and buttons only
    income_list_frame = ttk.Frame(income_frame)
    income_list_frame.grid(row=0, column=0, columnspan=2, pady=10)
    columns = ("Source", "Amount", "Frequency")
    income_tree = ttk.Treeview(income_list_frame, columns=columns, show="headings", height=10)
    for col in columns:
        income_tree.heading(col, text=col)
        income_tree.column(col, width=150)
    income_scrollbar = ttk.Scrollbar(income_list_frame, orient=tk.VERTICAL, command=income_tree.yview)
    income_tree.configure(yscrollcommand=income_scrollbar.set)
    income_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    income_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    add_income_btn = ttk.Button(income_frame, text="Add Income", command=add_income)
    add_income_btn.grid(row=1, column=0, columnspan=2, pady=10)

    # Function to edit a selected income stream
    def edit_income():
        selected = income_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an income stream to edit.")
            return
        item = income_tree.item(selected[0])
        values = item["values"]
        # Find the index in the budget list
        for idx, stream in enumerate(budget.income_streams):
            if (stream["source"] == values[0] and
                f"${stream['amount']:.2f}" == values[1] and
                stream["frequency"] == values[2]):
                break
        else:
            messagebox.showerror("Error", "Could not find the selected income stream.")
            return
        # Popup for editing
        edit_win = tk.Toplevel(budget_window)
        edit_win.title("Edit Income Stream")
        tk.Label(edit_win, text="Source:").grid(row=0, column=0)
        src_entry = tk.Entry(edit_win)
        src_entry.insert(0, budget.income_streams[idx]["source"])
        src_entry.grid(row=0, column=1)
        tk.Label(edit_win, text="Amount:").grid(row=1, column=0)
        amt_entry = tk.Entry(edit_win)
        amt_entry.insert(0, str(budget.income_streams[idx]["amount"]))
        amt_entry.grid(row=1, column=1)
        tk.Label(edit_win, text="Frequency:").grid(row=2, column=0)
        freq_var = tk.StringVar(value=budget.income_streams[idx]["frequency"])
        freq_combo = ttk.Combobox(edit_win, textvariable=freq_var, values=["One-time", "Weekly", "Monthly", "Yearly"])
        freq_combo.grid(row=2, column=1)
        def save_edit():
            try:
                new_src = src_entry.get()
                new_amt = float(amt_entry.get())
                new_freq = freq_var.get()
                if not new_src or new_amt <= 0:
                    raise ValueError("Please enter valid values")
                budget.income_streams[idx] = {"source": new_src, "amount": new_amt, "frequency": new_freq}
                save_budgets_callback(budgets)
                # Refresh tree
                for i in income_tree.get_children():
                    income_tree.delete(i)
                for income in budget.income_streams:
                    income_tree.insert("", tk.END, values=(income["source"], f"${income['amount']:.2f}", income["frequency"]))
                update_summary()
                edit_win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        tk.Button(edit_win, text="Save", command=save_edit).grid(row=3, column=0, columnspan=2)

    edit_income_btn = ttk.Button(income_frame, text="Edit Selected", command=edit_income)
    edit_income_btn.grid(row=2, column=0, columnspan=2, pady=5)

    # --- Expenses Tab ---
    expenses_frame = ttk.Frame(notebook)
    notebook.add(expenses_frame, text="Expenses")
    # Form to add a new expense
    ttk.Label(expenses_frame, text="Add Expense", font=("Helvetica", 12)).grid(row=0, column=0, columnspan=2, pady=10)
    ttk.Label(expenses_frame, text="Category:").grid(row=1, column=0, pady=5, padx=5)
    category_entry = ttk.Entry(expenses_frame)
    category_entry.grid(row=1, column=1, pady=5, padx=5)
    ttk.Label(expenses_frame, text="Amount:").grid(row=2, column=0, pady=5, padx=5)
    expense_amount_entry = ttk.Entry(expenses_frame)
    expense_amount_entry.grid(row=2, column=1, pady=5, padx=5)
    ttk.Label(expenses_frame, text="Frequency:").grid(row=3, column=0, pady=5, padx=5)
    expense_frequency_var = tk.StringVar(value="Monthly")
    expense_frequency_combo = ttk.Combobox(expenses_frame, textvariable=expense_frequency_var, values=["One-time", "Weekly", "Monthly", "Yearly"])
    expense_frequency_combo.grid(row=3, column=1, pady=5, padx=5)
    # List of expenses
    expenses_list_frame = ttk.Frame(expenses_frame)
    expenses_list_frame.grid(row=4, column=0, columnspan=2, pady=10)
    columns = ("Category", "Amount", "Frequency")
    expenses_tree = ttk.Treeview(expenses_list_frame, columns=columns, show="headings", height=10)
    for col in columns:
        expenses_tree.heading(col, text=col)
        expenses_tree.column(col, width=150)
    expenses_scrollbar = ttk.Scrollbar(expenses_list_frame, orient=tk.VERTICAL, command=expenses_tree.yview)
    expenses_tree.configure(yscrollcommand=expenses_scrollbar.set)
    expenses_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    expenses_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Function to add a new expense to the budget
    def add_expense():
        try:
            category = category_entry.get()
            amount_str = expense_amount_entry.get()
            if not category or not amount_str:
                messagebox.showerror("Error", "Please enter both category and amount.")
                return
            amount = float(amount_str)
            frequency = expense_frequency_var.get()
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0.")
                return
            expense = {"category": category, "amount": amount, "frequency": frequency}
            budget.expenses.append(expense)
            save_budgets_callback(budgets)
            expenses_tree.insert("", tk.END, values=(category, f"${amount:.2f}", frequency))
            category_entry.delete(0, tk.END)
            expense_amount_entry.delete(0, tk.END)
            expense_frequency_var.set("Monthly")
            update_summary()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for amount.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Function to edit a selected expense
    def edit_expense():
        selected = expenses_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an expense to edit.")
            return
        item = expenses_tree.item(selected[0])
        values = item["values"]
        for idx, exp in enumerate(budget.expenses):
            if (exp["category"] == values[0] and
                f"${exp['amount']:.2f}" == values[1] and
                exp["frequency"] == values[2]):
                break
        else:
            messagebox.showerror("Error", "Could not find the selected expense.")
            return
        edit_win = tk.Toplevel(budget_window)
        edit_win.title("Edit Expense")
        tk.Label(edit_win, text="Category:").grid(row=0, column=0)
        cat_entry = tk.Entry(edit_win)
        cat_entry.insert(0, budget.expenses[idx]["category"])
        cat_entry.grid(row=0, column=1)
        tk.Label(edit_win, text="Amount:").grid(row=1, column=0)
        amt_entry = tk.Entry(edit_win)
        amt_entry.insert(0, str(budget.expenses[idx]["amount"]))
        amt_entry.grid(row=1, column=1)
        tk.Label(edit_win, text="Frequency:").grid(row=2, column=0)
        freq_var = tk.StringVar(value=budget.expenses[idx]["frequency"])
        freq_combo = ttk.Combobox(edit_win, textvariable=freq_var, values=["One-time", "Weekly", "Monthly", "Yearly"])
        freq_combo.grid(row=2, column=1)
        def save_edit():
            try:
                new_cat = cat_entry.get()
                new_amt = float(amt_entry.get())
                new_freq = freq_var.get()
                if not new_cat or new_amt <= 0:
                    raise ValueError("Please enter valid values")
                budget.expenses[idx] = {"category": new_cat, "amount": new_amt, "frequency": new_freq}
                save_budgets_callback(budgets)
                for i in expenses_tree.get_children():
                    expenses_tree.delete(i)
                for expense in budget.expenses:
                    expenses_tree.insert("", tk.END, values=(expense["category"], f"${expense['amount']:.2f}", expense["frequency"]))
                update_summary()
                edit_win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        tk.Button(edit_win, text="Save", command=save_edit).grid(row=3, column=0, columnspan=2)

    add_expense_btn = ttk.Button(expenses_frame, text="Add Expense", command=add_expense)
    add_expense_btn.grid(row=5, column=0, columnspan=2, pady=10)
    edit_expense_btn = ttk.Button(expenses_frame, text="Edit Selected", command=edit_expense)
    edit_expense_btn.grid(row=6, column=0, columnspan=2, pady=5)

    # --- Summary Tab ---
    summary_frame = ttk.Frame(notebook)
    notebook.add(summary_frame, text="Summary")
    # Labels to show summary information
    ttk.Label(summary_frame, text="Budget Summary", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=20)
    total_income_label = ttk.Label(summary_frame, text="Total Monthly Income: $0.00")
    total_income_label.grid(row=1, column=0, columnspan=2, pady=10)
    total_expenses_label = ttk.Label(summary_frame, text="Total Monthly Expenses: $0.00")
    total_expenses_label.grid(row=2, column=0, columnspan=2, pady=10)
    net_income_label = ttk.Label(summary_frame, text="Net Monthly Income: $0.00")
    net_income_label.grid(row=3, column=0, columnspan=2, pady=10)
    saving_goal_label = ttk.Label(summary_frame, text=f"Saving Goal: ${budget.saving_goal:.2f}")
    saving_goal_label.grid(row=4, column=0, columnspan=2, pady=10)
    target_date_label = ttk.Label(summary_frame, text=f"Target Date: {budget.target_date}")
    target_date_label.grid(row=5, column=0, columnspan=2, pady=10)

    # Helper function to convert different frequencies to a monthly value
    def calculate_monthly_amount(amount, frequency):
        if frequency == "One-time":
            return amount / 12
        elif frequency == "Weekly":
            return amount * 52 / 12
        elif frequency == "Monthly":
            return amount
        elif frequency == "Yearly":
            return amount / 12
        return 0

    # Update the summary labels based on current incomes and expenses
    def update_summary():
        total_monthly_income = sum(
            calculate_monthly_amount(stream["amount"], stream["frequency"])
            for stream in budget.income_streams
        )
        total_monthly_expenses = sum(
            calculate_monthly_amount(expense["amount"], expense["frequency"])
            for expense in budget.expenses
        )
        net_monthly_income = total_monthly_income - total_monthly_expenses
        total_income_label.config(text=f"Total Monthly Income: ${total_monthly_income:.2f}")
        total_expenses_label.config(text=f"Total Monthly Expenses: ${total_monthly_expenses:.2f}")
        net_income_label.config(text=f"Net Monthly Income: ${net_monthly_income:.2f}")

    # Populate the income and expense lists with existing data
    for income in budget.income_streams:
        income_tree.insert("", tk.END, values=(
            income["source"],
            f"${income['amount']:.2f}",
            income["frequency"]
        ))
    for expense in budget.expenses:
        expenses_tree.insert("", tk.END, values=(
            expense["category"],
            f"${expense['amount']:.2f}",
            expense["frequency"]
        ))
    update_summary() 