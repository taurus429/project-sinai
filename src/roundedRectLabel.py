from PyQt5.QtWidgets import QWidget, QToolTip
from PyQt5.QtGui import QPainter, QColor, QFontMetrics, QCursor
from PyQt5.QtCore import Qt, QRect, QSize, QPoint
from util import Util
class RoundedRectLabel(QWidget):
    def __init__(self, code, date):
        super().__init__()
        self.util = Util()
        code2desc, desc2code = self.util.모임코드조회()
        self.info = code2desc[int(code)]
        self.text = self.info[1]
        self.setMinimumSize(20, 20)  # 최소 크기 설정 (가로, 세로)
        self.setMouseTracking(True)  # 마우스 움직임 추적 활성화
        self.tooltip_info = [date]

    def getToolTipText(self):
        text = f"<b>{self.tooltip_info[0]}</b><br>{self.text}"
        return text

    def enterEvent(self, event):
        tooltip_height = self.calculate_tooltip_height()
        cursor_pos = QCursor.pos()
        tooltip_pos = cursor_pos + QPoint(0, -tooltip_height)
        QToolTip.showText(tooltip_pos, self.getToolTipText(), self, self.rect(), 3000)
        super().enterEvent(event)

    def leaveEvent(self, event):
        QToolTip.hideText()  # 툴팁 숨기기
        super().leaveEvent(event)

    def mouseMoveEvent(self, event):
        tooltip_height = self.calculate_tooltip_height()
        cursor_pos = QCursor.pos()
        tooltip_pos = cursor_pos + QPoint(0, -tooltip_height)
        QToolTip.showText(tooltip_pos, self.getToolTipText(), self, self.rect(), 3000)
        super().mouseMoveEvent(event)

    def calculate_tooltip_height(self):
        # QFontMetrics를 사용하여 텍스트의 높이 계산
        font_metrics = QFontMetrics(QToolTip.font())
        text_height = font_metrics.height()
        line_count = f"<b>안내</b><br>{self.text}".count("<br>") + 1
        total_height = text_height * line_count + 35  # 텍스트 라인 수에 따라 높이 계산 (패딩 포함)
        return total_height

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 안티앨리어싱 활성화

        rect = event.rect()  # 위젯의 사각형 영역
        rect.adjust(2, 2, -2, -2)  # 사각형을 약간 안쪽으로 줄임
        painter.setBrush(QColor(self.info[2]))  # default 색상 설정

        painter.drawRoundedRect(rect, 5, 5)  # 둥근 직사각형 그리기

        font_metrics = QFontMetrics(self.font())  # 현재 폰트 메트릭스
        text_width = font_metrics.horizontalAdvance(self.text)  # 텍스트의 너비 계산
        text_height = font_metrics.height()  # 텍스트의 높이 계산
        text_rect = QRect(rect.left() + 2, rect.top() + 3, text_width, text_height)  # 텍스트 위치 지정

        painter.setPen(QColor(self.info[3]))  # 펜 색상 설정
        painter.drawText(text_rect, Qt.AlignCenter, self.text)  # 텍스트를 중앙 정렬하여 그리기

    def sizeHint(self):
        font_metrics = QFontMetrics(self.font())  # 현재 폰트 메트릭스
        text_width = font_metrics.horizontalAdvance(self.text)  # 텍스트의 너비 계산
        text_height = font_metrics.height()  # 텍스트의 높이 계산
        return QSize(text_width + 10, text_height + 10)  # 위젯의 기본 크기 지정
