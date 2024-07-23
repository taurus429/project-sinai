import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QColorDialog,
    QLabel,
    QHBoxLayout,
    QLineEdit,
    QCheckBox
)
from PyQt5.QtGui import QColor, QPainter, QPainterPath
from PyQt5.QtCore import Qt, QRectF
from util import Util

class CustomLabel(QLabel):
    def __init__(self, text='', bgcolor='#FFFFFF', fgcolor='#000000', parent=None):
        super().__init__(parent)
        self.text = text
        self.bgcolor = bgcolor
        self.fgcolor = fgcolor


    def setColors(self, bgcolor, fgcolor):
        self.bgcolor = bgcolor
        self.fgcolor = fgcolor
        self.update()

    def setText(self, text):
        self.text = text
        self.update()

    def paintEvent(self, event):
        # QPainter를 사용하여 둥근 모서리의 사각형 그리기
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 안티앨리어싱 활성화

        # 배경색 설정
        painter.setBrush(QColor(self.bgcolor))
        painter.setPen(Qt.NoPen)  # 윤곽선 없앰

        # 둥근 모서리 사각형 경로 생성
        rect_path = QPainterPath()
        rect_path.addRoundedRect(QRectF(self.rect()), 10, 10)  # 10은 모서리 둥글기 정도

        # 사각형 그리기
        painter.drawPath(rect_path)

        # 글자색 설정
        painter.setPen(QColor(self.fgcolor))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text)  # 중앙 정렬로 텍스트 그리기


class MeetingItem(QWidget):
    def __init__(self, name='', bgcolor='#FFFFFF', fgcolor='#000000'):
        super().__init__()
        self.initUI(name, bgcolor, fgcolor)

    def initUI(self, name, bgcolor, fgcolor):
        self.layout = QHBoxLayout()

        self.nameEdit = QLineEdit(name)
        self.nameEdit.setFixedWidth(150)
        self.nameEdit.textChanged.connect(self.updateName)  # 이름 변경시 미리보기 업데이트

        # 배경색 선택 라벨
        self.bgColorLabel = QLabel()
        self.bgColorLabel.setText(bgcolor)
        self.bgColorLabel.setStyleSheet(f'background-color: {bgcolor}')
        self.bgColorLabel.setFixedWidth(100)
        self.bgColorLabel.setAlignment(Qt.AlignCenter)
        self.bgColorLabel.mousePressEvent = self.changeBgColor

        # 글자색 선택 라벨
        self.fgColorLabel = QLabel()
        self.fgColorLabel.setText(fgcolor)
        self.fgColorLabel.setStyleSheet(f'background-color: {fgcolor}')
        self.fgColorLabel.setFixedWidth(100)
        self.fgColorLabel.setAlignment(Qt.AlignCenter)
        self.fgColorLabel.mousePressEvent = self.changeFgColor

        # CustomLabel을 사용한 미리보기
        self.previewLabel = CustomLabel(name, bgcolor, fgcolor)
        self.previewLabel.setFixedSize(100, 30)

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
            self.updatePreview(self.nameEdit.text(), color.name(), self.fgColorLabel.text())

    def changeFgColor(self, event):
        color = QColorDialog.getColor()
        if color.isValid():
            self.fgColorLabel.setText(color.name())
            self.fgColorLabel.setStyleSheet(f'background-color: {color.name()}')
            self.updatePreview(self.nameEdit.text(), self.bgColorLabel.text(), color.name())

    def updateName(self, text):
        self.updatePreview(text, self.bgColorLabel.text(), self.fgColorLabel.text())

    def updatePreview(self, text, bgcolor, fgcolor):
        # CustomLabel의 색상 및 텍스트 업데이트
        self.previewLabel.setText(text)
        self.previewLabel.setColors(bgcolor, fgcolor)

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
        self.util = Util()
        meetings = self.util.모임코드조회()

        for _, name, bgcolor, fgcolor in meetings[0].values():
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
