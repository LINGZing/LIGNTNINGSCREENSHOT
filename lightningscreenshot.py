import sys
import os


import qdarkstyle
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget

from lightningscreenshotui import Ui_Form
from ligntningscst import lightningscst

# url = 'https://www.heweather.com/'
url = 'http://192.4.2.154/lightning/'


class screenshotthread(QThread):
    scstout = pyqtSignal(str)

    def __init__(self, parent=None):
        super(screenshotthread, self).__init__(parent)

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            text = lightningscst(url)
            self.scstout.emit(text)
            self.sleep(300)


class MyWidget(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.temp = 0
        self.thread = screenshotthread()
        self.thread.scstout.connect(self.slotscst)
        self.thread.start()

    def slotscst(self, text):
        if self.temp >= 10:
            self.textBrowser.clear()
            self.temp = 0
        if os.path.exists(text):
            self.textBrowser.insertPlainText(text + "已保存" + "\n")
            QApplication.processEvents()
            self.temp = self.temp + 1
        else:
            self.textBrowser.insertPlainText(text + "\n")
            self.temp = self.temp + 1


if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWgt = MyWidget()
    myWgt.setWindowIcon(QIcon("ls.ico"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    myWgt.show()
    sys.exit(app.exec_())
