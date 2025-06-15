import unittest
import os
import sys
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.manager import FinanceManager
from core.transaction import TransactionFactory

class TestFinanceManager(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, "test_finance.db")
        self.manager = FinanceManager(db_path=self.db_path)

    def tearDown(self):
        self.manager.close()
        shutil.rmtree(self.test_dir)

    def test_add_income_transaction(self):
        t = self.manager.add_transaction("Income", 1000, "Salary", "2024-01-01", "January salary")
        self.assertEqual(t.amount, 1000)
        self.assertEqual(t.get_type(), "Income")

    def test_add_expense_transaction(self):
        t = self.manager.add_transaction("Expense", 200, "Food", "2024-01-01", "Groceries")
        self.assertEqual(t.amount, 200)
        self.assertEqual(t.get_type(), "Expense")

    def test_get_balance_after_income(self):
        self.manager.add_transaction("Income", 1000, "Salary", "2024-01-01", "January salary")
        self.assertEqual(self.manager.get_balance(), 1000)

    def test_get_balance_after_expense(self):
        self.manager.add_transaction("Income", 1000, "Salary", "2024-01-01", "January salary")
        self.manager.add_transaction("Expense", 300, "Rent", "2024-01-02", "Room rent")
        self.assertEqual(self.manager.get_balance(), 700)

    def test_summary_income_expense(self):
        self.manager.add_transaction("Income", 1500, "Bonus", "2024-02-01", "Performance bonus")
        self.manager.add_transaction("Expense", 500, "Utilities", "2024-02-02", "Electricity bill")
        summary = self.manager.get_summary()
        self.assertEqual(summary["income"], 1500)
        self.assertEqual(summary["expense"], 500)

    def test_get_all_transactions(self):
        self.manager.add_transaction("Income", 500, "Gift", "2024-03-01", "Birthday gift")
        self.assertEqual(len(self.manager.get_all_transactions()), 1)

    def test_transaction_repr(self):
        t = TransactionFactory.create_transaction("income", 100, "Bonus", "2024-01-01", "Extra")
        repr_str = repr(t)
        self.assertIn("[Income]", repr_str)

    def test_invalid_transaction_type(self):
        with self.assertRaises(ValueError):
            TransactionFactory.create_transaction("loan", 300, "Loan", "2024-01-01", "Bank loan")

    def test_logger_file_written(self):
        log_path = "log.txt"
        if os.path.exists(log_path):
            os.remove(log_path)
        self.manager.add_transaction("Income", 100, "Gift", "2024-01-01", "New year gift")
        with open(log_path, encoding="utf-8") as f:
            self.assertIn("Додано", f.read())

    def test_delete_transaction_by_id(self):
        self.manager.add_transaction("Expense", 100, "Test", "2024-01-01", "Test desc")
        tid = self.manager.get_all_transactions()[0].id
        self.manager.delete_transaction_by_id(tid)
        self.assertEqual(len(self.manager.get_all_transactions()), 0)

    def test_analytics_resets_after_delete(self):
        self.manager.add_transaction("Income", 500, "Job", "2024-01-01", "Work")
        self.manager.add_transaction("Expense", 100, "Food", "2024-01-02", "Pizza")
        tid = self.manager.get_all_transactions()[0].id
        self.manager.delete_transaction_by_id(tid)
        summary = self.manager.get_summary()
        self.assertGreaterEqual(summary["income"], 0)

    def test_subject_attach_and_detach(self):
        from core.observer import Logger
        subject = self.manager.subject
        logger = Logger()
        subject.attach(logger)
        self.assertIn(logger, subject._observers)
        subject.detach(logger)
        self.assertNotIn(logger, subject._observers)

    def test_transaction_date_format(self):
        t = TransactionFactory.create_transaction("Expense", 20, "Test", "2024-01-01", "Test")
        self.assertEqual(str(t.date.date()), "2024-01-01")

    def test_multiple_transactions(self):
        for i in range(5):
            self.manager.add_transaction("Income", i * 10, "Loop", "2024-01-01", f"Inc {i}")
        self.assertEqual(len(self.manager.get_all_transactions()), 5)

    def test_negative_amount(self):
        t = self.manager.add_transaction("Expense", -100, "Refund", "2024-01-01", "Incorrect refund")
        self.assertEqual(t.amount, -100)

    def test_empty_description(self):
        t = self.manager.add_transaction("Income", 200, "Unknown", "2024-01-01", "")
        self.assertEqual(t.description, "")

    def test_long_description(self):
        desc = "A" * 1000
        t = self.manager.add_transaction("Expense", 30, "Misc", "2024-01-01", desc)
        self.assertEqual(t.description, desc)

    def test_zero_amount(self):
        t = self.manager.add_transaction("Income", 0, "Zero", "2024-01-01", "Zero amount")
        self.assertEqual(t.amount, 0)

    def test_balance_no_transactions(self):
        self.assertEqual(self.manager.get_balance(), 0)

if __name__ == '__main__':
    unittest.main()
