import sys

import cv2
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QBasicTimer, Qt
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QWidget, QApplication


class MainWindow(QWidget):
    CAMERA = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.qimage = None
        self.capture = cv2.VideoCapture(self.CAMERA)
        self.update_image()
        self.timer = QBasicTimer()
        self.timer.start(50, self)

    def timerEvent(self, event, *args, **kwargs):
        self.update_image()
        self.update()

    def update_image(self):
        ret, frame = self.capture.read()
        height, width, byte_value = frame.shape
        byte_value *= width
        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, frame)
        self.qimage = QImage(frame, width, height, byte_value, QImage.Format_RGB888)

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setPen(Qt.gray)
        painter.drawImage(0, 0, self.qimage)
        painter.end()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    application = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(application.exec_())
