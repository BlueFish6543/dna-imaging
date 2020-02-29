from PySide2.QtWidgets import QWidget, QFileDialog, QHeaderView, QShortcut, QApplication
from PySide2.QtCore import QDir, QObject, QFileInfo, SIGNAL, Qt, QFile
from PySide2.QtGui import QPixmap, QImage, QKeySequence
from PySide2.QtUiTools import QUiLoader
import numpy as np
import os
from src.model import ResultsModel
import src.imaging as imaging
from src.dialog import Dialog
import src.utils as utils
import src.camera as camera

class Widget(QWidget):
    def __init__(self, ui):
        super(Widget, self).__init__()

        self.ui = ui
        self.directory = QDir.currentPath()
        self.file_name = ""

        self.pixmap = None

        self.num_columns = 5
        self.num_colours = 8
        self.ladder_threshold = 5
        self.sample_threshold = 3

        self.ladder_bands = 0
        self.coords = []
        self.calibration_values = []
        self.results = []

        QObject.connect(ui.selectFile, SIGNAL ('clicked()'), self.select_file)
        QObject.connect(ui.loadImage, SIGNAL ('clicked()'), self.load_image)
        QObject.connect(ui.saveImage, SIGNAL ('clicked()'), self.save_image)
        QObject.connect(ui.sendEmail, SIGNAL ('clicked()'), self.show_dialog)

        self.ui.columns.setMinimum(2)
        self.ui.columns.setValue(self.num_columns)
        self.ui.colours.setMinimum(4)
        self.ui.colours.setValue(self.num_colours)
        self.ui.ladderThreshold.setMinimum(1)
        self.ui.ladderThreshold.setMaximum(self.num_colours)
        self.ui.ladderThreshold.setValue(self.ladder_threshold)
        self.ui.sampleThreshold.setMinimum(1)
        self.ui.sampleThreshold.setMaximum(self.num_colours)
        self.ui.sampleThreshold.setValue(self.sample_threshold)

        QObject.connect(self.ui.columns, SIGNAL ('valueChanged(int)'), self.set_columns)
        QObject.connect(self.ui.colours, SIGNAL ('valueChanged(int)'), self.set_colours)
        QObject.connect(self.ui.ladderThreshold, SIGNAL ('valueChanged(int)'), self.set_ladder_threshold)
        QObject.connect(self.ui.sampleThreshold, SIGNAL ('valueChanged(int)'), self.set_sample_threshold)

        self.ui.calibrationText.setText("No ladder bands detected.")

        self.model = ResultsModel()
        self.ui.results.setModel(self.model)
        self.ui.results.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.results.show()

        QObject.connect(self.ui.findContours, SIGNAL ('clicked()'), self.find_contours)
        QObject.connect(self.ui.findContours, SIGNAL ('clicked()'), self.update_calibration_text)
        QObject.connect(self.ui.calibrate, SIGNAL ('clicked()'), self.parse_calibration_base_pairs)

        ui_file = QFile(os.path.join(os.getcwd(), 'src', 'dialog.ui'))
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        ui = loader.load(ui_file)
        ui_file.close()

        self.dialog = Dialog(ui)
        QObject.connect(self.dialog.ui, SIGNAL ('accepted()'), self.send_email)

        quit_shortcut = QShortcut(QKeySequence.Quit, self.ui)
        close_shortcut = QShortcut(QKeySequence.Close, self.ui)
        QObject.connect(quit_shortcut, SIGNAL ('activated()'), self.ui.close)
        QObject.connect(close_shortcut, SIGNAL ('activated()'), self.ui.close)

        QObject.connect(self.ui.takePicture, SIGNAL ('clicked()'), self.take_picture)
        self.ui.whiteBalance.addItems(camera.MODES)
        QObject.connect(self.ui.whiteBalance, SIGNAL ('currentIndexChanged(int)'), self.select_white_balance)

    def select_file(self):
        self.file_name = QFileDialog.getOpenFileName(
            self, "Select file", self.directory, "Images (*.png *.jpg)"
        )[0]
        self.ui.lineEdit.setText(self.file_name)
        f = QFileInfo(self.file_name)
        self.directory = f.absolutePath()

    def load_image(self):
        if not self.file_name:
            return
        else:
            pic = QPixmap(self.file_name)
            w = self.ui.picture.width()
            h = self.ui.picture.height()
            self.ui.picture.setPixmap(pic.scaled(w, h, Qt.KeepAspectRatio))
            self.ui.picture.setAlignment(Qt.AlignCenter)

    def take_picture(self):
        camera.take_picture()
        self.file_name = os.path.join(os.getcwd(), 'tmp', 'image.jpg')
        self.load_image()

    def select_white_balance(self):
        camera.set_white_balance(self.ui.whiteBalance.currentText())

    def save_image(self):
        if not self.pixmap:
            return
        file_name = QFileDialog.getSaveFileName(
            self, "Save file", self.directory, "Images (*.png *.jpg)"
        )[0]
        info = QFileInfo(file_name)
        if not info.suffix():
            file_name += ".png"
        self.pixmap.save(file_name)

    def show_dialog(self):
        if not self.pixmap:
            return
        self.dialog.show()

    def send_email(self):
        file_name, email_address = self.dialog.get_data()
        info = QFileInfo(file_name)
        if not info.suffix():
            file_name += ".png"
        file_name = os.path.join(os.getcwd(), "tmp", file_name)
        self.pixmap.save(file_name)

        os.remove(file_name)

    def set_columns(self):
        self.num_columns = self.ui.columns.value()

    def set_colours(self):
        self.num_colours = self.ui.colours.value()
        self.ui.ladderThreshold.setMaximum(self.num_colours)
        self.ui.sampleThreshold.setMaximum(self.num_colours)

    def set_ladder_threshold(self):
        self.ladder_threshold = self.ui.ladderThreshold.value()

    def set_sample_threshold(self):
        self.sample_threshold = self.ui.sampleThreshold.value()

    def find_contours(self):
        if not self.file_name:
            return
        else:
            # https://stackoverflow.com/questions/34232632/convert-python-opencv-image-numpy-array-to-pyqt-qpixmap-image
            img, coords = imaging.find_contours(
                self.file_name, self.sample_threshold, self.ladder_threshold, self.num_columns, self.num_colours)
            height, width, channel = img.shape
            bytes_per_line = 3 * width
            qimg = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.pixmap = QPixmap.fromImage(qimg)

            w = self.ui.picture.width()
            h = self.ui.picture.height()
            self.ui.picture.setPixmap(self.pixmap.scaled(w, h, Qt.KeepAspectRatio))
            self.ui.picture.setAlignment(Qt.AlignCenter)

            self.coords = coords
            self.ladder_bands = len(coords[0])

            self.update_calibration_text()

    def update_calibration_text(self):
        self.ui.calibrationText.setText("{} ladder bands detected.".format(self.ladder_bands))
        self.ui.calibrationHelpText.setText("Enter ladder base pairs below:")

    def parse_calibration_base_pairs(self):
        if not self.ladder_bands:
            return
        
        contents = self.ui.plainTextEdit.toPlainText()
        str_list = contents.splitlines()
        int_list = []
        try:
            assert len(str_list) == self.ladder_bands
            for s in str_list:
                int_list.append(int(s))
        except AssertionError:
            self.ui.warningMessage.setText("Wrong number of values entered.")
            return
        except ValueError:
            self.ui.warningMessage.setText("Invalid characters entered.")
            return
        
        self.calibration_values = int_list
        self.ui.warningMessage.setText("")
        self.calibrate_data()

    def calibrate_data(self):
        if (not self.coords) or (not self.calibration_values):
            return
        self.results = imaging.calibrate_data(self.coords, self.calibration_values,
                                         self.ui.checkBox.isChecked())
        self.update_results()

    def update_results(self):
        if not self.results:
            return
        self.model.setResults(self.results)

    def show(self):
        self.ui.show()
