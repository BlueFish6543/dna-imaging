import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile
from widget import Widget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    ui_file = QFile("widget.ui")
    ui_file.open(QFile.ReadOnly)
    
    loader = QUiLoader()
    ui = loader.load(ui_file)
    ui_file.close()

    widget = Widget(ui)
    widget.show()
    
    sys.exit(app.exec_())