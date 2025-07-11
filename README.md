# 💰 Finance Tracker — Персональний фінансовий трекер на Python

Цей застосунок допомагає відстежувати ваші доходи, витрати, загальний баланс та візуалізувати витрати по категоріях. Побудований з використанням архітектури на базі шаблонів проєктування (Design Patterns) та сучасного GUI.

---

## 📂 Структура проєкту

```

Finance\_Tracker/
├── charts/
│   └── chart.py              # Побудова графіків (матплотліб)
├── core/
│   ├── database.py           # Робота з SQLite базою
│   ├── manager.py            # Facade над логікою
│   ├── observer.py           # Реалізація патерну Observer
│   └── transaction.py        # Класи та Factory для транзакцій
├── data/
│   └── finance.db            # SQLite база (генерується)
├── tests/
│   └── test\_transactions.py  # 20+ модульних тестів (unittest)
├── ui/
│   └── data/
│       └── log.txt           # Логування (через Observer)
│   └── gui.py                # Графічний інтерфейс Tkinter
├── log.txt                   # Основний лог-файл
└── main.py                   # Точка запуску (альтернативна)

````

---

## 🧩 Використані шаблони проєктування (Design Patterns)

### 🏭 Factory Method — `TransactionFactory` (`core/transaction.py`)
> Створює об'єкти `IncomeTransaction` або `ExpenseTransaction` залежно від типу. Дозволяє легко розширювати типи транзакцій у майбутньому.

**Переваги:**
- Централізоване створення об'єктів
- Інкапсуляція логіки вибору класу

---

### 🧰 Facade — `FinanceManager` (`core/manager.py`)
> Спрощує роботу з транзакціями: додає, видаляє, повертає баланс, дані для графіків. Приховує складну логіку взаємодії з базою, транзакціями та спостерігачами.

**Переваги:**
- Простий інтерфейс для GUI
- Вся логіка в одному фасаді

---

### 🔔 Observer — `Observer` / `LoggerObserver` (`core/observer.py`)
> При кожній транзакції спостерігач логування фіксує дію у `log.txt`. У майбутньому можна додати email-нотифікацію або push-повідомлення.

**Переваги:**
- Гнучка система повідомлень
- Розширюється без змін основної логіки

---

## 🧪 Модульні тести

- 📁 `tests/test_transactions.py` — понад 20 модульних тестів:
  - створення транзакцій
  - робота бази даних
  - розрахунок балансу
  - видалення транзакцій
  - облік доходів/витрат

### ▶️ Запуск тестів:
```bash
python -m unittest discover tests
````

---

## 💻 Запуск застосунку

### 1. Встановити залежності:

```bash
pip install matplotlib
```

### 2. Запустити:

```bash
python ui/gui.py
```

---

## 📊 Візуалізація

* Додано діаграму витрат за категоріями (Pie Chart)
* Побудова графіка вбудована в GUI
* Виводиться автоматично після натискання

---
## UML-діаграма архітектури

![UML-діаграма](uml.png)

## 📄 Автор

* **Ім'я:** \[Пихтін Нікіта]
* **Група:** \[ФеП-31]
* **Рік:** 2025

