class Dish:
    def __init__(self, name, calories, proteins, fats, carbs):
        self.name = name
        self.calories = calories
        self.proteins = proteins
        self.fats = fats
        self.carbs = carbs

    def to_dict(self):
        return {
            'name': self.name,
            'calories': self.calories,
            'proteins': self.proteins,
            'fats': self.fats,
            'carbs': self.carbs
        }

    @staticmethod
    def from_dict(data):
        return Dish(data['name'], data['calories'], data['proteins'], data['fats'], data['carbs'])

    def __str__(self):
        return f"{self.name} - КБЖУ: {self.calories} kcal, {self.proteins}g, {self.fats}g, {self.carbs}g"
