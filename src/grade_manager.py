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
from PyQt5.QtCore import Qt
import util

class GradeManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("등급 관리")
        self.setGeometry(100, 100, 320, 300)
        self.util = util.Util()

        # 예시 데이터 초기화
        self.grades = self.util.구분코드조회()[1:]

        # 메인 레이아웃
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # 테이블 위젯
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["UID", "구분", "색깔", "설명", "자동할당"])
        self.table.cellDoubleClicked.connect(self.change_color)  # 셀 클릭 이벤트 연결
        self.table.setColumnWidth(1, 40)
        self.table.setColumnWidth(2, 70)
        self.table.setColumnWidth(3, 90)
        self.table.setColumnWidth(4, 60)
        self.layout.addWidget(self.table)

        # UID 열을 숨깁니다.
        self.table.setColumnHidden(0, True)

        # 버튼 레이아웃
        self.button_layout = QHBoxLayout()

        self.add_button = QPushButton("추가")
        self.add_button.clicked.connect(self.add_grade)
        self.button_layout.addWidget(self.add_button)

        self.update_button = QPushButton("업데이트")
        self.update_button.clicked.connect(self.update_grade)
        self.button_layout.addWidget(self.update_button)

        self.delete_button = QPushButton("삭제")
        self.delete_button.clicked.connect(self.delete_grade)
        self.button_layout.addWidget(self.delete_button)

        self.layout.addLayout(self.button_layout)

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
        new_uid = max(uid for uid, _, _ in self.grades) + 1 if self.grades else 1
        self.grades.append((new_uid, grade_name, grade_color.name(), "", "❌"))
        self.refresh_table()

    def update_grade(self):
        """
        Print the current grades data as a list of dictionaries.
        """
        # Extract the grades data from the table
        grades_list = []
        for row in range(self.table.rowCount()):
            uid = self.table.item(row, 0).text()
            name = self.table.item(row, 1).text()
            color = self.table.item(row, 2).text()
            desc = self.table.item(row, 3).text()
            auto = self.table.cellWidget(row, 4).currentText()

            # Append the grade data as a dictionary
            grades_list.append({
                "UID": uid,
                "Name": name,
                "Color": color,
                "Desc": desc,
                "Auto": auto
            })
        self.util.업데이트_구분(grades_list)
        QMessageBox.information(self, '저장 완료', '저장에 성공했습니다', QMessageBox.Ok)

    def delete_grade(self):
        current_row = self.table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "경고", "삭제할 등급을 선택하세요.")
            return

        del self.grades[current_row]
        self.refresh_table()

    def refresh_table(self):
        self.table.setRowCount(len(self.grades))
        for row, (uid, name, color, desc, auto) in enumerate(self.grades):
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

            self.table.setItem(row, 0, uid_item)
            self.table.setItem(row, 1, name_item)
            self.table.setItem(row, 2, color_item)
            self.table.setItem(row, 3, desc_item)
            self.table.setCellWidget(row, 4, auto_combobox)

            # 가운데 정렬 설정
            name_item.setTextAlignment(Qt.AlignCenter)
            auto_combobox.setStyleSheet("QComboBox { text-align: center; }")

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
                self.grades[row] = (self.grades[row][0], self.grades[row][1], new_color.name(), self.grades[row][3], self.grades[row][4])
                self.refresh_table()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GradeManager()
    window.show()
    sys.exit(app.exec_())
