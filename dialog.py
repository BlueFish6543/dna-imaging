from PySide2.QtWidgets import QDialog, QDialogButtonBox
from PySide2.QtCore import QObject, SIGNAL
import re

class Dialog(QDialog):
    def __init__(self, ui):
        super(Dialog, self).__init__()
        self.ui = ui
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.file_name = ""
        self.email_address = ""

        QObject.connect(self.ui.fileName, SIGNAL ('textEdited(QString)'), self._check_valid)
        QObject.connect(self.ui.emailAddress, SIGNAL ('textEdited(QString)'), self._check_valid)

    def _get_image_file_name(self):
        file_name = self.ui.fileName.text()
        pattern = re.compile(r'^(?:[0-9a-zA-Z\-\_\.])+$')
        self.file_name = file_name
        return bool(pattern.match(file_name))

    def _get_email_address(self):
        email_address = self.ui.emailAddress.text()
        pattern = re.compile(r'^(?:[0-9a-zA-Z\-\_\.])+\@(?:[0-9a-zA-Z\.])+\.(?:[0-9a-zA-Z])+$')
        self.email_address = email_address
        return bool(pattern.match(email_address))

    def _check_valid(self):
        if self._get_image_file_name() and self._get_email_address():
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

    def get_data(self):
        return self.file_name, self.email_address

    def show(self):
        return self.ui.exec_()