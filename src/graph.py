import sys
from collections import defaultdict

from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QComboBox, QCheckBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import util
from datetime import datetime
# 한글 문자를 지원하기 위해 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows
# plt.rcParams['font.family'] = 'NanumGothic'  # Linux 또는 macOS에서는 이 줄의 주석을 해제하고 사용하세요.

plt.style.use('ggplot')  # 그래프 스타일 설정


class MplCanvas(FigureCanvas):
    """Matplotlib 캔버스를 위한 클래스"""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)  # 그래프 서브플롯 생성
        super(MplCanvas, self).__init__(fig)


class GraphWindow(QWidget):
    """그래프 창을 구성하는 클래스"""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()  # 메인 레이아웃 생성

        # 파이 차트를 위한 가로 레이아웃 생성
        main_pie_layout = QHBoxLayout()

        self.util = util.Util()

        # 성별 분포 데이터 가져오기
        res = self.util.성별분포조회(False, False)
        res = res[1:]
        size = []
        label = []
        for r in res:
            label.append(r[0])
            size.append(r[1])

        # 성별 분포 섹션 생성
        gender_layout = QVBoxLayout()

        # 성별 파이 차트 생성
        self.gender_pie = MplCanvas(self, width=2, height=2, dpi=100)
        self.plot_pie_chart(
            self.gender_pie.axes,
            sizes=size,  # 장결자 제외 기본 데이터
            labels=label,
            title='성별 분포',
            colors= ['#ADD8E6', '#FFB6C1']
        )
        gender_layout.addWidget(self.gender_pie)

        main_pie_layout.addLayout(gender_layout)

        # 연령 분포 섹션 생성
        age_layout = QVBoxLayout()

        # 연령 분포 데이터 가져오기
        res = self.util.또래분포조회(False, False)
        res = res[1:]
        size = []
        label = []
        for r in res:
            label.append(r[0])
            size.append(r[1])

        # 연령 파이 차트 생성
        self.age_pie = MplCanvas(self, width=2, height=2, dpi=100)
        self.plot_pie_chart(
            self.age_pie.axes,
            sizes=size,  # 장결자 제외 기본 데이터
            labels=label,
            title='또래 분포'
        )
        age_layout.addWidget(self.age_pie)

        main_pie_layout.addLayout(age_layout)

        # 구분 분포 섹션 생성
        eval_layout = QVBoxLayout()

        # 구분 파이 차트 생성
        res = self.util.구분분포조회(False, False)
        res = res[1:]
        size = []
        label = []
        color = []
        구분데이터 = self.util.구분코드조회()[1:]
        구분색 = dict()
        for g in 구분데이터:
            구분색[g[1]] = g[2]
        구분색[None] = '#F0F0F0'
        구분색[''] = '#F0F0F0'
        for r in res:
            label.append(r[0])
            size.append(r[1])
            color.append(구분색[r[0]])
        self.eval_pie = MplCanvas(self, width=2, height=2, dpi=100)
        self.plot_pie_chart(
            self.eval_pie.axes,
            sizes=size,  # 장결자 제외 기본 데이터
            labels=label,
            title='구분 분포',
            colors=color
        )
        eval_layout.addWidget(self.eval_pie)
        main_pie_layout.addLayout(eval_layout)

        # 파이 차트를 메인 레이아웃에 추가
        layout.addLayout(main_pie_layout)

        tup = (4,14)
        모임참석통계 = self.util.모임참석통계(tup)[1:]

        # 쿼리 결과를 처리하여 딕셔너리로 변환
        meetings_data = defaultdict(lambda: defaultdict(int))
        dates_set = set()

        for meeting_date, meeting_name, attendees in 모임참석통계:
            # 날짜를 문자열 형식으로 변환하여 x축 레이블로 사용
            meeting_date_obj = datetime.strptime(meeting_date, '%Y-%m-%d %H:%M:%S')
            meeting_date_str = meeting_date_obj.strftime('%Y-%m-%d')
            meetings_data[meeting_name][meeting_date_str] = attendees
            dates_set.add(meeting_date_str)

        # 날짜를 정렬된 리스트로 변환
        sorted_dates = sorted(dates_set)

        print(sorted_dates)
        # 데이터 범위를 선택하기 위한 드롭다운 메뉴 추가
        self.dropdown = QComboBox()
        self.dropdown.addItems(['최근 6달', '최근 12달', '최근 6주', '최근 12주'])
        self.dropdown.currentIndexChanged.connect(self.update_line_chart)
        layout.addWidget(self.dropdown)

        # 선형 차트 생성
        self.line_chart = MplCanvas(self, width=5, height=4, dpi=100)
        self.plot_line_chart(self.line_chart.axes, '최근 6주', meetings_data, sorted_dates)
        layout.addWidget(self.line_chart)

        self.setLayout(layout)

    def plot_pie_chart(self, axes, sizes, labels, title, colors = None):
        """파이 차트를 그리는 함수"""
        axes.clear()
        color = plt.cm.Paired(np.arange(len(sizes)))
        if colors:
            color = colors

        pie_result = axes.pie(
            sizes,
            labels=labels,
            autopct=None,
            startangle=90,
            colors=color
        )
        if len(pie_result) == 2:
            wedges, texts = pie_result
            autotexts = []  # 자동 퍼센트 텍스트 없음
        else:
            wedges, texts, autotexts = pie_result

        for text in texts:
            text.set_color('black')
        axes.axis('equal')  # 원형 비율을 유지하여 파이를 원 모양으로 그림
        axes.set_title(title, fontsize=10, fontweight='bold')

        # 툴팁 기능 구현
        def update_annot(annot, wedge, size):
            # 레이블 위치 계산
            x, y = wedge.center
            annot.xy = (x, y)
            annot.set_text(f'{size}명')

        def hover(event):
            vis = annot.get_visible()
            if event.inaxes == axes:
                for wedge, size in zip(wedges, sizes):
                    cont, _ = wedge.contains(event)
                    if cont:
                        update_annot(annot, wedge, size)
                        annot.set_visible(True)
                        canvas.draw()
                        return
            if vis:
                annot.set_visible(False)
                canvas.draw()

        annot = axes.annotate(
            "",
            xy=(0, 0),
            xytext=(10, 10),
            textcoords="offset points",
            bbox=dict(boxstyle="round", fc="w"),
            arrowprops=dict(arrowstyle="->")
        )
        annot.set_visible(False)

        # 캔버스에 hover 이벤트 연결
        canvas = axes.figure.canvas
        canvas.mpl_connect("motion_notify_event", hover)

    import matplotlib.pyplot as plt

    def plot_line_chart(self, axes, period, meetings_data, sorted_dates):
        """선형 차트를 그리는 함수"""
        axes.clear()

        # 모든 모임의 실제 날짜를 수집
        all_actual_dates = set()
        for attendance_data in meetings_data.values():
            all_actual_dates.update(attendance_data.keys())

        # 모든 모임 날짜를 정렬하여 x축 레이블로 사용
        sorted_dates = sorted(all_actual_dates)

        # 색상 맵 설정 (다양한 모임에 대해 색상을 다르게 지정)
        colors = plt.cm.get_cmap('tab10')

        # 각 모임의 참석자 수를 차트로 표현
        for idx, (meeting_name, attendance_data) in enumerate(meetings_data.items()):
            # 실제 데이터가 있는 날짜만 추출
            actual_dates = [date for date in sorted_dates if date in attendance_data]
            y_values = [attendance_data[date] for date in actual_dates]

            # 연속된 데이터로 구성된 세그먼트를 별도로 처리
            segments = []
            current_segment = []

            for i, date in enumerate(actual_dates):
                # 첫 번째 데이터를 현재 세그먼트에 추가
                if not current_segment:
                    current_segment.append((date, y_values[i]))
                    continue

                # 현재 날짜가 이전 날짜의 다음 날짜가 아닐 경우, 새로운 세그먼트를 시작
                if i > 0 and (sorted_dates.index(date) - sorted_dates.index(actual_dates[i - 1])) > 1:
                    segments.append(current_segment)
                    current_segment = []

                # 현재 데이터를 현재 세그먼트에 추가
                current_segment.append((date, y_values[i]))

            # 마지막 세그먼트를 추가
            if current_segment:
                segments.append(current_segment)

            # 각 세그먼트를 개별적으로 플롯
            for segment in segments:
                segment_dates, segment_y_values = zip(*segment)
                axes.plot(segment_dates, segment_y_values, marker='o',
                          label=meeting_name if segment is segments[0] else "", color=colors(idx))

        # x축 레이블, y축 레이블, 제목 설정
        axes.set_xlabel('날짜')
        axes.set_ylabel('참석자 수')
        axes.set_title(f'참석 데이터 ({period})')
        axes.legend(loc='upper left', title='모임 이름')

        # x축 레이블 회전 (날짜를 읽기 쉽게 하기 위함)
        plt.setp(axes.get_xticklabels(), rotation=45, ha="right")

        # x축의 범위를 데이터가 있는 범위로 설정
        axes.set_xlim(min(sorted_dates), max(sorted_dates))

        # y축의 범위를 자동으로 설정
        axes.set_ylim(bottom=0)

        # 주석 및 마우스 오버 기능 설정
        def update_annot(line, ind):
            x, y = line.get_data()
            annot.xy = (x[ind["ind"][0]], y[ind["ind"][0]])
            text = f"{line.get_label()}: {y[ind['ind'][0]]}"  # 모임 이름과 참석자 수를 주석으로 표시
            annot.set_text(text)
            annot.get_bbox_patch().set_alpha(0.4)

        def hover(event):
            vis = annot.get_visible()
            if event.inaxes == axes:
                for line in axes.get_lines():
                    cont, ind = line.contains(event)
                    if cont:
                        update_annot(line, ind)
                        annot.set_visible(True)
                        self.line_chart.draw()
                        return
            if vis:
                annot.set_visible(False)
                self.line_chart.draw()

        # 주석 객체 초기화 및 이벤트 연결
        annot = axes.annotate(
            "",
            xy=(0, 0),
            xytext=(10, 10),
            textcoords="offset points",
            bbox=dict(boxstyle="round", fc="w"),
            arrowprops=dict(arrowstyle="->")
        )
        annot.set_visible(False)
        self.line_chart.mpl_connect("motion_notify_event", hover)

    def update_pies(self, 장결포함, 졸업포함):
        self.update_gender_pie_chart(not 장결포함, not 졸업포함)
        self.update_age_pie_chart(not 장결포함, not 졸업포함)

    def update_gender_pie_chart(self, 장결포함, 졸업포함):
        res = self.util.성별분포조회(장결포함, 졸업포함)
        res = res[1:]
        size = []
        label = []
        for r in res:
            label.append(r[0])
            size.append(r[1])

        self.plot_pie_chart(
            self.gender_pie.axes,
            sizes=size,  # 장결자 제외 기본 데이터
            labels=label,
            title='성별 분포',
            colors=['#ADD8E6', '#FFB6C1']
        )
        self.gender_pie.draw()

    def update_age_pie_chart(self, 장결포함, 졸업포함):
        res = self.util.또래분포조회(장결포함, 졸업포함)
        res = res[1:]
        size = []
        label = []
        for r in res:
            label.append(r[0])
            size.append(r[1])
        self.plot_pie_chart(
            self.age_pie.axes,
            sizes=size,  # 장결자 제외 기본 데이터
            labels=label,
            title='또래 분포',
        )
        self.age_pie.draw()

    def update_eval_pie_chart(self):
        """직원 평가 파이 차트 업데이트 함수"""
        if self.eval_check_include.isChecked():
            sizes = [25, 30, 20, 25]  # 장결자 포함 예시 데이터
            title = '장결자 포함'
        else:
            sizes = [20, 30, 25, 25]  # 장결자 제외 예시 데이터
            title = '장결자 제외'
        self.plot_pie_chart(self.eval_pie.axes, sizes=sizes, labels=['A', 'B', 'C', 'D'], title=title)
        self.eval_pie.draw()

    def update_line_chart(self):
        """선형 차트 업데이트 함수"""
        period = self.dropdown.currentText()
        self.plot_line_chart(self.line_chart.axes, period)
        self.line_chart.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = GraphWindow()
    main.show()
    sys.exit(app.exec_())
