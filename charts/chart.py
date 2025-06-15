import matplotlib.pyplot as plt
from collections import defaultdict

def show_expense_pie(transactions):
    # Збираємо витрати по категоріях
    categories = defaultdict(float)
    for t in transactions:
        if t.get_type().lower() == "expense":
            categories[t.category] += t.amount

    if not categories:
        print("Немає витрат для побудови графіку.")
        return

    labels = list(categories.keys())
    sizes = list(categories.values())

    # Побудова діаграми
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Витрати по категоріях")
    plt.axis('equal')
    plt.show()
