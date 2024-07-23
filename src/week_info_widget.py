# week_info_widget.py
from PyQt5.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QSpacerItem, QSizePolicy
from roundedRectLabel import RoundedRectLabel


class WeekInfoWidget(QScrollArea):
    def __init__(self, weeks, parent=None):
        super().__init__(parent)

        # 스크롤 영역 초기 설정
        self.setWidgetResizable(True)  # 위젯 크기를 조절 가능하게 설정
        self.setStyleSheet("background-color: #FFFFFF;")  # 스크롤 영역 배경 색상

        scroll_widget = QWidget()
        scroll_widget.setStyleSheet("background-color: #FFFFFF;")
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(0, 0, 0, 0)  # 여백을 제거합니다.
        scroll_layout.setSpacing(0)  # 위젯 간의 간격을 제거합니다.

        # 주별 정보 표시
        for week_info in weeks.keys():
            meetings = weeks[week_info]
            group_box = QGroupBox(f"{week_info}")
            group_box.setFixedHeight(50)  # 각 주간 정보 그룹 박스의 높이

            # 회의 수에 따라 그룹 박스 색상 설정
            if len(meetings) > 0:
                group_box.setStyleSheet("background-color: #D4E4FE;")  # 회의가 있는 경우 파란색
            else:
                group_box.setStyleSheet("background-color: #FFEEEE;")  # 회의가 없는 경우 빨간색

            group_layout = QVBoxLayout()
            # 회의 정보를 가로로 나열하기 위한 레이아웃
            h_layout = QHBoxLayout()
            for meeting in meetings:
                label = RoundedRectLabel(f"{meeting[0]} ({meeting[1]})")
                label.setFixedSize(label.sizeHint())
                h_layout.addWidget(label)

            # 빈 공간을 위한 스페이서
            spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
            h_layout.addItem(spacer)

            group_layout.addLayout(h_layout)
            group_box.setLayout(group_layout)
            scroll_layout.addWidget(group_box)

        scroll_widget.setLayout(scroll_layout)
        self.setWidget(scroll_widget)

