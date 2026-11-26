# Viva Preparation: Student Expense Tracker

Every member must be able to explain the WHOLE program plus their own part.

## 30-second summary
"Our program is a menu-driven expense tracker. The user adds expenses with date, amount, category and description. The program validates input, shows totals by category, compares spending with a monthly budget, warns when it is reached or exceeded, and saves everything to a JSON file so data survives restarts."

## Code walkthrough (know these functions)
| Function | What it does |
|---|---|
| parse_amount | text -> positive float; raises ValueError for text, zero, negative, nan/inf |
| parse_date | validates YYYY-MM-DD with datetime.strptime; blank = today |
| resolve_category | accepts number 1-6 or name |
| make_expense | builds one record (dictionary) |
| total_spending / category_totals | sum of amounts; dictionary of category -> total |
| filter_by_month | keeps records whose date starts with "YYYY-MM" |
| budget_status | returns (remaining, message) |
| load_data / save_data | JSON file reading/writing with exception handling |
| ask | loop that repeats a prompt until the parser accepts the input |
| main | the while loop that shows the menu and calls the right function |

## Likely questions and answers
1. **Why a list of dictionaries?** Each expense has named fields (date, amount, category, description); a dictionary keeps them together and a list holds many records and is easy to loop over and save as JSON.
2. **Why JSON and not CSV?** JSON stores the budget and the expenses in one file and maps directly to Python lists/dictionaries via json.dump/json.load.
3. **How does validation work?** parse_amount calls float(); non-numeric text raises ValueError. We also raise ValueError for zero or negative values. The ask() loop catches it with try/except and asks again.
4. **Where did you use exception handling?** ValueError in input parsing; FileNotFoundError, JSONDecodeError in load_data; OSError in save_data.
5. **What if the data file is missing or corrupt?** load_data catches the error and starts with empty data instead of crashing.
6. **Why separate pure functions from input()/print()?** So they can be unit-tested without typing input. That is why we have 15 automated tests.
7. **How are category totals calculated?** Loop over the expenses; for each, `totals[cat] = totals.get(cat, 0) + amount`.
8. **What does `while True` do in main()?** Keeps the menu running until the user chooses 5, which uses `break`.
9. **When is data saved?** After every add/budget change and on exit.
10. **What happens when spending equals the budget?** remaining == 0, so a warning is shown (the proposal says "reaches or exceeds").
11. **Why round to 2 decimals?** Money values; avoids floating-point noise like 0.1 + 0.2.
12. **What are the limitations?** No edit/delete, no bank integration, single user, text interface.
13. **How would you improve it?** Edit/delete, CSV export, per-category budgets, charts, GUI.
14. **What is `with open(...)`?** Opens a file and closes it automatically even if an error occurs.
15. **What does `sorted(..., key=lambda x: x["date"])` do?** Sorts records by date; the lambda tells sorted() which field to compare.

## Demo script (2-3 minutes)
1. Run `python expense_tracker.py`. Set budget 5000.
2. Add an expense; try amount `-50` and `abc` to show validation.
3. View expenses, then show summary for the month.
4. Add a large expense to trigger the budget warning.
5. Exit, run again, and show the data has been reloaded.
6. Run `python -m unittest discover tests -v` to show the tests passing.

## Before the viva checklist
- [ ] Each member has run the program on their own laptop
- [ ] Each member can explain every function above, not only their own
- [ ] Contribution table in the report is filled in honestly
- [ ] GitHub link pasted in the report and repository is public/accessible
- [ ] LinkedIn profile updated and accessible
