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
)
from PyQt5.QtGui import QColor
import util

class GradeManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("등급 관리")
        self.setGeometry(100, 100, 200, 300)
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
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["UID", "등급 이름", "색깔"])
        self.table.cellDoubleClicked.connect(self.change_color)  # 셀 클릭 이벤트 연결
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
        self.grades.append((new_uid, grade_name, grade_color.name()))
        self.refresh_table()

    def update_grade(self):
        current_row = self.table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "경고", "업데이트할 등급을 선택하세요.")
            return

        grade_name, ok_pressed = self.get_grade_name(
            initial_text=self.grades[current_row][1]
        )
        if not ok_pressed or not grade_name.strip():
            return

        grade_color = self.get_color(initial_color=self.grades[current_row][2])
        if not grade_color:
            return

        uid = self.grades[current_row][0]  # 기존 uid 유지
        self.grades[current_row] = (uid, grade_name, grade_color.name())
        self.refresh_table()

    def delete_grade(self):
        current_row = self.table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "경고", "삭제할 등급을 선택하세요.")
            return

        del self.grades[current_row]
        self.refresh_table()

    def refresh_table(self):
        self.table.setRowCount(len(self.grades))
        for row, (uid, name, color) in enumerate(self.grades):
            uid_item = QTableWidgetItem(str(uid))
            name_item = QTableWidgetItem(name)
            color_item = QTableWidgetItem(color)
            color_item.setBackground(QColor(color))

            self.table.setItem(row, 0, uid_item)
            self.table.setItem(row, 1, name_item)
            self.table.setItem(row, 2, color_item)

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
                self.grades[row] = (self.grades[row][0], self.grades[row][1], new_color.name())
                self.refresh_table()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GradeManager()
    window.show()
    sys.exit(app.exec_())