import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QCheckBox, QSpinBox, \
    QAbstractItemView, QComboBox, QLabel, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
import util
from src.grade_cutoff import GradeCutoff


class GradeSet(QWidget):
    def __init__(self):
        super().__init__()
        self.util = util.Util()
        # 애플리케이션의 메인 레이아웃
        self.main_layout = QVBoxLayout()

        # "통계 시작일" 드롭다운 박스를 추가 및 구성
        self.add_statistics_start_date()

        # 수평 레이아웃 생성 및 구성
        self.horizontal_layout = QHBoxLayout()

        # 테이블 위젯을 생성하고 구성
        self.table_widget = QTableWidget()
        self.setup_table()

        # 간단한 라벨 생성
        self.grade_cutoff = GradeCutoff()
        self.grade_cutoff.setEnabled(False)
        # 수평 레이아웃에 테이블과 라벨 추가
        self.horizontal_layout.addWidget(self.table_widget)
        self.horizontal_layout.addWidget(self.grade_cutoff)

        # '구분 부여' 버튼 추가 및 구성
        self.add_button()

        # 메인 레이아웃에 수평 레이아웃 추가
        self.main_layout.addLayout(self.horizontal_layout)
        self.setLayout(self.main_layout)
        self.setWindowTitle("구분 부여")

    def add_statistics_start_date(self):
        # 드롭다운 박스와 레이블을 위한 레이아웃 생성
        header_layout = QHBoxLayout()

        # 드롭다운 박스에 대한 레이블 생성
        label = QLabel("구분부여 기준일:")

        텀 = self.util.텀조회()[1:]
        dates = []
        for t in 텀:
            dates.append(t[2])
        # 드롭다운 박스 생성
        self.start_date_combo = QComboBox()
        # 드롭다운 목록에 예제 날짜 추가
        self.start_date_combo.addItems(dates)

        # 레이블과 드롭다운 박스를 헤더 레이아웃에 추가
        header_layout.addWidget(label)
        header_layout.addWidget(self.start_date_combo)

        # 메인 레이아웃에 헤더 레이아웃 추가
        self.main_layout.addLayout(header_layout)

    def setup_table(self):
        # 열의 개수 설정
        self.table_widget.setColumnCount(5)  # UID, 체크, 항목, 비중, 퍼센트 열을 설정합니다.

        meetings, _ = self.util.모임코드조회()
        # 헤더 레이블 설정
        self.table_widget.setHorizontalHeaderLabels(["UID", "체크", "항목", "비중", "퍼센트"])

        # 행의 개수 설정
        self.table_widget.setRowCount(len(meetings))

        for row, (uid, meeting_name, _, _, _) in enumerate(meetings.values()):
            # UID를 0번 열에 추가하지만 사용자는 보지 않도록 숨깁니다.
            uid_item = QTableWidgetItem(str(uid))
            self.table_widget.setItem(row, 0, uid_item)
            uid_item.setFlags(uid_item.flags() ^ Qt.ItemIsEditable)  # UID 열은 편집 불가로 설정
            # 체크박스 생성
            checkbox = QCheckBox()
            checkbox.stateChanged.connect(lambda state, row=row: self.toggle_spinbox(state, row))

            # 항목 레이블 생성
            item_label = QTableWidgetItem(meeting_name)

            # 스핀박스 생성 및 초기 상태를 비활성으로 설정
            spinbox = QSpinBox()
            spinbox.setEnabled(False)
            spinbox.valueChanged.connect(self.update_percentages)

            # 퍼센트 레이블 생성
            percent_label = QTableWidgetItem()

            # 테이블 셀에 위젯 추가
            self.table_widget.setCellWidget(row, 1, checkbox)  # 체크박스는 1열에 추가
            self.table_widget.setItem(row, 2, item_label)  # 항목 레이블은 2열에 추가
            self.table_widget.setCellWidget(row, 3, spinbox)  # 스핀박스는 3열에 추가
            self.table_widget.setItem(row, 4, percent_label)  # 퍼센트 레이블은 4열에 추가

        # 내용에 맞게 열 너비 조정
        self.table_widget.resizeColumnsToContents()

        # 테이블을 읽기 전용으로 설정하여 셀 편집 방지
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # UID 열 숨기기
        self.table_widget.setColumnHidden(0, True)  # UID 열 숨기기

    def add_button(self):
        # '구분 부여' 버튼을 생성하고 클릭 시 동작을 설정합니다.
        self.assign_button = QPushButton("구분 부여")
        self.assign_button.clicked.connect(self.show_data)
        self.assign_button.setEnabled(False)
        self.main_layout.addWidget(self.assign_button)

    def toggle_spinbox(self, state, row):
        # 현재 행의 스핀박스 위젯을 가져옵니다.
        spinbox = self.table_widget.cellWidget(row, 3)
        if spinbox:
            if state == Qt.Checked:
                spinbox.setEnabled(True)
                spinbox.setValue(1)
            else:
                spinbox.setEnabled(False)
                spinbox.setValue(0)  # 스핀박스 값을 0으로 설정합니다.
            self.update_percentages()  # 퍼센트 업데이트 호출
            self.update_button_state()  # 버튼 활성화 상태 업데이트

    def update_percentages(self):
        total = 0
        rows = self.table_widget.rowCount()

        # 모든 스핀박스의 값을 합산합니다.
        for row in range(rows):
            spinbox = self.table_widget.cellWidget(row, 3)
            if spinbox:
                total += spinbox.value()

        # 각 행의 퍼센트를 계산하고 업데이트합니다.
        for row in range(rows):
            spinbox = self.table_widget.cellWidget(row, 3)
            percent_label = self.table_widget.item(row, 4)
            if spinbox:
                if total > 0:
                    percent = (spinbox.value() / total) * 100
                    percent_label.setText(f"{round(percent)}%")
                else:
                    percent_label.setText("")  # 총합이 0일 때 퍼센트 열 비우기

        # '구분 부여' 버튼의 활성화 상태를 업데이트합니다.
        self.update_button_state()

    def update_button_state(self):
        all_zero = True
        rows = self.table_widget.rowCount()

        # 모든 비중 값이 0인지 확인합니다.
        for row in range(rows):
            spinbox = self.table_widget.cellWidget(row, 3)
            if spinbox and spinbox.value() != 0:
                all_zero = False
                break

        # '구분 부여' 버튼의 활성화 상태를 업데이트합니다.
        self.assign_button.setEnabled(not all_zero)

    def show_data(self):
        # 테이블의 모든 데이터를 출력합니다.
        rows = self.table_widget.rowCount()
        data = []
        할당구분 = self.util.구분코드조회(True)[1:]
        # 선택된 날짜 가져오기
        selected_date = self.start_date_combo.currentText()
        참석통계 = self.util.참석통계조회(selected_date)[1:]

        score = []
        for i in range(len(참석통계)):
            score_sum = 0
            for row in range(rows):
                percent = self.table_widget.item(row, 4).text()
                if 참석통계[i][row + 2] is not None:
                    score_sum += 참석통계[i][row + 2] * float(percent[:-1]) / float(100)
            score.append((참석통계[i][0], 참석통계[i][1], score_sum))
        sorted_score = sorted(score, key=lambda x: x[2], reverse=True)
        print(할당구분)
        print(sorted_score)

        num_sections = len(할당구분)
        section_size = len(sorted_score) // num_sections

        # 섹션을 나누고 각 섹션에 대해 할당구분의 등급을 매핑
        result = []
        for i in range(num_sections):
            start_index = i * section_size
            end_index = (i + 1) * section_size if i < num_sections - 1 else len(sorted_score)

            section_scores = sorted_score[start_index:end_index]
            grade = 할당구분[i][1]  # 각 섹션에 해당하는 할당구분의 등급
            for score in section_scores:
                result.append((score[0], score[1], grade))

        # 결과 출력
        print(result)
        self.util.구분부여(result)

        # 선택된 날짜와 데이터를 함께 출력
        message = f"선택된 날짜: {selected_date}\n\n" + "\n".join(data)
        QMessageBox.information(self, "전체 데이터", message)

    def toggle_widgets(self, layout, enabled):
        # 레이아웃의 모든 위젯을 비활성화하거나 활성화
        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()
            if widget:
                widget.setEnabled(enabled)
                # 위젯이 숨겨져 있는 경우는 visible 상태도 변경할 수 있음
                widget.setVisible(enabled)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = GradeSet()
    window.show()

    sys.exit(app.exec_())
