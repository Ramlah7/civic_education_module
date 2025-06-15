import sys
from PyQt5.QtWidgets import QApplication
from gui.civic_education_gui import CivicEducationApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CivicEducationApp()
    window.show()
    sys.exit(app.exec_())
