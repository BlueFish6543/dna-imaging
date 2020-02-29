import sys
import os
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile
from src.widget import Widget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    ui_file = QFile(os.path.join(os.getcwd(), 'src', 'widget.ui'))
    ui_file.open(QFile.ReadOnly)
    
    loader = QUiLoader()
    ui = loader.load(ui_file)
    ui_file.close()

    widget = Widget(ui)
    widget.show()
    
    sys.exit(app.exec_())