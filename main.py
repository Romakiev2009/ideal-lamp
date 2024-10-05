import requests
import tkinter as tk
from tkinter import messagebox, ttk

class CurrencyConverter:
    def __init__(self):
        self.rates = {}
        self.get_rates()

    def get_rates(self):
        try:
            response = requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json")
            data = response.json()

            for item in data:
                self.rates[item['cc']] = item['rate']
            self.rates['UAH'] = 1.0
        except requests.RequestException as e:
            messagebox.showerror("Помилка мережі", f"Не вдалося отримати дані: {e}")

    def convert(self, amount, from_currency):
        if from_currency != "USD":
            amount = amount / self.rates[from_currency]
        return round(amount * self.rates["USD"], 2)

class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Конвертер валюти")
        self.converter = CurrencyConverter()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Сума валюти:").grid(row=0, column=0)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Виберіть валюту:").grid(row=1, column=0)
        self.currency_combobox = ttk.Combobox(self.root, values=[code for code in self.converter.rates.keys() if code != "USD"], state="readonly")
        self.currency_combobox.grid(row=1, column=1)
        self.currency_combobox.current(0)  # Встановлюємо перший елемент за замовчуванням

        self.convert_button = tk.Button(self.root, text="Конвертувати", command=self.convert)
        self.convert_button.grid(row=2, columnspan=2)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.grid(row=3, columnspan=2)

    def convert(self):
        try:
            amount = float(self.amount_entry.get())
            from_currency = self.currency_combobox.get()
            converted_amount = self.converter.convert(amount, from_currency)

            self.result_label.config(text=f"{amount} {from_currency} = {converted_amount:.2f} USD")
        except KeyError:
            messagebox.showerror("Помилка", "Некоректний код валюти. Спробуйте ще раз.")
        except ValueError:
            messagebox.showerror("Помилка", "Некоректна сума. Спробуйте ще раз.")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

def main():
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
