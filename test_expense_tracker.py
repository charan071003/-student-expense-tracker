"""Unit tests - run with:  python -m unittest discover tests"""
import os, sys, tempfile, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import expense_tracker as et


class TestValidation(unittest.TestCase):
    def test_valid_amount(self):
        self.assertEqual(et.parse_amount("120"), 120.0)
        self.assertEqual(et.parse_amount("1,250.50"), 1250.5)

    def test_negative_and_zero_amount(self):
        for bad in ("-5", "0"):
            with self.assertRaises(ValueError):
                et.parse_amount(bad)

    def test_non_numeric_amount(self):
        for bad in ("abc", "", "12rs", "nan", "inf"):
            with self.assertRaises(ValueError):
                et.parse_amount(bad)

    def test_dates(self):
        self.assertEqual(et.parse_date("2026-10-09"), "2026-10-09")
        with self.assertRaises(ValueError):
            et.parse_date("09-10-2026")
        with self.assertRaises(ValueError):
            et.parse_date("2026-02-30")

    def test_category(self):
        self.assertEqual(et.resolve_category("1"), "Food")
        self.assertEqual(et.resolve_category("transport"), "Transport")
        with self.assertRaises(ValueError):
            et.resolve_category("9")


class TestCalculations(unittest.TestCase):
    def setUp(self):
        self.data = [
            et.make_expense("2026-10-01", 120, "Food", "Lunch"),
            et.make_expense("2026-10-02", 80, "Transport", "Metro"),
            et.make_expense("2026-10-03", 60, "Food", "Snacks"),
            et.make_expense("2026-09-15", 500, "Stationery", "Books"),
        ]

    def test_total_empty(self):
        self.assertEqual(et.total_spending([]), 0)
        self.assertEqual(et.category_totals([]), {})

    def test_total_and_categories(self):
        self.assertEqual(et.total_spending(self.data), 760)
        self.assertEqual(et.category_totals(self.data)["Food"], 180)

    def test_month_filter(self):
        self.assertEqual(len(et.filter_by_month(self.data, "2026-10")), 3)

    def test_budget_within(self):
        rem, msg = et.budget_status(120, 5000)
        self.assertEqual(rem, 4880)
        self.assertIn("within", msg)

    def test_budget_exceeded(self):
        rem, msg = et.budget_status(5200, 5000)
        self.assertEqual(rem, -200)
        self.assertIn("exceeded", msg)

    def test_budget_reached_exactly(self):
        rem, msg = et.budget_status(5000, 5000)
        self.assertEqual(rem, 0)
        self.assertIn("WARNING", msg)

    def test_budget_not_set(self):
        rem, _ = et.budget_status(100, 0)
        self.assertIsNone(rem)


class TestFileHandling(unittest.TestCase):
    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "data.json")
            exp = [et.make_expense("2026-10-09", 120, "Food", "Lunch")]
            self.assertTrue(et.save_data(exp, 5000, path))
            loaded, budget = et.load_data(path)
            self.assertEqual(loaded, exp)
            self.assertEqual(budget, 5000)

    def test_missing_file(self):
        self.assertEqual(et.load_data("does_not_exist.json"), ([], 0.0))

    def test_corrupt_file(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "bad.json")
            with open(path, "w") as f:
                f.write("{not json")
            self.assertEqual(et.load_data(path), ([], 0.0))


if __name__ == "__main__":
    unittest.main()
