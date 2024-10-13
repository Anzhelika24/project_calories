import json
from datetime import timedelta
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QListWidget, QMessageBox, QTextEdit, QMenu, QDateEdit
)
from PyQt5.QtCore import Qt
from datetime import datetime

from AddDishDialog import AddDishDialog
from Dish import Dish
from MealRecord import MealRecord


class DishManager(QWidget):
    def __init__(self):
        super().__init__()

        self.dishes = []
        self.eaten_dishes = []
        self.meal_records = []
        self.load_dishes()
        self.load_meal_records()

        self.setWindowTitle("Управление блюдами")
        self.setGeometry(100, 100, 600, 600)

        self.layout = QVBoxLayout()

        self.add_dish_button = QPushButton("Добавить свое блюдо", self)
        self.layout.addWidget(self.add_dish_button)

        self.dish_list = QListWidget(self)

        self.search_input = QLineEdit(self)
        self.search_button = QPushButton("Поиск", self)

        self.eaten_dish_input = QLineEdit(self)
        self.add_eaten_button = QPushButton("Добавить съеденное блюдо", self)
        self.eaten_dish_list = QListWidget(self)

        self.date_selector = QDateEdit(self)
        self.date_selector.setDate(datetime.now())
        self.date_selector.setCalendarPopup(True)
        self.date_selector.setDisplayFormat("yyyy-MM-dd")

        self.show_meals_button = QPushButton("Показать съеденные блюда за день", self)

        self.total_nutrition_display = QTextEdit(self)
        self.total_nutrition_display.setReadOnly(True)

        # Date range selectors for plotting
        self.start_date_selector = QDateEdit(self)
        self.start_date_selector.setDate(datetime.now() - timedelta(days=7))
        self.start_date_selector.setCalendarPopup(True)
        self.start_date_selector.setDisplayFormat("yyyy-MM-dd")

        self.end_date_selector = QDateEdit(self)
        self.end_date_selector.setDate(datetime.now())
        self.end_date_selector.setCalendarPopup(True)
        self.end_date_selector.setDisplayFormat("yyyy-MM-dd")

        self.plot_button = QPushButton("Построить график потребляемых калорий", self)

        self.layout.addWidget(self.add_dish_button)
        self.layout.addWidget(QLabel("Поиск по названию:"))
        self.layout.addWidget(self.search_input)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.dish_list)

        self.layout.addWidget(QLabel("Съеденные блюда:"))
        self.layout.addWidget(self.eaten_dish_input)
        self.layout.addWidget(self.add_eaten_button)
        self.layout.addWidget(self.eaten_dish_list)

        self.layout.addWidget(QLabel("Выберите дату:"))
        self.layout.addWidget(self.date_selector)
        self.layout.addWidget(self.show_meals_button)

        self.layout.addWidget(QLabel("Общее КБЖУ за день:"))
        self.layout.addWidget(self.total_nutrition_display)

        self.layout.addWidget(QLabel("Выберите начальную дату:"))
        self.layout.addWidget(self.start_date_selector)
        self.layout.addWidget(QLabel("Выберите конечную дату:"))
        self.layout.addWidget(self.end_date_selector)
        self.layout.addWidget(self.plot_button)

        self.setLayout(self.layout)

        self.add_dish_button.clicked.connect(self.open_add_dish_dialog)
        self.show_all_button = QPushButton("Показать все блюда")
        self.layout.addWidget(self.show_all_button)
        self.show_all_button.clicked.connect(self.update_dish_list)
        self.dish_list.itemClicked.connect(self.display_dish_info)
        self.search_button.clicked.connect(self.search_dish)
        self.add_eaten_button.clicked.connect(self.add_eaten_dish)
        self.show_meals_button.clicked.connect(self.show_meals_for_selected_date)
        self.plot_button.clicked.connect(self.plot_calorie_graph)

        self.dish_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.dish_list.customContextMenuRequested.connect(self.show_context_menu)

        self.update_total_nutrition_display()

    def open_add_dish_dialog(self):
        dialog = AddDishDialog(self)
        dialog.exec_()

    def show_context_menu(self, pos):
        selected_item = self.dish_list.itemAt(pos)
        if selected_item:
            context_menu = QMenu(self)
            delete_action = context_menu.addAction("Удалить блюдо")
            delete_action.triggered.connect(lambda: self.confirm_delete_dish(selected_item))
            context_menu.exec_(self.dish_list.mapToGlobal(pos))

    def confirm_delete_dish(self, selected_item):
        if QMessageBox.question(self, "Подтверждение", "Точно удалить блюдо из общего списка блюд?") == QMessageBox.Yes:
            selected_index = self.dish_list.row(selected_item)
            del self.dishes[selected_index]
            self.save_dishes()
            self.update_dish_list()

    def save_dishes(self):
        with open("dishes.json", "w") as f:
            json.dump([dish.to_dict() for dish in self.dishes], f)

    def load_dishes(self):
        try:
            with open("dishes.json", "r") as f:
                dishes_data = json.load(f)
                self.dishes = [Dish.from_dict(data) for data in dishes_data]
        except FileNotFoundError:
            self.dishes = []

    def save_meal_record(self):
        current_date = datetime.now().strftime("%Y-%m-%d")
        meal_record = MealRecord(current_date, self.eaten_dishes)
        self.meal_records.append(meal_record)
        self.save_meal_records()

    def save_meal_records(self):
        with open("meal_records.json", "w") as f:
            json.dump([record.to_dict() for record in self.meal_records], f)

    def load_meal_records(self):
        try:
            with open("meal_records.json", "r") as f:
                records_data = json.load(f)
                self.meal_records = [MealRecord.from_dict(data) for data in records_data]
        except FileNotFoundError:
            self.meal_records = []

    def add_eaten_dish(self):
        dish_name = self.eaten_dish_input.text()
        for dish in self.dishes:
            if dish.name.lower() == dish_name.lower():
                self.eaten_dishes.append(dish)
                self.eaten_dish_list.addItem(dish.name)
                self.update_total_nutrition_display()
                self.save_meal_record()
                self.eaten_dish_input.clear()
                return

        QMessageBox.warning(self, "Ошибка", "Блюдо не найдено.")

    def show_meals_for_selected_date(self):
        selected_date = self.date_selector.date().toString("yyyy-MM-dd")
        meals_for_date = [record for record in self.meal_records if record.date == selected_date]

        if not meals_for_date:
            self.total_nutrition_display.setPlainText("На выбранную дату нет записей.")
            return

        total_calories = sum(dish.calories for record in meals_for_date for dish in record.eaten_dishes)
        total_proteins = sum(dish.proteins for record in meals_for_date for dish in record.eaten_dishes)
        total_fats = sum(dish.fats for record in meals_for_date for dish in record.eaten_dishes)
        total_carbs = sum(dish.carbs for record in meals_for_date for dish in record.eaten_dishes)

        self.total_nutrition_display.setPlainText(f"Калории: {total_calories} kcal\n"
                                                  f"Белки: {total_proteins} g\n"
                                                  f"Жиры: {total_fats} g\n"
                                                  f"Углеводы: {total_carbs} g\n")

    def plot_calorie_graph(self):
        start_date = self.start_date_selector.date().toString("yyyy-MM-dd")
        end_date = self.end_date_selector.date().toString("yyyy-MM-dd")

        date_range_meals = [
            (record.date, sum(dish.calories for dish in record.eaten_dishes))
            for record in self.meal_records if start_date <= record.date <= end_date
        ]

        if not date_range_meals:
            QMessageBox.warning(self, "Ошибка", "Нет записей в выбранном диапазоне дат.")
            return

        dates, calories = zip(*date_range_meals)

        plt.figure(figsize=(10, 5))
        plt.plot(dates, calories, marker='o')
        plt.title("Потребление калорий")
        plt.xlabel("Дата")
        plt.ylabel("Калории")
        plt.xticks(rotation=45)
        plt.grid()
        plt.tight_layout()
        plt.show()

    def update_dish_list(self):
        self.dish_list.clear()
        self.dish_list.addItems([dish.name for dish in self.dishes])

    def search_dish(self):
        search_term = self.search_input.text().lower()
        filtered_dishes = [dish for dish in self.dishes if search_term in dish.name.lower()]
        self.dish_list.clear()
        self.dish_list.addItems([dish.name for dish in filtered_dishes])

    def update_total_nutrition_display(self):
        total_calories = sum(dish.calories for dish in self.eaten_dishes)
        total_proteins = sum(dish.proteins for dish in self.eaten_dishes)
        total_fats = sum(dish.fats for dish in self.eaten_dishes)
        total_carbs = sum(dish.carbs for dish in self.eaten_dishes)

        self.total_nutrition_display.setPlainText(f"Калории: {total_calories} kcal\n"
                                                  f"Белки: {total_proteins} g\n"
                                                  f"Жиры: {total_fats} g\n"
                                                  f"Углеводы: {total_carbs} g\n")

    def display_dish_info(self, item):
        selected_dish = next(dish for dish in self.dishes if dish.name == item.text())
        QMessageBox.information(self, "Информация о блюде", str(selected_dish))

