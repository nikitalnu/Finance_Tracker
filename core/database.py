import sqlite3
from core.transaction import IncomeTransaction, ExpenseTransaction
from datetime import datetime
import os

class DatabaseHandler:
    def __init__(self, db_path):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def close(self):
        self.conn.close()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT
            )
        ''')
        self.conn.commit()

    def save_transaction(self, transaction):
        self.cursor.execute('''
            INSERT INTO transactions (type, amount, category, date, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            transaction.get_type(),
            transaction.amount,
            transaction.category,
            transaction.date.strftime('%Y-%m-%d'),
            transaction.description
        ))
        self.conn.commit()

    def load_transactions(self):
        self.cursor.execute('SELECT id, type, amount, category, date, description FROM transactions')
        rows = self.cursor.fetchall()

        transactions = []
        for row in rows:
            id, t_type, amount, category, date_str, description = row
            if t_type.lower() == "income":
                transactions.append(IncomeTransaction(amount, category, date_str, description, id=id))
            elif t_type.lower() == "expense":
                transactions.append(ExpenseTransaction(amount, category, date_str, description, id=id))
        return transactions

    def delete_transaction(self, id):
        self.cursor.execute('DELETE FROM transactions WHERE id = ?', (id,))
        self.conn.commit()
