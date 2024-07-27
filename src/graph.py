import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QComboBox, QCheckBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import util

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
        print(res)
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

        # 직원 평가 분포 섹션 생성
        eval_layout = QVBoxLayout()

        # 직원 평가 파이 차트 생성
        self.eval_pie = MplCanvas(self, width=2, height=2, dpi=100)
        self.plot_pie_chart(
            self.eval_pie.axes,
            sizes=[20, 30, 25, 25],  # 장결자 제외 기본 데이터
            labels=['A', 'B', 'C', 'D'],
            title='구분 분포'
        )
        eval_layout.addWidget(self.eval_pie)
        main_pie_layout.addLayout(eval_layout)

        # 파이 차트를 메인 레이아웃에 추가
        layout.addLayout(main_pie_layout)

        # 데이터 범위를 선택하기 위한 드롭다운 메뉴 추가
        self.dropdown = QComboBox()
        self.dropdown.addItems(['최근 6달', '최근 12달', '최근 6주', '최근 12주'])
        self.dropdown.currentIndexChanged.connect(self.update_line_chart)
        layout.addWidget(self.dropdown)

        # 선형 차트 생성
        self.line_chart = MplCanvas(self, width=5, height=4, dpi=100)
        self.plot_line_chart(self.line_chart.axes, '최근 6달')
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

    def plot_line_chart(self, axes, period):
        """선형 차트를 그리는 함수"""
        axes.clear()
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6']

        # 기본 데이터 설정
        total_employees = [100, 105, 102, 108, 110, 115]
        avg_attendees = [80, 82, 85, 88, 87, 90]
        avg_overtime = [10, 12, 15, 14, 13, 16]

        if period == '최근 6달':
            x_labels = months
            total_employees = [100, 105, 102, 108, 110, 115]
            avg_attendees = [80, 82, 85, 88, 87, 90]
            avg_overtime = [10, 12, 15, 14, 13, 16]
        elif period == '최근 12달':
            x_labels = months * 2  # 12달에 대한 데이터 반복
            total_employees = total_employees * 2
            avg_attendees = avg_attendees * 2
            avg_overtime = avg_overtime * 2
        elif period == '최근 6주':
            x_labels = weeks
            total_employees = [90, 92, 95, 93, 98, 100]
            avg_attendees = [70, 72, 75, 78, 77, 80]
            avg_overtime = [8, 10, 12, 11, 9, 13]
        elif period == '최근 12주':
            x_labels = weeks * 2  # 12주에 대한 데이터 반복
            total_employees = total_employees[:12]  # 12주의 데이터만 사용
            avg_attendees = avg_attendees[:12]
            avg_overtime = avg_overtime[:12]

        # 선형 차트 데이터 설정
        line1, = axes.plot(x_labels, total_employees, marker='o', label='총 마을원 수')
        line2, = axes.plot(x_labels, avg_attendees, marker='o', label='평균 참석자 수')
        line3, = axes.plot(x_labels, avg_overtime, marker='o', label='평균 사랑모임 수')

        axes.set_xlabel('기간')
        axes.set_ylabel('인원 수')
        axes.set_title(f'참석 데이터 ({period})')
        axes.legend(loc='upper left')

        # 주석 기능
        def update_annot(line, ind):
            x, y = line.get_data()
            annot.xy = (x[ind["ind"][0]], y[ind["ind"][0]])
            text = f"{y[ind['ind'][0]]}"
            annot.set_text(text)
            annot.get_bbox_patch().set_alpha(0.4)

        def hover(event):
            vis = annot.get_visible()
            if event.inaxes == axes:
                for line in [line1, line2, line3]:
                    cont, ind = line.contains(event)
                    if cont:
                        update_annot(line, ind)
                        annot.set_visible(True)
                        self.line_chart.draw()
                        return
            if vis:
                annot.set_visible(False)
                self.line_chart.draw()

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
