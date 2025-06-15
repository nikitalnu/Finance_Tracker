from core.transaction import TransactionFactory
from core.observer import Subject, Logger, Analytics
from core.database import DatabaseHandler

class FinanceManager:
    def __init__(self, db_path="data/finance.db"):
        self.subject = Subject()
        self.logger = Logger()
        self.analytics = Analytics()

        self.subject.attach(self.logger)
        self.subject.attach(self.analytics)

        self.db = DatabaseHandler(db_path)

        # Повідомляємо аналітику про всі існуючі транзакції
        for transaction in self.db.load_transactions():
            self.subject.notify(transaction)

    def close(self):
        self.db.close()

    def add_transaction(self, transaction_type, amount, category, date, description):
        transaction = TransactionFactory.create_transaction(
            transaction_type, amount, category, date, description
        )

        self.db.save_transaction(transaction)
        self.subject.notify(transaction)
        return transaction

    def get_balance(self):
        income = self.analytics.total_income
        expense = self.analytics.total_expense
        return income - expense

    def get_all_transactions(self):
        return self.db.load_transactions()

    def get_summary(self):
        return self.analytics.summary()

    def delete_transaction_by_id(self, transaction_id):
        self.db.delete_transaction(transaction_id)
        # Після видалення треба оновити аналітику:
        self.analytics.total_income = 0
        self.analytics.total_expense = 0
        for transaction in self.db.load_transactions():
            self.subject.notify(transaction)
