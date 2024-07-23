import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QComboBox, QCheckBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import util
# Use a specific font to support Korean characters
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows
# plt.rcParams['font.family'] = 'NanumGothic'  # For Linux or macOS, use this if Malgun Gothic is not available

plt.style.use('ggplot')


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class GraphWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        # Create a horizontal layout to hold the pie charts
        main_pie_layout = QHBoxLayout()

        self.util = util.Util()
        res = self.util.성별분포조회()
        res = res[1:]
        size = []
        label = []
        for r in res:
            label.append(r[0])
            size.append(r[1])

        # Gender Distribution Section
        gender_layout = QVBoxLayout()
        # gender_title = QLabel("성별 분포")
        # gender_layout.addWidget(gender_title)

        # Gender Pie Chart
        self.gender_pie = MplCanvas(self, width=2, height=2, dpi=100)
        self.plot_pie_chart(self.gender_pie.axes,
                            sizes=size,  # Default sizes for 장결자 제외
                            labels=label,
                            title='장결자 제외')
        self.gender_pie.axes.set_title('장결자 제외', fontsize=10, fontweight='bold')
        gender_layout.addWidget(self.gender_pie)

        # Add Checkboxes for Gender Pie Charts
        self.gender_check_include = QCheckBox('장결자 포함')
        self.gender_check_include.setChecked(False)  # Default is unchecked
        self.gender_check_include.stateChanged.connect(self.update_gender_pie_chart)

        gender_layout.addWidget(self.gender_check_include)
        main_pie_layout.addLayout(gender_layout)

        # Age Distribution Section
        age_layout = QVBoxLayout()
        # age_title = QLabel("연령 분포")
        # age_layout.addWidget(age_title)

        res = self.util.또래분포조회()
        res = res[1:]
        size = []
        label = []
        for r in res:
            label.append(r[0])
            size.append(r[1])
        # Age Pie Chart
        self.age_pie = MplCanvas(self, width=2, height=2, dpi=100)
        self.plot_pie_chart(self.age_pie.axes,
                            sizes=size,  # Default sizes for 장결자 제외
                            labels=label,
                            title='장결자 제외')
        self.age_pie.axes.set_title('장결자 제외', fontsize=10, fontweight='bold')
        age_layout.addWidget(self.age_pie)

        # Add Checkboxes for Age Pie Charts
        self.age_check_include = QCheckBox('장결자 포함')
        self.age_check_include.setChecked(False)  # Default is unchecked
        self.age_check_include.stateChanged.connect(self.update_age_pie_chart)

        age_layout.addWidget(self.age_check_include)
        main_pie_layout.addLayout(age_layout)

        # Employee Evaluation Distribution Section
        eval_layout = QVBoxLayout()

        # Employee Evaluation Pie Chart
        self.eval_pie = MplCanvas(self, width=2, height=2, dpi=100)
        self.plot_pie_chart(self.eval_pie.axes,
                            sizes=[20, 30, 25, 25],  # Default sizes for 장결자 제외
                            labels=['A', 'B', 'C', 'D'],
                            title='장결자 제외')
        self.eval_pie.axes.set_title('장결자 제외', fontsize=10, fontweight='bold')
        eval_layout.addWidget(self.eval_pie)

        # Add Checkboxes for Employee Evaluation Pie Charts
        self.eval_check_include = QCheckBox('장결자 포함')
        self.eval_check_include.setChecked(False)  # Default is unchecked
        self.eval_check_include.stateChanged.connect(self.update_eval_pie_chart)

        eval_layout.addWidget(self.eval_check_include)
        main_pie_layout.addLayout(eval_layout)

        # Add the pie charts layout to the main layout
        layout.addLayout(main_pie_layout)

        # Add the dropdown menu for selecting the data range
        self.dropdown = QComboBox()
        self.dropdown.addItems(['최근 6달', '최근 12달', '최근 6주', '최근 12주'])
        self.dropdown.currentIndexChanged.connect(self.update_line_chart)
        layout.addWidget(self.dropdown)

        # Line Chart
        self.line_chart = MplCanvas(self, width=5, height=4, dpi=100)
        self.plot_line_chart(self.line_chart.axes, '최근 6달')
        layout.addWidget(self.line_chart)

        self.setLayout(layout)

        # Initialize pie charts
        #self.update_gender_pie_chart()
        #self.update_age_pie_chart()
        #self.update_eval_pie_chart()

    def plot_pie_chart(self, axes, sizes, labels, title):
        axes.clear()
        pie_result = axes.pie(sizes, labels=labels, autopct=None, startangle=90,
                              colors=plt.cm.Paired(np.arange(len(sizes))))
        if len(pie_result) == 2:
            wedges, texts = pie_result
            autotexts = []  # No autopct in this case
        else:
            wedges, texts, autotexts = pie_result

        for text in texts:
            text.set_color('black')
        axes.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        axes.set_title(title)

        # Implement tooltips
        def update_annot(annot, wedge, size):
            # Calculate the label's position
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

        annot = axes.annotate("", xy=(0, 0), xytext=(10, 10), textcoords="offset points",
                              bbox=dict(boxstyle="round", fc="w"),
                              arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)

        # Connect hover event to canvas
        canvas = axes.figure.canvas
        canvas.mpl_connect("motion_notify_event", hover)

    def plot_line_chart(self, axes, period):
        axes.clear()
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6']

        total_employees = [100, 105, 102, 108, 110, 115]
        avg_attendees = [80, 82, 85, 88, 87, 90]
        avg_overtime = [10, 12, 15, 14, 13, 16]
        if period == '최근 6달':
            x_labels = months
            total_employees = [100, 105, 102, 108, 110, 115]
            avg_attendees = [80, 82, 85, 88, 87, 90]
            avg_overtime = [10, 12, 15, 14, 13, 16]
        elif period == '최근 12달':
            x_labels = months * 2  # Repeat months for 12 months
            total_employees = total_employees * 2
            avg_attendees = avg_attendees * 2
            avg_overtime = avg_overtime * 2
        elif period == '최근 6주':
            x_labels = weeks
            total_employees = [90, 92, 95, 93, 98, 100]
            avg_attendees = [70, 72, 75, 78, 77, 80]
            avg_overtime = [8, 10, 12, 11, 9, 13]
        elif period == '최근 12주':
            x_labels = weeks * 2  # Repeat weeks for 12 weeks
            total_employees = total_employees[:12]  # Use the first 12 weeks of data
            avg_attendees = avg_attendees[:12]
            avg_overtime = avg_overtime[:12]

        line1, = axes.plot(x_labels, total_employees, marker='o', label='Total Employees')
        line2, = axes.plot(x_labels, avg_attendees, marker='o', label='Avg. Attendees')
        line3, = axes.plot(x_labels, avg_overtime, marker='o', label='Avg. Overtime')

        axes.set_xlabel('Time Period')
        axes.set_ylabel('Number of People')
        axes.set_title(f'Monthly Employee Data ({period})')
        axes.legend(loc='upper left')

        # Annotate function
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

        annot = axes.annotate("", xy=(0, 0), xytext=(10, 10), textcoords="offset points",
                              bbox=dict(boxstyle="round", fc="w"),
                              arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)
        self.line_chart.mpl_connect("motion_notify_event", hover)

    def update_gender_pie_chart(self):
        if self.gender_check_include.isChecked():
            sizes = [45, 55]  # Example data for 장결자 포함
            title = '장결자 포함'
        else:
            sizes = [40, 60]  # Example data for 장결자 제외
            title = '장결자 제외'
        self.plot_pie_chart(self.gender_pie.axes, sizes=sizes, labels=['남', '여'], title=title)
        self.gender_pie.draw()

    def update_age_pie_chart(self):
        if self.age_check_include.isChecked():
            sizes = [15, 25, 35, 25]  # Example data for 장결자 포함
            title = '장결자 포함'
        else:
            sizes = [10, 20, 40, 30]  # Example data for 장결자 제외
            title = '장결자 제외'
        self.plot_pie_chart(self.age_pie.axes, sizes=sizes, labels=['<18', '18-25', '26-40', '40+'], title=title)
        self.age_pie.draw()

    def update_eval_pie_chart(self):
        if self.eval_check_include.isChecked():
            sizes = [25, 30, 20, 25]  # Example data for 장결자 포함
            title = '장결자 포함'
        else:
            sizes = [20, 30, 25, 25]  # Example data for 장결자 제외
            title = '장결자 제외'
        self.plot_pie_chart(self.eval_pie.axes, sizes=sizes, labels=['A', 'B', 'C', 'D'], title=title)
        self.eval_pie.draw()

    def update_line_chart(self):
        period = self.dropdown.currentText()
        self.plot_line_chart(self.line_chart.axes, period)
        self.line_chart.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = GraphWindow()
    main.show()
    sys.exit(app.exec_())
