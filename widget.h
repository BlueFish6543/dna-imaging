#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>
#include <QDir>

namespace Ui {
class Widget;
}

class Widget : public QWidget
{
    Q_OBJECT

public:
    explicit Widget(QWidget *parent = 0);
    ~Widget();

private:
    Ui::Widget *ui;
    QString directory = QDir::currentPath();
    QString fileName = "";
    const char *imageFileName;

    int numColumns = 5;
    int numColours = 8;
    int ladderThreshold = 5;
    int sampleThreshold = 3;

    int ladderBands = -1;

private slots:
    void selectFile();
    void loadImage();
    void setColumns();
    void setColours();
    void setLadderThreshold();
    void setSampleThreshold();
};

#endif // WIDGET_H
