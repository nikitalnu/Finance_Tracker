from abc import ABC, abstractmethod

# ==== Інтерфейс Observer ====
class Observer(ABC):
    @abstractmethod
    def update(self, transaction):
        pass

# ==== Клас Subject ====
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, transaction):
        for observer in self._observers:
            observer.update(transaction)

# ==== Логгер, який веде журнал ====
class Logger(Observer):
    def update(self, transaction):
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"[LOG] Додано: {transaction}\n")

# ==== Аналітика (можна доповнити далі) ====
class Analytics(Observer):
    def __init__(self):
        self.total_income = 0
        self.total_expense = 0

    def update(self, transaction):
        if transaction.get_type() == "Income":
            self.total_income += transaction.amount
        elif transaction.get_type() == "Expense":
            self.total_expense += transaction.amount

    def summary(self):
        return {
            "income": self.total_income,
            "expense": self.total_expense
        }
