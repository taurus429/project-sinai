import sys
from PyQt5.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QApplication,
    QStyledItemDelegate,
    QComboBox,
)
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtCore import Qt, pyqtSignal, QObject, pyqtSlot
import color as cUtil

class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.items = items

    def createEditor(self, parent, option, index):
        # 콤보박스 편집기를 생성합니다.
        editor = QComboBox(parent)
        editor.addItems(self.items)
        return editor

    def setEditorData(self, editor, index):
        # 편집기에 현재 데이터를 설정합니다.
        value = index.data()
        if value in self.items:
            editor.setCurrentText(value)

    def setModelData(self, editor, model, index):
        # 모델에 편집기 데이터를 설정합니다.
        model.setData(index, editor.currentText())


class StudentTableWidget(QTableWidget):
    def __init__(self, students, header, util):
        super().__init__()
        self.util = util
        self.students = students
        self.구분데이터 = self.util.구분코드조회()[1:]
        self.구분색사전 = dict()
        for 구분 in self.구분데이터:
            self.구분색사전[구분[1]] = 구분[2]

        # 헤더 이름을 변환합니다.
        self.header = [col if col != "장결여부" else "장결" for col in header]
        self.header = [col if col != "졸업여부" else "졸업" for col in self.header]
        self.header = [col if col != "리더여부" else "리더" for col in self.header]
        self.header = [col if col != "빠른여부" else "빠른" for col in self.header]

        # 원본 데이터를 복사합니다.
        self.original_data = [row[:] for row in students]

        self.setColumnCount(len(self.header))
        self.setHorizontalHeaderLabels(self.header)
        self.populate_table()

        self.setColumnHidden(0, True)  # uid 컬럼 숨기기

        # 컬럼 너비 설정
        self.setColumnWidth(1, 40)
        self.setColumnWidth(2, 60)
        self.setColumnWidth(3, 40)
        self.setColumnWidth(4, 70)
        self.setColumnWidth(5, 30)
        self.setColumnWidth(6, 120)
        self.setColumnWidth(7, 60)
        self.setColumnWidth(8, 40)
        self.setColumnWidth(9, 40)
        self.setColumnWidth(10, 40)
        self.setColumnWidth(11, 40)
        self.setColumnWidth(12, 40)

        # 정렬 상태를 관리합니다.
        self.sort_states = {col: 0 for col in range(len(self.header))}
        self.last_clicked_column = None

        self.horizontalHeader().sectionClicked.connect(self.handle_header_click)
        self.horizontalHeader().installEventFilter(self)
        self.verticalHeader().hide()

        self.setStyleSheet("QHeaderView::section { background-color: '#F0F0F0'; }")
        listbox = [name for _, name, _, _, _, _, _ in self.구분데이터]
        listbox.append("")

        # Define the items for "장결", "졸업", "리더", "빠른", "또래장" columns.
        status_options = ["✅", "❌"]

        # 드롭다운 설정
        self.setItemDelegateForColumn(
            self.header.index("구분"), ComboBoxDelegate(listbox, self)
        )
        self.setItemDelegateForColumn(
            self.header.index("성별"), ComboBoxDelegate(['남', '여'], self)
        )
        # Apply ComboBoxDelegate to columns 8 to 12 for status options.
        for column_name in ["장결", "졸업", "리더", "빠른", "또래장"]:
            if column_name in self.header:
                self.setItemDelegateForColumn(
                    self.header.index(column_name), ComboBoxDelegate(status_options, self)
                )

        # 데이터가 변경될 때 색깔 업데이트
        self.model().dataChanged.connect(self.update_cell_color)

    def populate_table(self):
        # 테이블에 데이터를 채웁니다.
        self.setRowCount(len(self.students) - 1)
        for row, student in enumerate(self.students[1:]):
            for col, data in enumerate(student):
                if self.header[col] in ("장결", "졸업", "리더", "빠른", "또래장"):
                    data = "✅" if data == 1 else "❌"
                elif self.header[col] in ("사랑장", "구분"):
                    data = "" if data is None else data

                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignCenter)

                # 초기 셀 색깔 설정
                self.set_cell_color(item, col, data)

                self.setItem(row, col, item)

    def set_cell_color(self, item, col, data):
        """셀의 색깔을 데이터에 기반하여 설정합니다."""
        if self.header[col] == "성별":
            if data == "남":
                item.setBackground(QColor(173, 216, 230))  # 연한 파란색
            elif data == "여":
                item.setBackground(QColor(255, 182, 193))  # 연한 분홍색
        elif self.header[col] == "구분":
            color = self.구분색사전.get(data, "#FFFFFF")
            item.setBackground(QColor(color))  # 구분 색상
            item.setForeground(QColor(cUtil.get_contrast_color(color)))


    def update_cell_color(self, top_left, bottom_right):
        """데이터가 변경되었을 때 셀 색깔을 업데이트합니다."""
        for row in range(top_left.row(), bottom_right.row() + 1):
            for col in range(top_left.column(), bottom_right.column() + 1):
                item = self.item(row, col)
                data = item.text() if item else ""
                self.set_cell_color(item, col, data)

    def handle_header_click(self, column_index):
        # 헤더 클릭 시 정렬 상태를 변경합니다.
        if (
            self.last_clicked_column is not None
            and self.last_clicked_column != column_index
        ):
            self.sort_states[self.last_clicked_column] = 0

        self.sort_states[column_index] = (self.sort_states[column_index] + 1) % 2
        self.last_clicked_column = column_index

        if self.sort_states[column_index] == 1:
            self.sortItems(column_index, Qt.AscendingOrder)
            self.horizontalHeader().setSortIndicator(column_index, Qt.AscendingOrder)
        elif self.sort_states[column_index] == 0:
            self.sortItems(column_index, Qt.DescendingOrder)
            self.horizontalHeader().setSortIndicator(column_index, Qt.DescendingOrder)

    def get_changed_data(self):
        # Get only changed data and convert "✅" to 1 and "❌" to 0.
        changed_data = []
        original_data_no_header = self.original_data[1:]
        for row in range(self.rowCount()):
            row_data = []
            changed = False
            for col in range(self.columnCount()):
                item = self.item(row, col)
                data = item.text() if item else ""
                if original_data_no_header[row][col] is None:
                    original_data = None
                elif row < len(original_data_no_header):
                    original_data = str(original_data_no_header[row][col])
                else:
                    original_data = ""

                # Convert "✅" to 1 and "❌" to 0 for comparison.
                if self.header[col] in ("장결", "졸업", "리더", "빠른", "또래장"):
                    data = 1 if data == "✅" else 0
                    original_data = int(original_data) if original_data.isdigit() else original_data

                # Convert "" to None and None to None for comparison.
                if self.header[col] in ("구분", "사랑장"):
                    data = None if data == "" else data
                    original_data = None if original_data == "" else original_data

                # Check if current data differs from the original data.
                if data != original_data:
                    if data is None and original_data is None:
                        continue
                    changed = True

                row_data.append(data)
            if changed:
                changed_data.append(row_data)  # Store the row index and data if changed.
        return changed_data

    def reset_changes(self):
        # 테이블을 원래 데이터로 리셋합니다.
        self.students = [row[:] for row in self.original_data]
        self.populate_table()

    def sort_by_column(self, column_index):
        # 지정된 컬럼에 따라 정렬합니다.
        if self.horizontalHeader().sortIndicatorOrder() == Qt.AscendingOrder:
            self.sortItems(column_index, Qt.AscendingOrder)
            self.horizontalHeader().setSortIndicator(column_index, Qt.DescendingOrder)
        else:
            self.sortItems(column_index, Qt.DescendingOrder)
            self.horizontalHeader().setSortIndicator(column_index, Qt.AscendingOrder)

    def eventFilter(self, obj, event):
        # 이벤트 필터를 적용합니다.
        if obj == self.horizontalHeader() and event.type() == event.MouseMove:
            pos = event.pos()
            index = self.horizontalHeader().logicalIndexAt(pos)

            if index == 1:
                self.setCursor(QCursor(Qt.PointingHandCursor))
            else:
                self.setCursor(QCursor(Qt.ArrowCursor))

            return True
        return super().eventFilter(obj, event)

    def hide_rows_with_absence(self, 장결제외, 졸업제외):
        # "장결" 또는 "졸업"이 포함된 행을 숨깁니다.
        absence_col_index = self.header.index("장결")  # "장결" 컬럼의 인덱스를 찾습니다.
        graduated_col_index = self.header.index(
            "졸업"
        )  # "졸업" 컬럼의 인덱스를 찾습니다.

        # 각 행을 반복하여 기준에 따라 숨기거나 표시합니다.
        for row in range(self.rowCount()):
            # "장결" 및 "졸업" 컬럼의 아이템을 가져옵니다.
            absence_item = self.item(row, absence_col_index)
            graduated_item = self.item(row, graduated_col_index)

            # 플래그에 따라 행을 숨길지 결정합니다.
            hide_row = False

            if 장결제외 and 졸업제외:
                # "장결" 또는 "졸업"이 "✅"인 경우 숨깁니다.
                hide_row = (absence_item and absence_item.text() == "✅") or (
                    graduated_item and graduated_item.text() == "✅"
                )
            elif 장결제외:
                # "장결"이 "✅"인 경우 숨깁니다.
                hide_row = absence_item and absence_item.text() == "✅"
            elif 졸업제외:
                # "졸업"이 "✅"인 경우 숨깁니다.
                hide_row = graduated_item and graduated_item.text() == "✅"

            # 계산된 플래그에 따라 행의 가시성을 설정합니다.
            self.setRowHidden(row, hide_row)

        # 이제 보이는 행의 번호를 다시 매깁니다.
        visible_row_number = 0
        for row in range(self.rowCount()):
            if not self.isRowHidden(row):  # 행이 보이는지 확인합니다.
                visible_row_number += 1
                # 선택적으로 첫 번째 열의 보이는 행 번호를 업데이트합니다.
                # self.setItem(row, 0, QTableWidgetItem(str(visible_row_number)))

        return visible_row_number

    def refresh_data(self):
        """데이터베이스에서 최신 데이터를 가져와 테이블을 새로고침합니다."""
        self.students = self.util.select_all("마을원")  # 최신 데이터를 가져옵니다.
        self.구분데이터 = self.util.구분코드조회()[1:]
        self.구분색사전 = dict()
        for 구분 in self.구분데이터:
            self.구분색사전[구분[1]] = 구분[2]
        self.original_data = [row[:] for row in self.students]  # 원본 데이터 복사본을 업데이트합니다.
        self.populate_table()  # 테이블을 다시 채웁니다.


if __name__ == "__main__":
    import util

    util = util.Util()
    students = util.select_all("마을원")
    header = ["uid"] + students[0][1:]

    app = QApplication(sys.argv)

    # 학생 테이블 위젯을 생성합니다.
    student_table_widget = StudentTableWidget(students, header, util)
    student_table_widget.resize(600, 400)
    student_table_widget.show()

    sys.exit(app.exec_())
