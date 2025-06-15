import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.manager import FinanceManager


class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Фінансовий трекер")
        self.root.state('zoomed')
        self.manager = FinanceManager()
        self.chart_canvas = None

        # 🎨 Стилізація
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.bg_color = "#f1f2f6"
        self.accent_color = "#40739e"
        self.button_color = "#2f3640"
        self.text_color = "#2d3436"

        self.root.configure(bg=self.bg_color)
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("TLabel", background=self.bg_color, foreground=self.text_color, font=("Segoe UI", 10))
        self.style.configure("TButton", background=self.button_color, foreground="white", font=("Segoe UI", 10, "bold"))
        self.style.configure("TCombobox", padding=5)

        # Двоколонкова сітка
        self.left_frame = ttk.Frame(root, padding=10)
        self.right_frame = ttk.Frame(root, padding=10)
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        root.columnconfigure(0, weight=3)
        root.columnconfigure(1, weight=2)
        root.rowconfigure(0, weight=1)

        self.build_right_ui()
        self.build_left_ui()
        self.update_display()

    def build_right_ui(self):
        self.right_frame.columnconfigure(0, weight=1)
        self.right_frame.columnconfigure(1, weight=1)

        ttk.Label(self.right_frame, text="Тип:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.type_var = tk.StringVar()
        self.type_combobox = ttk.Combobox(self.right_frame, textvariable=self.type_var,
                                          values=["Income", "Expense"], state="readonly")
        self.type_combobox.grid(row=0, column=1, sticky="we", padx=5, pady=2)
        self.type_combobox.set("Income")

        ttk.Label(self.right_frame, text="Сума:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.amount_entry = ttk.Entry(self.right_frame)
        self.amount_entry.grid(row=1, column=1, sticky="we", padx=5, pady=2)

        ttk.Label(self.right_frame, text="Категорія:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.category_entry = ttk.Entry(self.right_frame)
        self.category_entry.grid(row=2, column=1, sticky="we", padx=5, pady=2)

        ttk.Label(self.right_frame, text="Дата (YYYY-MM-DD):").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.date_entry = ttk.Entry(self.right_frame)
        self.date_entry.grid(row=3, column=1, sticky="we", padx=5, pady=2)

        ttk.Label(self.right_frame, text="Опис:").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.description_entry = ttk.Entry(self.right_frame)
        self.description_entry.grid(row=4, column=1, sticky="we", padx=5, pady=2)

        self.add_button = ttk.Button(self.right_frame, text="➕ Додати транзакцію", command=self.add_transaction)
        self.add_button.grid(row=5, column=0, columnspan=2, pady=5, padx=5, sticky="we")

        self.delete_button = ttk.Button(self.right_frame, text="🗑️ Видалити вибране", command=self.delete_selected_transaction)
        self.delete_button.grid(row=6, column=0, columnspan=2, pady=5, padx=5, sticky="we")

        self.chart_button = ttk.Button(self.right_frame, text="📊 Графік витрат у вікні", command=self.render_expense_chart_in_gui)
        self.chart_button.grid(row=7, column=0, columnspan=2, pady=5, padx=5, sticky="we")

        self.balance_label = ttk.Label(self.right_frame, text="Баланс: 0 грн", font=("Segoe UI", 11, "bold"))
        self.balance_label.grid(row=8, column=0, columnspan=2, pady=10)

        ttk.Label(self.right_frame, text="Показати:").grid(row=9, column=0, sticky="w", padx=5, pady=2)
        self.filter_var = tk.StringVar()
        self.filter_combobox = ttk.Combobox(self.right_frame, textvariable=self.filter_var,
                                            values=["Всі", "Income", "Expense"], state="readonly")
        self.filter_combobox.grid(row=9, column=1, sticky="we", padx=5, pady=2)
        self.filter_combobox.set("Всі")
        self.filter_combobox.bind("<<ComboboxSelected>>", lambda e: self.update_display())

    def build_left_ui(self):
        self.left_frame.rowconfigure(0, weight=1)
        self.left_frame.columnconfigure(0, weight=1)

        self.transactions_text = tk.Text(self.left_frame, wrap=tk.WORD, font=("Consolas", 10), bg="white", fg="#2d3436")
        self.transactions_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.left_frame, command=self.transactions_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.transactions_text.config(yscrollcommand=scrollbar.set)

    def add_transaction(self):
        try:
            t_type = self.type_var.get().lower()
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            date = self.date_entry.get()
            description = self.description_entry.get()
            self.manager.add_transaction(t_type, amount, category, date, description)
            messagebox.showinfo("Успіх", "Транзакцію додано!")
            self.clear_inputs()
            self.update_display()
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def delete_selected_transaction(self):
        try:
            selection = self.transactions_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            if not selection.strip().startswith("#"):
                messagebox.showwarning("Увага", "Виділіть рядок з транзакцією (починається з #ID).")
                return
            transaction_id = int(selection.strip().split()[0][1:])
            if messagebox.askyesno("Підтвердження", f"Видалити транзакцію #{transaction_id}?"):
                self.manager.delete_transaction_by_id(transaction_id)
                messagebox.showinfo("Успішно", "Транзакцію видалено.")
                self.update_display()
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося видалити: {e}")

    def render_expense_chart_in_gui(self):
        transactions = self.manager.get_all_transactions()
        data = defaultdict(float)
        for t in transactions:
            if t.get_type().lower() == "expense":
                data[t.category] += t.amount
        if not data:
            messagebox.showinfo("Інфо", "Немає витрат для побудови графіку.")
            return
        if self.chart_canvas:
            self.chart_canvas.get_tk_widget().destroy()
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=140)
        ax.set_title("Витрати по категоріях")
        self.chart_canvas = FigureCanvasTkAgg(fig, master=self.left_frame)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, pady=10, sticky="nsew")

    def clear_inputs(self):
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

    def update_display(self):
        self.transactions_text.delete("1.0", tk.END)
        transactions = self.manager.get_all_transactions()
        filter_type = self.filter_var.get()
        for t in transactions:
            if filter_type == "Всі" or t.get_type().lower() == filter_type.lower():
                self.transactions_text.insert(tk.END, str(t) + "\n")
        balance = self.manager.get_balance()
        summary = self.manager.get_summary()
        self.balance_label.config(
            text=f"Баланс: {balance:.2f} грн | Дохід: {summary['income']} | Витрати: {summary['expense']}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
