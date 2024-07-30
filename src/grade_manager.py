import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QColorDialog,
    QHBoxLayout,
    QMessageBox,
    QInputDialog,
    QComboBox,
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, pyqtSignal
import util

class GradeManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("등급 관리")
        self.setGeometry(100, 100, 410, 430)  # Width adjusted to accommodate the new column
        self.util = util.Util()

        # 예시 데이터 초기화
        self.grades = self.util.구분코드조회()[1:]

        # Store the last saved state
        self.saved_grades = self.grades.copy()

        # List to store deleted UIDs
        self.deleted_uids = []

        # 메인 레이아웃
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # 테이블 위젯
        self.table = QTableWidget()
        self.table.setColumnCount(7)  # Adjust column count for the new "순서" column
        self.table.setHorizontalHeaderLabels(["UID", "구분", "색깔", "설명", "자동할당", "사랑배치", "순서"])
        self.table.cellDoubleClicked.connect(self.change_color)  # 셀 클릭 이벤트 연결
        self.table.setColumnWidth(1, 40)
        self.table.setColumnWidth(2, 70)
        self.table.setColumnWidth(3, 90)
        self.table.setColumnWidth(4, 60)
        self.table.setColumnWidth(5, 60)
        self.table.setColumnWidth(6, 40)  # Set width for the "순서" column
        self.layout.addWidget(self.table)

        # UID 열을 숨깁니다.
        self.table.setColumnHidden(0, True)

        # 버튼 레이아웃
        self.button_layout_top = QHBoxLayout()
        self.button_layout_bottom = QHBoxLayout()

        # 행 이동 버튼 추가 (상단 버튼 레이아웃)
        self.move_up_button = QPushButton("위로 이동")
        self.move_up_button.clicked.connect(self.move_row_up)
        self.button_layout_top.addWidget(self.move_up_button)

        self.move_down_button = QPushButton("아래로 이동")
        self.move_down_button.clicked.connect(self.move_row_down)
        self.button_layout_top.addWidget(self.move_down_button)

        # 하단 버튼 레이아웃에 나머지 버튼 추가
        self.add_button = QPushButton("추가")
        self.add_button.clicked.connect(self.add_grade)
        self.button_layout_bottom.addWidget(self.add_button)

        self.update_button = QPushButton("변경내용 저장")
        self.update_button.clicked.connect(self.update_grade)
        self.button_layout_bottom.addWidget(self.update_button)

        self.delete_button = QPushButton("삭제")
        self.delete_button.clicked.connect(self.delete_grade)
        self.button_layout_bottom.addWidget(self.delete_button)

        # 변경 초기화 버튼 추가
        self.reset_button = QPushButton("변경 초기화")
        self.reset_button.clicked.connect(self.reset_changes)
        self.button_layout_bottom.addWidget(self.reset_button)

        # 상단 버튼 레이아웃과 하단 버튼 레이아웃을 각각 추가
        self.layout.addLayout(self.button_layout_top)
        self.layout.addLayout(self.button_layout_bottom)

        # 초기 테이블 데이터 로드
        self.refresh_table()

    def add_grade(self):
        grade_name, ok_pressed = self.get_grade_name()
        if not ok_pressed or not grade_name.strip():
            return

        grade_color = self.get_color()
        if not grade_color:
            return

        # 새 uid는 현재 최대 uid + 1로 설정
        new_uid = max(uid for uid, _, _, _, _, _, _ in self.grades) + 1 if self.grades else 1
        new_ord = max(order for _, _, _, _, _, _, order in self.grades) + 1 if self.grades else 1
        self.grades.append((new_uid, grade_name, grade_color.name(), "", 0, 0, new_ord))
        self.refresh_table()

    def update_grade(self):
        # Extract the grades data from the table
        grades_list = []
        for row in range(self.table.rowCount()):
            uid = int(self.table.item(row, 0).text())
            name = self.table.item(row, 1).text()
            color = self.table.item(row, 2).text()
            desc = self.table.item(row, 3).text()
            auto = self.table.cellWidget(row, 4).currentText()
            allo = self.table.cellWidget(row, 5).currentText()
            order = int(self.table.item(row, 6).text())

            allo = 1 if allo == "✅" else 0
            auto = 1 if auto == "✅" else 0
            # Append the grade data as a dictionary
            grades_list.append({
                "코드": uid,
                "구분이름": name,
                "구분색깔": color,
                "설명": desc,
                "자동할당": auto,
                "사랑배치": allo,
                "순서": order
            })
        self.util.업데이트_구분(grades_list)
        QMessageBox.information(self, '저장 완료', '저장에 성공했습니다', QMessageBox.Ok)

        # Update the saved state
        self.saved_grades = self.grades.copy()

        # Clear the deleted UIDs list after update
        self.deleted_uids.clear()

    def delete_grade(self):
        current_row = self.table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "경고", "삭제할 등급을 선택하세요.")
            return

        # Store the UID of the deleted row
        deleted_uid = int(self.table.item(current_row, 0).text())
        self.deleted_uids.append(deleted_uid)

        del self.grades[current_row]
        self.refresh_table()

    def refresh_table(self):
        self.table.setRowCount(len(self.grades))
        for row, (uid, name, color, desc, auto, allo, order) in enumerate(self.grades):
            uid_item = QTableWidgetItem(str(uid))
            name_item = QTableWidgetItem(name)
            color_item = QTableWidgetItem(color)
            color_item.setBackground(QColor(color))
            desc_item = QTableWidgetItem(desc)

            # 자동할당 드롭다운 박스
            auto_combobox = QComboBox()
            auto_combobox.addItems(["✅", "❌"])
            auto = "✅" if auto == 1 else "❌"
            auto_combobox.setCurrentText(auto)

            # allo할당 드롭다운 박스
            allo_combobox = QComboBox()
            allo_combobox.addItems(["✅", "❌"])
            allo = "✅" if allo == 1 else "❌"
            allo_combobox.setCurrentText(allo)

            # 순서 아이템 생성
            order_item = QTableWidgetItem(str(row+1))
            order_item.setFlags(order_item.flags() & ~Qt.ItemIsEditable)  # Make "순서" column non-editable
            order_item.setTextAlignment(Qt.AlignCenter)

            self.table.setItem(row, 0, uid_item)
            self.table.setItem(row, 1, name_item)
            self.table.setItem(row, 2, color_item)
            self.table.setItem(row, 3, desc_item)
            self.table.setCellWidget(row, 4, auto_combobox)
            self.table.setCellWidget(row, 5, allo_combobox)
            self.table.setItem(row, 6, order_item)

            # 가운데 정렬 설정
            name_item.setTextAlignment(Qt.AlignCenter)
            auto_combobox.setStyleSheet("QComboBox { text-align: center; }")

    def reset_changes(self):
        # Reset the grades data to the last saved state
        self.grades = self.saved_grades.copy()
        self.deleted_uids.clear()  # Clear the list of deleted UIDs
        self.refresh_table()

    def get_color(self, initial_color="#FFFFFF"):
        color = QColorDialog.getColor(QColor(initial_color), self, "색깔 선택")
        if color.isValid():
            return color
        return None

    def get_grade_name(self, initial_text=""):
        name, ok_pressed = QInputDialog.getText(
            self, "등급 이름", "등급 이름을 입력하세요:", text=initial_text
        )
        return name, ok_pressed

    def change_color(self, row, column):
        # 색깔 열에서만 작동
        if column == 2:
            current_color = self.grades[row][2]
            new_color = self.get_color(initial_color=current_color)

            if new_color:
                self.grades[row] = (
                    self.grades[row][0],
                    self.grades[row][1],
                    new_color.name(),
                    self.grades[row][3],
                    self.grades[row][4],
                    self.grades[row][5],
                    self.grades[row][6]
                )
                self.refresh_table()

    def move_row_up(self):
        current_row = self.table.currentRow()
        if current_row > 0:
            self.swap_rows(current_row, current_row - 1)

    def move_row_down(self):
        current_row = self.table.currentRow()
        if current_row < self.table.rowCount() - 1:
            self.swap_rows(current_row, current_row + 1)

    def swap_rows(self, row1, row2):
        # Swap the grades data
        self.grades[row1], self.grades[row2] = self.grades[row2], self.grades[row1]
        # Refresh table to reflect the swapped rows
        self.refresh_table()

        # Set the current row to the new row position
        self.table.setCurrentCell(row2, 0)

        # 순서 업데이트는 필요 없음, refresh_table에서 자동으로 설정됨

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GradeManager()
    window.show()
    sys.exit(app.exec_())
