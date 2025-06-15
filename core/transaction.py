from abc import ABC, abstractmethod
from datetime import datetime

class Transaction(ABC):
    def __init__(self, amount, category, date, description, id=None):
        self.amount = amount
        self.category = category
        self.date = date if isinstance(date, datetime) else datetime.strptime(date, '%Y-%m-%d')
        self.description = description
        self.id = id  # ← потрібен для видалення по ID

    @abstractmethod
    def get_type(self):
        pass

    def __repr__(self):
        return f"#{self.id} [{self.get_type()}] {self.date.date()} - {self.category}: {self.amount} ({self.description})"


class IncomeTransaction(Transaction):
    def get_type(self):
        return "Income"


class ExpenseTransaction(Transaction):
    def get_type(self):
        return "Expense"


class TransactionFactory:
    @staticmethod
    def create_transaction(transaction_type, amount, category, date, description):
        transaction_type = transaction_type.lower()
        if transaction_type == "income":
            return IncomeTransaction(amount, category, date, description)
        elif transaction_type == "expense":
            return ExpenseTransaction(amount, category, date, description)
        else:
            raise ValueError("Unknown transaction type")
