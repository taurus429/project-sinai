import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
import numpy as np

from src import util
gender_colors = {"남": '#ADD8E6', "여": '#FFB6C1'}
age_colors = {"91": "#d9ed92",
                      "92": "#b5e48c",
                      "93": "#99d98c",
                      "94": "#76c893",
                      "95": "#52b69a",
                      "96": "#34a0a4",
                      "97": "#168aad",
                      "98": "#1a759f",
                      "99": "#1e6091",
                      "00": "#184e77"}
grade_colors = dict()
구분데이터 = util.Util().구분코드조회()[1:]
for g in 구분데이터:
    grade_colors[g[1]] = g[2]

class StatisticsWidget(QWidget):
    def __init__(self, parent=None, 리더=None):
        super().__init__(parent)
        self.리더 = 리더
        self.layout = QVBoxLayout(self)
        self.stats_label = QLabel("통계", self)
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.stats_label)
        self.figures = []
        self.canvases = []
        self.count_label = QLabel("사랑원: 0명")
        self.sunday_label = QLabel("예배출석: 0명")
        self.sarang_label = QLabel("사랑모임: 0명")
        self.initCharts()
        self.setMinimumWidth(130)

    def initCharts(self):
        figure = Figure(figsize=(5, 5), tight_layout=True)
        canvas = FigureCanvas(figure)
        self.figures.append(figure)
        self.canvases.append(canvas)
        self.layout.addWidget(canvas)
        ax = figure.add_subplot(111)
        sizes = [1]
        labels = [self.리더[4]]
        self.plot_pie_chart(ax, sizes, labels, [gender_colors[self.리더[4]]], "성별 분포")

        figure = Figure(figsize=(5, 5), tight_layout=True)
        canvas = FigureCanvas(figure)
        self.figures.append(figure)
        self.canvases.append(canvas)
        self.layout.addWidget(canvas)
        ax = figure.add_subplot(111)
        sizes = [1]
        labels = [self.리더[2]]
        self.plot_pie_chart(ax, sizes, labels, [age_colors[self.리더[2]]], "또래 분포")

        figure = Figure(figsize=(5, 5), tight_layout=True)
        canvas = FigureCanvas(figure)
        self.figures.append(figure)
        self.canvases.append(canvas)
        self.layout.addWidget(canvas)
        ax = figure.add_subplot(111)
        sizes = [1]
        labels = [self.리더[3]]
        self.plot_pie_chart(ax, sizes, labels, [grade_colors[self.리더[3]]], "구분 분포")

        self.layout.addWidget(self.count_label)
        self.layout.addWidget(self.sunday_label)
        self.layout.addWidget(self.sarang_label)

    def plot_pie_chart(self, axes, sizes, labels, colors=None, title=None):
        axes.clear()
        pie_result = axes.pie(
            sizes,
            labels=None,
            autopct=None,
            startangle=90,
            colors=colors
        )
        if len(pie_result) == 2:
            wedges, texts = pie_result
            autotexts = []
        else:
            wedges, texts, autotexts = pie_result

        for text in texts:
            text.set_color('black')
            text.set_visible(False)
        for autotext in autotexts:
            autotext.set_visible(False)

        axes.axis('equal')
        axes.set_title(title, fontsize=8, fontweight='bold')

        # Update figure size dynamically in resizeEvent
        figure = axes.figure
        figure.tight_layout(pad=0.5)

        def update_annot(annot, wedge, size, label):
            x, y = wedge.center
            annot.xy = (x, y)
            annot.set_text(f'{label}: {size}명')

        def hover(event):
            vis = annot.get_visible()
            if event.inaxes == axes:
                for wedge, size, label in zip(wedges, sizes, labels):
                    cont, _ = wedge.contains(event)
                    if cont:
                        update_annot(annot, wedge, size, label)
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

        canvas = axes.figure.canvas
        canvas.mpl_connect("motion_notify_event", hover)

    def updateCharts(self, members):
        members.append(self.리더)
        age_counts = {}
        grade_counts = {}
        gender_counts = {}

        for record in members:
            age = record[2]
            grade = record[3]
            gender = record[4]

            if age not in age_counts:
                age_counts[age] = 0
            age_counts[age] += 1

            if grade not in grade_counts:
                grade_counts[grade] = 0
            grade_counts[grade] += 1

            if gender not in gender_counts:
                gender_counts[gender] = 0
            gender_counts[gender] += 1

        # Update pie charts with new data
        self.updatePieChart(self.figures[0].axes[0], gender_counts, "gender")
        self.updatePieChart(self.figures[1].axes[0], age_counts, "age")
        self.updatePieChart(self.figures[2].axes[0], grade_counts, "grade")
        self.count_label.setText(f"사랑원: {len(members)-1}명")

    def updatePieChart(self, ax, data, category):
        data = {k: data[k] for k in sorted(data)}
        labels = list(data.keys())
        sizes = list(data.values())
        colors = []
        title = ""
        if category == "gender":
            for label in labels:
                colors.append(gender_colors[label])
            title = "성별 분포"
        elif category == "age":
            for label in labels:
                colors.append(age_colors[label])
            title = "또래 분포"
        elif category == "grade":
            for label in labels:
                colors.append(grade_colors[label])
            title = "구분 분포"
        self.plot_pie_chart(ax, sizes, labels, colors, title = title)
        # Redraw the canvas to reflect updates
        canvas = ax.figure.canvas
        canvas.draw()
        canvas.flush_events()
