#include "widget.h"
#include "ui_widget.h"
#include "model.h"
#include <QFileDialog>

Widget::Widget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Widget)
{
    ui->setupUi(this);
    connect(ui->selectFile, SIGNAL(clicked()), this, SLOT(selectFile()));
    connect(ui->loadImage, SIGNAL(clicked()), this, SLOT(loadImage()));

    ui->columns->setMinimum(2);
    ui->columns->setValue(numColumns);
    ui->colours->setMinimum(4);
    ui->colours->setValue(numColours);
    ui->ladderThreshold->setMinimum(1);
    ui->ladderThreshold->setMaximum(numColours);
    ui->ladderThreshold->setValue(ladderThreshold);
    ui->sampleThreshold->setMinimum(1);
    ui->sampleThreshold->setMaximum(numColours);
    ui->sampleThreshold->setValue(sampleThreshold);

    connect(ui->columns, SIGNAL(valueChanged(int)), this, SLOT(setColumns()));
    connect(ui->colours, SIGNAL(valueChanged(int)), this, SLOT(setColours()));
    connect(ui->ladderThreshold, SIGNAL(valueChanged(int)), this, SLOT(setLadderThreshold()));
    connect(ui->sampleThreshold, SIGNAL(valueChanged(int)), this, SLOT(setSampleThreshold()));

    ui->calibrationText->setText(QString("No ladder bands detected."));

    ResultsModel *model = new ResultsModel(0);
    ui->results->setModel(model);
    ui->results->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
    ui->results->show();
}

Widget::~Widget()
{
    delete ui;
}

void Widget::selectFile()
{
    fileName = QFileDialog::getOpenFileName(
        this, tr("Select File"), directory, tr("Images (*.png *.jpg)"));
    ui->lineEdit->setText(fileName);
    QFileInfo f(fileName);
    directory = f.absolutePath();
}

void Widget::loadImage()
{
    if (fileName.isEmpty())
    {
        return;
    }
    else
    {
        QPixmap pic(fileName);
        int w = ui->picture->width();
        int h = ui->picture->height();
        ui->picture->setPixmap(pic.scaled(w, h, Qt::KeepAspectRatio));
        ui->picture->setAlignment(Qt::AlignCenter);
    }
}

void Widget::setColumns()
{
    numColumns = ui->columns->value();
}

void Widget::setColours()
{
    numColours = ui->colours->value();
    ui->ladderThreshold->setMaximum(numColours);
    ui->sampleThreshold->setMaximum(numColours);
}

void Widget::setLadderThreshold()
{
    ladderThreshold = ui->ladderThreshold->value();
}

void Widget::setSampleThreshold()
{
    sampleThreshold = ui->sampleThreshold->value();
}
