import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton,
                             QColorDialog, QLabel, QHBoxLayout, QLineEdit, QCheckBox)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt


class MeetingItem(QWidget):
    def __init__(self, name='', bgcolor='#FFFFFF', fgcolor='#000000'):
        super().__init__()
        self.initUI(name, bgcolor, fgcolor)

    def initUI(self, name, bgcolor, fgcolor):
        self.layout = QHBoxLayout()

        self.nameEdit = QLineEdit(name)
        self.nameEdit.setFixedWidth(150)

        self.bgColorLabel = QLabel()
        self.bgColorLabel.setText(bgcolor)
        self.bgColorLabel.setStyleSheet(f'background-color: {bgcolor}')
        self.bgColorLabel.setFixedWidth(100)
        self.bgColorLabel.setAlignment(Qt.AlignCenter)
        self.bgColorLabel.mousePressEvent = self.changeBgColor

        self.fgColorLabel = QLabel()
        self.fgColorLabel.setText(fgcolor)
        self.fgColorLabel.setStyleSheet(f'background-color: {fgcolor}')
        self.fgColorLabel.setFixedWidth(100)
        self.fgColorLabel.setAlignment(Qt.AlignCenter)
        self.fgColorLabel.mousePressEvent = self.changeFgColor

        self.previewLabel = QLabel('미리보기')
        self.previewLabel.setFixedWidth(100)
        self.updatePreview(bgcolor, fgcolor)

        self.deleteCheckBox = QCheckBox()

        self.layout.addWidget(self.nameEdit)
        self.layout.addWidget(self.bgColorLabel)
        self.layout.addWidget(self.fgColorLabel)
        self.layout.addWidget(self.previewLabel)
        self.layout.addWidget(self.deleteCheckBox)

        self.setLayout(self.layout)

    def changeBgColor(self, event):
        color = QColorDialog.getColor()
        if color.isValid():
            self.bgColorLabel.setText(color.name())
            self.bgColorLabel.setStyleSheet(f'background-color: {color.name()}')
            self.updatePreview(color.name(), self.fgColorLabel.text())

    def changeFgColor(self, event):
        color = QColorDialog.getColor()
        if color.isValid():
            self.fgColorLabel.setText(color.name())
            self.fgColorLabel.setStyleSheet(f'background-color: {color.name()}')
            self.updatePreview(self.bgColorLabel.text(), color.name())

    def updatePreview(self, bgcolor, fgcolor):
        self.previewLabel.setStyleSheet(f'background-color: {bgcolor}; color: {fgcolor}')

    def getName(self):
        return self.nameEdit.text()

    def getBgColor(self):
        return self.bgColorLabel.text()

    def getFgColor(self):
        return self.fgColorLabel.text()

    def isMarkedForDeletion(self):
        return self.deleteCheckBox.isChecked()


class MeetingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.listWidget = QListWidget()
        self.layout.addWidget(self.listWidget)

        self.addHeader()
        self.loadData()

        self.addButton = QPushButton('추가')
        self.addButton.clicked.connect(self.addRow)
        self.layout.addWidget(self.addButton)

        self.saveButton = QPushButton('저장')
        self.saveButton.clicked.connect(self.saveData)
        self.layout.addWidget(self.saveButton)

        self.setLayout(self.layout)
        self.setWindowTitle('모임 관리')
        self.setGeometry(100, 100, 800, 400)
        self.show()

    def addHeader(self):
        header_item = QListWidgetItem(self.listWidget)
        header_widget = QWidget()
        header_layout = QHBoxLayout()

        name_label = QLabel('모임이름')
        name_label.setFixedWidth(150)
        bg_color_label = QLabel('배경색')
        bg_color_label.setFixedWidth(100)
        fg_color_label = QLabel('글자색')
        fg_color_label.setFixedWidth(100)
        preview_label = QLabel('미리보기')
        preview_label.setFixedWidth(100)
        delete_label = QLabel('삭제여부')

        header_layout.addWidget(name_label)
        header_layout.addWidget(bg_color_label)
        header_layout.addWidget(fg_color_label)
        header_layout.addWidget(preview_label)
        header_layout.addWidget(delete_label)

        header_widget.setLayout(header_layout)
        header_item.setSizeHint(header_widget.sizeHint())
        self.listWidget.addItem(header_item)
        self.listWidget.setItemWidget(header_item, header_widget)

    def loadData(self):
        # 더미 데이터 생성
        meetings = [
            ('모임1', '#FF5733', '#000000'),
            ('모임2', '#33FF57', '#000000'),
            ('모임3', '#3357FF', '#FFFFFF')
        ]

        for name, bgcolor, fgcolor in meetings:
            self.addMeetingItem(name, bgcolor, fgcolor)

    def addMeetingItem(self, name, bgcolor, fgcolor):
        item = QListWidgetItem(self.listWidget)
        item_widget = MeetingItem(name, bgcolor, fgcolor)
        item.setSizeHint(item_widget.sizeHint())
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, item_widget)

    def addRow(self):
        self.addMeetingItem('', '#FFFFFF', '#000000')

    def saveData(self):
        for index in range(1, self.listWidget.count()):  # 0번 인덱스는 헤더
            item = self.listWidget.item(index)
            item_widget = self.listWidget.itemWidget(item)
            name = item_widget.getName()
            bgcolor = item_widget.getBgColor()
            fgcolor = item_widget.getFgColor()
            delete = item_widget.isMarkedForDeletion()
            print(f"모임이름: {name}, 배경색: {bgcolor}, 글자색: {fgcolor}, 삭제여부: {delete}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MeetingApp()
    sys.exit(app.exec_())
