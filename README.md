# Student Expense Tracker (Python)

**Course:** Computational Thinking and Programming (2026CSAE100), Bennett University
**Group:** ByteBudgeters

| Member | Enrollment No. |
|---|---|
| Sri Charan Banda | S26CSEU0332 |
| Padala Sai Naga Teja Reddy | S26CSEU0341 |
| Amrit Jain | S26CSEU0323 |
| Md Obaidullah Ansari | S26CSEU0348 |

A menu-driven, text-based program that helps students record daily expenses, see
category-wise totals, and compare spending against a monthly budget. Data is saved
in a local JSON file and reloaded on the next run.

## Features
- Add an expense (date, amount, category, description) with input validation
- View all expenses in a table, sorted by date
- Monthly summary: total, category-wise totals, remaining budget, warnings
- Set / update monthly budget
- Automatic saving to `expenses.json`; loaded again at start-up
- Handles invalid, negative and non-numeric input without crashing

## How to run
Requires Python 3.8 or newer. No external libraries.

```bash
python expense_tracker.py
```

To try it with sample data, copy `sample_expenses.json` to `expenses.json` first.

## Run the tests
```bash
python -m unittest discover tests -v
```

## Project structure
```
expense_tracker.py        main program
tests/                    unit tests (15 tests)
sample_expenses.json      example data
sample_output/            recorded sample sessions
docs/                     flowchart, viva preparation
```

## Python concepts used
Variables and data types, input/output, conditionals, loops, lists and dictionaries,
functions, file handling (JSON), exception handling.

## Limitations
No bank/UPI integration, no cloud or multi-user support, no receipt scanning.
Accuracy depends on what the user enters.
