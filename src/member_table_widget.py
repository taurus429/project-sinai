import sys
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QApplication
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtCore import Qt
import util

class StudentTableWidget(QTableWidget):
    def __init__(self, students, header, util):
        super().__init__()
        self.util = util
        self.students = students

        # '장결여부'를 '장결'로 변경
        self.header = [col if col != '장결여부' else '장결' for col in header]
        self.header = [col if col != '졸업여부' else '졸업' for col in self.header]
        self.header = [col if col != '리더여부' else '리더' for col in self.header]

        self.original_data = [row[:] for row in students]  # 원본 데이터를 저장

        self.setColumnCount(len(self.header))
        self.setHorizontalHeaderLabels(self.header)
        self.populate_table()

        # uid 컬럼 숨기기
        self.setColumnHidden(0, True)  # 0번째 인덱스 컬럼 숨기기

        # 컬럼 너비 고정
        self.setColumnWidth(1, 60)
        self.setColumnWidth(2, 40)
        self.setColumnWidth(3, 70)
        self.setColumnWidth(4, 30)
        self.setColumnWidth(5, 120)
        self.setColumnWidth(6, 60)
        self.setColumnWidth(7, 30)
        self.setColumnWidth(8, 30)
        self.setColumnWidth(9, 30)

        # 각 컬럼에 대한 정렬 상태 초기화
        self.sort_states = {col: 0 for col in range(len(self.header))}
        self.last_clicked_column = None  # 마지막으로 클릭한 컬럼 인덱스 추적

        # 헤더 클릭 이벤트를 커스텀 정렬 메서드에 연결
        self.horizontalHeader().sectionClicked.connect(self.handle_header_click)
        # 헤더에 마우스 이동 이벤트를 연결
        self.horizontalHeader().installEventFilter(self)

        # 헤더 스타일을 연한 회색으로 설정
        self.setStyleSheet("QHeaderView::section { background-color: '#F0F0F0'; }")

    def populate_table(self):
        self.setRowCount(len(self.students) - 1)  # 헤더 행을 제외한 행 수 설정
        for row, student in enumerate(self.students[1:]):
            for col, data in enumerate(student):
                # '장결' 컬럼의 데이터 변환
                if self.header[col] in ('장결', '졸업', '리더'):
                    data = '✅' if data == 1 else '❌'

                item = QTableWidgetItem(str(data))

                # 텍스트 가운데 정렬
                item.setTextAlignment(Qt.AlignCenter)

                # '성별' 컬럼의 배경 색상 설정
                if self.header[col] == '성별':  # '성별' 컬럼 확인
                    if data == "남":
                        item.setBackground(QColor(173, 216, 230))  # 남성용 연한 파란색
                    else:
                        item.setBackground(QColor(255, 182, 193))  # 여성용 연한 분홍색

                self.setItem(row, col, item)

    def handle_header_click(self, column_index):
        """
        헤더 클릭 시 정렬 로직을 처리하는 메서드입니다.
        """
        # 다른 컬럼이 클릭되면 이전의 컬럼 정렬 상태를 초기화
        if self.last_clicked_column is not None and self.last_clicked_column != column_index:
            self.sort_states[self.last_clicked_column] = 0

        # 다음 정렬 상태 결정
        self.sort_states[column_index] = (self.sort_states[column_index] + 1) % 2  # 0: 초기 상태, 1: 오름차순, 2: 내림차순 (최대 두 가지 상태)
        self.last_clicked_column = column_index

        # 첫 번째 클릭 시 오름차순 정렬
        if self.sort_states[column_index] == 1:
            self.sortItems(column_index, Qt.AscendingOrder)
            self.horizontalHeader().setSortIndicator(column_index, Qt.AscendingOrder)
        # 두 번째 클릭 시 내림차순 정렬
        elif self.sort_states[column_index] == 0:
            self.sortItems(column_index, Qt.DescendingOrder)
            self.horizontalHeader().setSortIndicator(column_index, Qt.DescendingOrder)

    def get_changed_data(self):
        """
        테이블의 변경된 데이터를 가져옵니다.
        """
        changed_data = []
        for row in range(self.rowCount()):
            row_data = []
            for col in range(self.columnCount()):
                item = self.item(row, col)
                row_data.append(item.text() if item else "")
            changed_data.append(row_data)
        return changed_data

    def reset_changes(self):
        """
        테이블의 변경 사항을 원본 데이터로 되돌립니다.
        """
        self.students = [row[:] for row in self.original_data]
        self.populate_table()

    def sort_by_column(self, column_index):
        """
        특정 컬럼을 기준으로 정렬합니다.
        """
        if self.horizontalHeader().sortIndicatorOrder() == Qt.AscendingOrder:
            self.sortItems(column_index, Qt.AscendingOrder)
            self.horizontalHeader().setSortIndicator(column_index, Qt.DescendingOrder)
        else:
            self.sortItems(column_index, Qt.DescendingOrder)
            self.horizontalHeader().setSortIndicator(column_index, Qt.AscendingOrder)

    def eventFilter(self, obj, event):
        """
        이벤트 필터를 사용하여 헤더의 마우스 커서를 변경합니다.
        """
        if obj == self.horizontalHeader() and event.type() == event.MouseMove:
            pos = event.pos()
            index = self.horizontalHeader().logicalIndexAt(pos)

            # '이름' 컬럼 확인 및 커서 변경
            if index == 1:  # Assuming '이름' is at column index 1
                self.setCursor(QCursor(Qt.PointingHandCursor))
            else:
                self.setCursor(QCursor(Qt.ArrowCursor))

            return True  # Event is handled
        return super().eventFilter(obj, event)

if __name__ == "__main__":
    util = util.Util()
    students = util.select_all("마을원")
    header = ['uid'] + students[0][1:]  # 헤더가 데이터베이스 구조와 일치하는지 확인

    app = QApplication(sys.argv)
    window = StudentTableWidget(students, header, util)

    # 윈도우 크기 설정
    window.resize(600, 400)  # 너비: 600, 높이: 400

    window.show()
    sys.exit(app.exec_())
