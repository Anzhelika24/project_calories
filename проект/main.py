import sys
from PyQt5.QtWidgets import (
    QApplication
)
from DishManager import DishManager
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DishManager()
    window.show()
    sys.exit(app.exec_())
