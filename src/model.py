from PySide2.QtCore import QAbstractTableModel, Qt

class ResultsModel(QAbstractTableModel):
    def __init__(self):
        super(ResultsModel, self).__init__()
        self.rows = 0
        self.columns = 2
        self.results = []

    def rowCount(self, parent):
        return self.rows

    def columnCount(self, parent):
        return self.columns

    def data(self, index, role):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            return self.value(row, column)

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return "Column"
                elif section == 1:
                    return "Value"

    def setResults(self, results):
        self.beginResetModel()
        self.rows = len(results)
        self.results = results
        self.endResetModel()

    def value(self, row, column):
        return self.results[row][column]
