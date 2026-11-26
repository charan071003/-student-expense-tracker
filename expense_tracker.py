"""
Student Expense Tracker
Course : Computational Thinking and Programming (2026CSAE100), Bennett University
Group  : ByteBudgeters

A menu-driven, text-based program that lets a student record expenses,
view them, see category-wise totals and compare spending with a monthly budget.
Data is saved to a JSON file so it is available the next time the program runs.
"""

import json
from datetime import date, datetime

DATA_FILE = "expenses.json"
CATEGORIES = ["Food", "Transport", "Stationery", "Subscriptions", "Personal", "Other"]


# --------------------------------------------------------------------------
# Validation helpers (pure functions - no input()/print(), easy to test)
# --------------------------------------------------------------------------
def parse_amount(text):
    """Convert text to a positive float. Raises ValueError if invalid."""
    value = float(text.strip().replace(",", ""))   # ValueError if not numeric
    if value != value or value in (float("inf"), float("-inf")):
        raise ValueError("Amount must be a finite number.")
    if value <= 0:
        raise ValueError("Amount must be greater than zero.")
    return round(value, 2)


def parse_date(text):
    """Convert 'YYYY-MM-DD' text to the same normalised string. Empty = today."""
    text = text.strip()
    if text == "":
        return date.today().isoformat()
    return datetime.strptime(text, "%Y-%m-%d").date().isoformat()  # ValueError if bad


def resolve_category(text):
    """Accept a category number (1-6) or a name. Returns a category string."""
    text = text.strip()
    if text.isdigit() and 1 <= int(text) <= len(CATEGORIES):
        return CATEGORIES[int(text) - 1]
    for name in CATEGORIES:
        if name.lower() == text.lower():
            return name
    raise ValueError("Please choose a valid category.")


# --------------------------------------------------------------------------
# Core logic (pure functions)
# --------------------------------------------------------------------------
def make_expense(expense_date, amount, category, description):
    """Build one expense record (a dictionary)."""
    return {
        "date": expense_date,
        "amount": amount,
        "category": category,
        "description": description.strip() or "-",
    }


def total_spending(expenses):
    return round(sum(e["amount"] for e in expenses), 2)


def category_totals(expenses):
    """Return {category: total} for the given expenses."""
    totals = {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
    return {cat: round(val, 2) for cat, val in totals.items()}


def filter_by_month(expenses, month):
    """Keep expenses whose date starts with 'YYYY-MM'."""
    return [e for e in expenses if e["date"].startswith(month)]


def budget_status(spent, budget):
    """Return (remaining, message). budget of 0 means 'not set'."""
    if budget <= 0:
        return None, "No monthly budget set."
    remaining = round(budget - spent, 2)
    if remaining < 0:
        return remaining, f"WARNING: Budget exceeded by {money(-remaining)}!"
    if remaining == 0:
        return remaining, "WARNING: You have used your entire budget."
    if spent >= 0.8 * budget:
        return remaining, "Caution: you have used 80% or more of your budget."
    return remaining, "You are within your budget."


def money(value):
    return f"\u20b9{value:,.2f}"


# --------------------------------------------------------------------------
# File handling
# --------------------------------------------------------------------------
def load_data(filename=DATA_FILE):
    """Return (expenses, budget). Missing or corrupt file -> empty data."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        expenses = [e for e in data.get("expenses", [])
                    if {"date", "amount", "category", "description"} <= set(e)]
        budget = float(data.get("budget", 0))
        return expenses, budget
    except FileNotFoundError:
        return [], 0.0
    except (json.JSONDecodeError, ValueError, AttributeError, TypeError):
        print("Warning: data file was unreadable. Starting with empty data.")
        return [], 0.0


def save_data(expenses, budget, filename=DATA_FILE):
    """Write data to disk. Returns True on success."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({"budget": budget, "expenses": expenses}, f, indent=2)
        return True
    except OSError as err:
        print(f"Error: could not save data ({err}).")
        return False


# --------------------------------------------------------------------------
# User-interface functions (use input() and print())
# --------------------------------------------------------------------------
def ask(prompt, parser):
    """Keep asking until parser(text) succeeds."""
    while True:
        try:
            return parser(input(prompt))
        except ValueError as err:
            print(f"  Invalid input: {err}")


def show_menu():
    print("\n===== STUDENT EXPENSE TRACKER =====")
    print("1. Add expense")
    print("2. View expenses")
    print("3. Show summary")
    print("4. Set / update monthly budget")
    print("5. Exit")


def add_expense(expenses):
    print("\n--- Add Expense ---")
    exp_date = ask("Date (YYYY-MM-DD, Enter for today): ", parse_date)
    amount = ask("Amount (\u20b9): ", parse_amount)
    print("Categories: " + ", ".join(f"{i}={c}" for i, c in enumerate(CATEGORIES, 1)))
    category = ask("Category (number or name): ", resolve_category)
    description = input("Short description: ")
    expenses.append(make_expense(exp_date, amount, category, description))
    print("Expense added successfully.")


def view_expenses(expenses):
    print("\n--- All Expenses ---")
    if not expenses:
        print("No expenses recorded yet.")
        return
    print(f"{'No.':<4}{'Date':<12}{'Category':<15}{'Amount':>12}  Description")
    print("-" * 60)
    for i, e in enumerate(sorted(expenses, key=lambda x: x["date"]), 1):
        print(f"{i:<4}{e['date']:<12}{e['category']:<15}{money(e['amount']):>12}  {e['description']}")


def show_summary(expenses, budget):
    print("\n--- Summary ---")
    default_month = date.today().strftime("%Y-%m")
    month = input(f"Month to summarise (YYYY-MM, Enter for {default_month}): ").strip() or default_month
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month format. Use YYYY-MM.")
        return
    month_expenses = filter_by_month(expenses, month)
    spent = total_spending(month_expenses)
    print(f"\nMonth: {month}")
    print(f"Total recorded spending: {money(spent)}")
    if month_expenses:
        for cat, val in sorted(category_totals(month_expenses).items(), key=lambda kv: -kv[1]):
            print(f"  {cat} spending: {money(val)}")
    else:
        print("  (no expenses recorded for this month)")
    if budget > 0:
        print(f"Monthly budget: {money(budget)}")
    remaining, message = budget_status(spent, budget)
    if remaining is not None:
        print(f"Budget remaining: {money(remaining)}")
    print(message)


def set_budget(budget):
    print("\n--- Set Monthly Budget ---")
    print(f"Current budget: {money(budget) if budget else 'not set'}")
    return ask("New monthly budget (\u20b9): ", parse_amount)


def main():
    expenses, budget = load_data()
    print(f"Loaded {len(expenses)} saved expense(s).")
    while True:
        show_menu()
        choice = input("Enter choice (1-5): ").strip()
        if choice == "1":
            add_expense(expenses)
            save_data(expenses, budget)          # save after every change
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            show_summary(expenses, budget)
        elif choice == "4":
            budget = set_budget(budget)
            save_data(expenses, budget)
            print("Budget updated.")
        elif choice == "5":
            if save_data(expenses, budget):
                print("Data saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
