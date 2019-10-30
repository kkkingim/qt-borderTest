import random

from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QLabel


class Game(QLabel):
    def __init__(self, parent, width=None, height=None):
        super().__init__(parent)
        self.initUI(width, height)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.gameUpdate)

        self.balls = []

        self.timer.start(50)

        self.clicked = False
        self.endP = None

    def initUI(self, w, h):
        width = self.parent().width() if w == None else w
        height = self.parent().height() if h == None else h

        self.setGeometry(0, 0, width, height)
        self.setStyleSheet("background-color: #98A8CB")

    def addBall(self, x, y):
        self.balls.append({
            "pos": [x, y],
            "a": [0, 0]
        })

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:

        def drawCircle(qp, x, y, r):
            for i in range(-r, r + 1):
                for j in range(-r, r + 1):
                    if abs(i ** 2 + j ** 2 - r ** 2) <= r:
                        qp.drawPoint(i + x, j + y)

        def t(x, y):
            m, n = 1, 1
            if x > 0:
                m = -1
            if y > 0:
                n = -1
            return m, n

        super().paintEvent(a0)

        qp = QPainter(self)
        for ball in self.balls:
            x, y = ball["pos"]
            r = 5
            drawCircle(qp, x, y, r)

        if self.clicked and self.endP:
            x, y = self.balls[-1]["pos"]
            qp.drawLine(x, y, *self.endP)

            m, n = t(self.endP[0] - x, self.endP[1] - y)
            qp.drawLine(*self.endP, self.endP[0], self.endP[1] + n * 10)
            qp.drawLine(*self.endP, self.endP[0] + m * 10, self.endP[1])

            qp.drawRect(x, y, self.endP[0] - x, self.endP[1] - y)
            drawCircle(qp, *self.endP, 5)

        qp.end()

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        super().mouseReleaseEvent(ev)

        if self.clicked == True:
            self.clicked = False
            x, y = self.balls[-1]["pos"]
            if ev.x() == x and ev.y() == y:
                self.balls.pop(-1)
                return

            ex, ey = ev.x(), ev.y()

            m = ((ex - x) ** 2 + (ey - y) ** 2) ** 0.5

            dx, dy = (ex - x) / m, (ey - y) / m

            self.balls[-1]["a"] = [dx * 3, dy * 3]

    def mouseMoveEvent(self, ev: QtGui.QMouseEvent) -> None:
        super().mouseMoveEvent(ev)
        self.endP = ev.x(), ev.y()

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        super().mousePressEvent(ev)
        self.clicked = True
        self.endP = None
        self.addBall(ev.x(), ev.y())

    def gameUpdate(self):
        def crashBoard(x, y):
            a = 1 if x <= 0 else 0
            b = 1 if y <= 0 else 0
            a = -1 if x >= self.width() else a
            b = -1 if y >= self.height() else b
            if a == 0 and b == 0:
                return False
            return a, b

        for ball in self.balls:
            # offset = random.choice([(-3, 0), (3, 0), (0, 3), (0, -3)])
            ball["pos"][0] += ball["a"][0]
            ball["pos"][1] += ball["a"][1]

            crash = crashBoard(*ball["pos"])
            if crash:
                a, b = crash
                if a != 0:
                    ball["a"][0] = -ball["a"][0]
                if b != 0:
                    ball["a"][1] = -ball["a"][1]

                ball["pos"][0] += ball["a"][0]
                ball["pos"][1] += ball["a"][1]

        self.repaint()
