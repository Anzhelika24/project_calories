from PyQt5.QtWidgets import (
    QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QDialog
)
from Dish import Dish


class AddDishDialog(QDialog):
    def __init__(self, dish_manager):
        super().__init__()

        self.dish_manager = dish_manager
        self.setWindowTitle("Добавить блюдо")
        self.setGeometry(150, 150, 300, 200)

        self.layout = QVBoxLayout()

        self.name_input = QLineEdit(self)
        self.kcal_input = QLineEdit(self)

        self.layout.addWidget(QLabel("Название блюда:"))
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(QLabel("КБЖУ (калории, белки, жиры, углеводы):"))
        self.layout.addWidget(self.kcal_input)

        self.add_button = QPushButton("Добавить блюдо", self)
        self.layout.addWidget(self.add_button)

        self.add_button.clicked.connect(self.add_dish)

        self.setLayout(self.layout)

    def add_dish(self):
        name = self.name_input.text()
        kcal_input = self.kcal_input.text()

        if not name or not kcal_input:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        try:
            calories, proteins, fats, carbs = map(float, kcal_input.split(','))
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите корректные значения КБЖУ через запятую.")
            return

        new_dish = Dish(name, calories, proteins, fats, carbs)
        self.dish_manager.dishes.append(new_dish)
        self.dish_manager.save_dishes()
        self.dish_manager.update_dish_list()

        self.close()
