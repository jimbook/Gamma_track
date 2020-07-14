"""
Created on 2013-7-2
@author: badboy
Email:lucky.haiyu@gmail.com
QQ:43831266
"""
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class clockForm(QWidget):
    def __init__(self, parent=None):
        super(clockForm, self).__init__(parent)
        self.setWindowTitle("Clock")
        self.timer = QTimer()
        # 设置窗口计时器
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 设置表盘中的文字字体
        font = QFont("Times", 6)
        fm = QFontMetrics(font)
        fontRect = fm.boundingRect("99")  # 获取绘制字体的矩形范围

        # 分针坐标点
        minPoints = [QPointF(50, 25),
                     QPointF(48, 50),
                     QPointF(52, 50)]

        # 时钟坐标点
        hourPoints = [QPointF(50, 35),
                      QPointF(48, 50),
                      QPointF(52, 50)]

        side = min(self.width(), self.height())
        painter.setViewport((self.width() - side) / 2, (self.height() - side) / 2,
                            side, side)  # 始终处于窗口中心位置显示

        # 设置QPainter的坐标系统，无论窗体大小如何变化，
        # 窗体左上坐标为(0,0),右下坐标为(100,100),
        # 因此窗体中心坐标为(50,50)
        painter.setWindow(0, 0, 100, 100)

        # 绘制表盘，使用环形渐变色
        niceBlue = QColor(150, 150, 200)
        haloGrident = QRadialGradient(50, 50, 50, 50, 50)
        haloGrident.setColorAt(0.0, Qt.lightGray)
        haloGrident.setColorAt(0.5, Qt.darkGray)
        haloGrident.setColorAt(0.9, Qt.white)
        haloGrident.setColorAt(1.0, niceBlue)
        painter.setBrush(haloGrident)
        painter.setPen(QPen(Qt.darkGray, 1))
        painter.drawEllipse(0, 0, 100, 100)

        transform = QTransform()

        # 绘制时钟为0的字，以及刻度
        painter.setPen(QPen(Qt.black, 1.5))
        fontRect.moveCenter(QPoint(50, 10 + fontRect.height() / 2))
        painter.setFont(font)
        painter.drawLine(50, 2, 50, 8)  #
        painter.drawText(QRectF(fontRect), Qt.AlignHCenter | Qt.AlignTop, "0")

        for i in range(1, 12):
            transform.translate(50, 50)
            transform.rotate(30)
            transform.translate(-50, -50)
            painter.setWorldTransform(transform)
            painter.drawLine(50, 2, 50, 8)
            painter.drawText(QRectF(fontRect), Qt.AlignHCenter | Qt.AlignTop, "%d" % i)

        transform.reset()

        # 绘制分钟刻度线
        painter.setPen(QPen(Qt.blue, 1))
        for i in range(1, 60):
            transform.translate(50, 50)
            transform.rotate(6)
            transform.translate(-50, -50)
            if i % 5 != 0:
                painter.setWorldTransform(transform)
                painter.drawLine(50, 2, 50, 5)

        transform.reset()

        # 获取当前时间
        currentTime = QTime().currentTime()
        hour = currentTime.hour() if currentTime.hour() < 12 else currentTime.hour() - 12
        minite = currentTime.minute()
        second = currentTime.second()

        # 获取所需旋转角度
        hour_angle = hour * 30.0 + (minite / 60.0) * 30.0
        minite_angle = (minite / 60.0) * 360.0
        second_angle = second * 6.0

        # 时针
        transform.translate(50, 50)
        transform.rotate(hour_angle)
        transform.translate(-50, -50)
        painter.setWorldTransform(transform)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(Qt.darkRed))
        painter.drawPolygon(QPolygonF(hourPoints))

        transform.reset()

        # 分针
        transform.translate(50, 50)
        transform.rotate(minite_angle)
        transform.translate(-50, -50)
        painter.setWorldTransform(transform)
        painter.setBrush(QBrush(Qt.darkGreen))
        painter.drawPolygon(QPolygonF(minPoints))

        transform.reset()
        # 秒针
        transform.translate(50, 50)
        transform.rotate(second_angle)
        transform.translate(-50, -50)
        painter.setWorldTransform(transform)
        painter.setPen(QPen(Qt.darkCyan, 1))
        painter.drawLine(50, 50, 50, 20)


import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt

df = pd.DataFrame({'a': ['Mary', 'Jim', 'John'],
                   'b': [100, 200, 300],
                   'c': ['a', 'b', 'c']})

class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = pandasModel(df)
    view = QTableView()
    view.setModel(model)
    view.resize(800, 600)
    df = df.append(pd.Series([2.3,596,99],name="d"))
    model = pandasModel(df)
    view = QTableView()
    view.setModel(model)
    view.show()
    sys.exit(app.exec_())