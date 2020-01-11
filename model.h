#ifndef MODEL_H
#define MODEL_H

#include <QAbstractTableModel>

class ResultsModel : public QAbstractTableModel
{
    Q_OBJECT

public:
    ResultsModel(QObject *parent);
    int rowCount(const QModelIndex &parent = QModelIndex()) const;
    int columnCount(const QModelIndex &parent = QModelIndex()) const;
    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const;
    QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const;
    void setRows(const int n);

private:
    int rows = 2;
    const int columns = 2;

    QString value(int row, int column) const;
};

#endif // MODEL_H
