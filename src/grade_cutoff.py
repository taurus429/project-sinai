import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSpinBox, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt
import util

class GradeCutoff(QWidget):
    def __init__(self):
        super().__init__()
        self.util = util.Util()
        self.grades = self.util.구분코드조회(True)[1:]
        # 등급 목록
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
            # 수평 레이아웃 생성 (등급 정보)
            grade_layout = QHBoxLayout()

            # 최대 점수 라벨
            max_score_label = QLabel(f"{100 if index == 0 else self.grade_widgets[index - 1]['min_score'].value()}")
            max_score_label.setAlignment(Qt.AlignCenter)

            # 최소 점수 입력기
            min_score_spinbox = QSpinBox()
            min_score_spinbox.setRange(0, 100)
            # 현재 등급의 최소 점수 초기값 설정
            min_score_spinbox.setValue(80 if index == 0 else int(max_score_label.text()) - 100/int(len(self.grades)))
            min_score_spinbox.valueChanged.connect(self.update_min_score)

            # 마지막 등급의 최소 점수는 편집할 수 없는 라벨로 설정
            min_score_label = QLabel("0") if index == len(self.grades) - 1 else QLabel()

            # 네모 모양의 등급 표시
            grade_label = QLabel()
            grade_label.setFixedSize(20, 20)  # 네모 크기 설정
            grade_label.setFrameStyle(QFrame.Panel | QFrame.Raised)  # 테두리 스타일 설정
            grade_label.setStyleSheet("background-color: #d3d3d3;")  # 배경색 설정
            grade_label.setAlignment(Qt.AlignCenter)
            grade_label.setText(grade[1])  # 등급 이름 추가

            # 수평 레이아웃에 위젯 추가 (등급 정보)
            grade_layout.addWidget(grade_label)
            grade_layout.addWidget(max_score_label)
            grade_layout.addWidget(QLabel("~"))
            grade_layout.addWidget(min_score_spinbox if index != len(self.grades) - 1 else min_score_label)

            # 메인 레이아웃에 등급 정보 레이아웃 추가
            self.main_layout.addLayout(grade_layout)

            # 수평 레이아웃 생성 (출력 영역)
            output_layout = QHBoxLayout()

            # 등급 아래의 네모난 출력 영역
            output_label = QLabel()
            output_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)  # 테두리 스타일 설정
            output_label.setStyleSheet("background-color: #f0f0f0;")  # 배경색 설정
            output_label.setAlignment(Qt.AlignCenter)
            output_label.setText("출력")  # 기본 출력 텍스트

            # output_label이 레이아웃의 남은 공간을 차지하도록 설정
            output_layout.addWidget(output_label)
            output_layout.setStretch(0, 1)  # 가로로 꽉 차도록 설정

            # 메인 레이아웃에 출력 레이아웃 추가
            self.main_layout.addLayout(output_layout)

            # 등급 위젯 저장
            self.grade_widgets.append({
                'grade': grade[1],
                'grade_label': grade_label,
                'max_score': max_score_label,
                'min_score': min_score_spinbox,
                'min_score_label': min_score_label,
                'output_label': output_label  # 출력 영역 저장
            })

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

            # 예시: 현재 등급의 출력 영역에 텍스트 업데이트
            self.grade_widgets[index]['output_label'].setText(f"{current_min_score}%")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = GradeCutoff()
    window.show()

    sys.exit(app.exec_())
