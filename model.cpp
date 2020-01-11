#include "model.h"

ResultsModel::ResultsModel(QObject *parent)
    :QAbstractTableModel(parent)
{
}

int ResultsModel::rowCount(const QModelIndex &parent) const
{
    return rows;
}

int ResultsModel::columnCount(const QModelIndex &parent) const
{
    return columns;
}

QVariant ResultsModel::data(const QModelIndex &index, int role) const
{
    if (role == Qt::DisplayRole)
    {
        int row = index.row();
        int column = index.column();
        return value(row, column);
    }
    return QVariant();
}

QVariant ResultsModel::headerData(int section, Qt::Orientation orientation, int role) const
{
    if (role == Qt::DisplayRole)
    {
        if (orientation == Qt::Horizontal)
        {
            switch (section)
            {
            case 0:
                return QString("Column");
                break;
            case 1:
                return QString("Value");
                break;
            }
        }
    }
    return QVariant();
}

void ResultsModel::setRows(const int n)
{
    rows = n;
}

QString ResultsModel::value(int row, int column) const
{
    return QString("Test");
}
