import sys
from PyQt5.QtWidgets import QDialog, QApplication

from game import Game


class main(QDialog):
    def __init__(self):
        super().__init__()

        self.game = Game(self)
        self.game.setFixedSize(100, 100)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = main()
    sys.exit(app.exec_())
