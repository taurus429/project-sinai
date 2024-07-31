import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSpinBox, QHBoxLayout
from PyQt5.QtCore import Qt


class GradeCutoff(QWidget):
    def __init__(self):
        super().__init__()

        # 등급 목록
        self.grades = ['A', 'B', 'C', 'D', 'F']
        self.grade_widgets = []  # 등급과 관련된 위젯을 저장할 리스트

        # 메인 레이아웃
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # 등급 커트라인 레이아웃을 생성하고 추가합니다.
        self.create_grade_cutoff_layout()

        self.setWindowTitle("Grade Cutoffs")
        self.setGeometry(100, 100, 500, 300)

    def create_grade_cutoff_layout(self):
        for index, grade in enumerate(self.grades):
            # 수평 레이아웃 생성
            grade_layout = QHBoxLayout()

            # 최대 점수 라벨
            max_score_label = QLabel(f"{100 if index == 0 else self.grade_widgets[index - 1]['min_score'].value()}")
            max_score_label.setAlignment(Qt.AlignCenter)

            # 최소 점수 입력기
            min_score_spinbox = QSpinBox()
            min_score_spinbox.setRange(0, 100)
            # 현재 등급의 최소 점수 초기값 설정
            min_score_spinbox.setValue(100 if index == 0 else int(max_score_label.text()) - 100/int(len(self.grades)))
            min_score_spinbox.valueChanged.connect(self.update_min_score)

            # 마지막 등급의 최소 점수는 편집할 수 없는 라벨로 설정
            min_score_label = QLabel("0") if index == len(self.grades) - 1 else QLabel()

            # 수평 레이아웃에 위젯 추가
            grade_layout.addWidget(QLabel(f"{grade} 등급:"))
            grade_layout.addWidget(max_score_label)
            grade_layout.addWidget(QLabel("~"))
            grade_layout.addWidget(min_score_spinbox if index != len(self.grades) - 1 else min_score_label)

            # 등급 위젯 저장
            self.grade_widgets.append({
                'grade': grade,
                'max_score': max_score_label,
                'min_score': min_score_spinbox,
                'min_score_label': min_score_label
            })

            # 메인 레이아웃에 수평 레이아웃 추가
            self.main_layout.addLayout(grade_layout)

    def update_min_score(self):
        for index in range(len(self.grade_widgets) - 1):
            current_min_score = self.grade_widgets[index]['min_score'].value()
            next_max_score_label = self.grade_widgets[index + 1]['max_score']
            next_min_score_spinbox = self.grade_widgets[index + 1]['min_score']
            next_min_score_label = self.grade_widgets[index + 1]['min_score_label']

            # 다음 등급의 최대 점수를 현재 등급의 최소 점수로 설정
            next_max_score_label.setText(f"{current_min_score}")
            next_min_score_spinbox.setRange(0, current_min_score)
            next_min_score_spinbox.setValue(min(next_min_score_spinbox.value(), current_min_score))
            next_min_score_label.setText(f"{next_min_score_spinbox.value()}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = GradeCutoff()
    window.show()

    sys.exit(app.exec_())
