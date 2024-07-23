# student_details_window.py
import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSplitter, QApplication
from PyQt5.QtCore import Qt
import namecard
from src import util, 날짜유틸
from statistics_table_widget import StatisticsTableWidget  # 통계 테이블 위젯 가져오기
from week_info_widget import WeekInfoWidget  # 주간 정보 위젯 가져오기


class StudentDetailsWindow(QWidget):
    def __init__(self, 마을원정보, weeks, util):
        try:
            super().__init__()
            self.setWindowTitle("마을원 세부 정보")
            self.setGeometry(150, 150, 800, 400)  # 창의 기본 크기를 설정합니다.

            main_layout = QVBoxLayout()
            main_layout.setContentsMargins(0, 0, 0, 0)  # 여백을 제거합니다.
            main_layout.setSpacing(0)  # 위젯 간의 간격을 제거합니다.

            # 명함 위젯 추가
            main_layout.addWidget(namecard.BusinessCardWidget(
                마을원정보["이름"],
                util.사랑장조회(마을원정보["uid"]),
                마을원정보["전화번호"],
                str(마을원정보["생년월일"])
            ))

            # QSplitter 사용하여 가로 레이아웃을 나누기
            splitter = QSplitter(Qt.Horizontal)  # 수평 방향으로 레이아웃을 나눕니다.

            # 통계 테이블을 왼쪽에 추가
            stats_table = StatisticsTableWidget()  # 통계 테이블 위젯 사용
            splitter.addWidget(stats_table)

            # 주간 정보를 표시하는 스크롤 영역을 오른쪽에 추가
            week_info_widget = WeekInfoWidget(weeks)  # 주간 정보 위젯 사용
            splitter.addWidget(week_info_widget)

            # 스플리터를 메인 레이아웃에 추가
            main_layout.addWidget(splitter)

            # 초기 크기 비율 설정 (1:2 비율로 통계 테이블과 스크롤 영역 크기 설정)
            splitter.setSizes([200, 600])

            self.setLayout(main_layout)
        except Exception as e:
            print(f"Error: {e}")
            return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    util = util.Util()
    res = util.참석조회(4)  # 학생 ID 4의 참석 정보를 조회합니다.
    weeks = dict()
    for r in res[1:]:
        week = 날짜유틸.get_week_of_month(r[2])
        if not weeks.__contains__(week):
            weeks[week] = []
        if r[0] == 1:
            date = 날짜유틸.convert_date_format(r[2].split()[0])
            weeks[week].append((r[1], date))
    마을원정보 = util.마을원정보조회(4)
    details_window = StudentDetailsWindow(마을원정보, weeks, util)
    details_window.show()

    sys.exit(app.exec_())

