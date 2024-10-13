from Dish import Dish


class MealRecord:
    def __init__(self, date, eaten_dishes):
        self.date = date
        self.eaten_dishes = eaten_dishes

    def to_dict(self):
        return {
            'date': self.date,
            'eaten_dishes': [dish.to_dict() for dish in self.eaten_dishes]
        }

    @staticmethod
    def from_dict(data):
        eaten_dishes = [Dish.from_dict(dish) for dish in data['eaten_dishes']]
        return MealRecord(data['date'], eaten_dishes)

    def __str__(self):
        return f"{self.date}: {', '.join(dish.name for dish in self.eaten_dishes)}"
