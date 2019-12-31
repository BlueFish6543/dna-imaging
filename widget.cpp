#include "widget.h"
#include "ui_widget.h"
#include <QFileDialog>

Widget::Widget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Widget)
{
    ui->setupUi(this);
    connect(ui->selectFile, SIGNAL(clicked()), this, SLOT(openFile()));
}

Widget::~Widget()
{
    delete ui;
}

void Widget::openFile()
{
    fileName = QFileDialog::getOpenFileName(
        this, tr("Select File"), QDir::currentPath(), tr("Images (*.png *.jpg)"));
}
