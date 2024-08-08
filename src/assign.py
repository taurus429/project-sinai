import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QTimer, QMimeData
from PyQt5.QtGui import QDrag, QPixmap
from list_manager import ListManager  # Assuming this is a custom module
from src import util
from statistics_widget import StatisticsWidget  # Import the new StatisticsWidget
import color as cUtil

구분리스트 = util.Util().구분코드조회()[1:]

class DraggableLabel(QLabel):
    def __init__(self, member_tuple, parent=None):
        super().__init__(member_tuple[2] + " " + member_tuple[1], parent)  # Use the name for display
        self.member_tuple = member_tuple
        bg_color = "#FFFFFF"
        for 구분 in 구분리스트:
            if 구분[1] == member_tuple[3]:
                bg_color = 구분[2]
                break
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(
            f"border: 1px solid black; background-color: {bg_color}; color: {cUtil.get_contrast_color(bg_color)};")
        self.setFixedHeight(25)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            # Start the drag operation
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.member_tuple[2] + " " + self.member_tuple[1])  # Use the name for drag data
            drag.setMimeData(mime_data)
            drag.setHotSpot(event.pos() - self.rect().topLeft())

            # Generate an image of the box being dragged
            pixmap = QPixmap(self.size())
            self.render(pixmap)  # Render the current widget's visual state to pixmap

            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)


class TeamWidget(QWidget):
    def __init__(self, index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index = index
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: #f0f0f0; border: 1px dashed #ccc;")
        마을원 = util.Util().마을원전체조회()[1:]
        리더 = [tup for tup in 마을원 if tup[3] == 'L'][index]
        리더튜플 = (리더[0], 리더[2], 리더[1], 리더[3], 리더[5])

        # Create a horizontal layout to hold team and statistics layouts
        self.main_layout = QVBoxLayout(self)
        self.middle_layout = QHBoxLayout(self)
        self.bottom_layout = QVBoxLayout(self)
        self.leader_label = QLabel(f"{리더[2]} 사랑", self)
        self.leader_label.setAlignment(Qt.AlignCenter)
        self.leader_label.setStyleSheet("background-color: #e6e6fa; font-size: 15px; font-weight: bold;")

        # Create a layout for team display
        self.team_layout = QVBoxLayout()
        # Create a statistics widget
        self.statistics_widget = StatisticsWidget(self, 리더튜플)
        self.middle_layout.addLayout(self.team_layout)
        self.middle_layout.addWidget(self.statistics_widget)
        self.main_layout.addWidget(self.leader_label)
        self.main_layout.addLayout(self.middle_layout)
        self.main_layout.addLayout(self.bottom_layout)

    def getIndex(self):
        return self.index

    def dropEvent(self, event):
        # Ensure that the drop event is handled properly
        member_name = event.mimeData().text()

        # Process the drop event
        self.parent().handleDrop(member_name, self.index)
        event.accept()


class TeamAllocator(QWidget):
    def __init__(self):
        super().__init__()

        self.util = util.Util()
        배치대상 = self.util.배치대상조회()[1:]

        self.members = []
        for b in 배치대상:
            self.members.append((b[0], b[2], b[1], b[3], b[5]))
        self.members = sorted(self.members, key=lambda x: x[1])
        self.teams = []

        # Open the list manager window for managing both separate and companion lists
        self.list_manager_window = ListManager(self)
        # Initialize UI
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Random Team Allocator')
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        main_layout = QVBoxLayout()
        date_layout = QHBoxLayout()
        label = QLabel("통계 기준일:")

        텀 = self.util.텀조회()[1:]
        dates = []
        for t in 텀:
            dates.append(t[2])
        # 드롭다운 박스 생성
        self.start_date_combo = QComboBox()
        # 드롭다운 목록에 예제 날짜 추가
        self.start_date_combo.addItems(dates)

        date_layout.addWidget(label)
        date_layout.addWidget(self.start_date_combo)
        date_layout.setAlignment(Qt.AlignLeft)
        main_layout.addLayout(date_layout)

        # Display area for current member
        self.current_member_label = QLabel("", self)
        self.current_member_label.setAlignment(Qt.AlignCenter)
        self.current_member_label.setStyleSheet("background-color: lightblue; font-size: 20px;")
        self.current_member_label.setFixedSize(100, 50)

        main_layout.addWidget(self.current_member_label, alignment=Qt.AlignCenter)

        마을원 = self.util.마을원전체조회()[1:]
        리더리스트 = [tup for tup in 마을원 if tup[3] == 'L']
        self.teams = [[] for _ in range(len(리더리스트))]

        # Team area layout
        self.team_layouts = []
        team_area = QHBoxLayout()
        self.current_index = 0
        사랑배치분류 = self.util.배치구분분류조회()[1:]
        사랑배치분류 = [item[0] for item in 사랑배치분류]


        for i, 리더 in enumerate(리더리스트):
            # Use TeamWidget's new main_layout for organizing team and statistics
            team_widget = TeamWidget(i, self)

            # Create checkboxes for grades A to E
            checkbox_layout = QVBoxLayout()
            for grade in 사랑배치분류:
                checkbox = QCheckBox(grade)
                checkbox_layout.addWidget(checkbox)

            # Add the checkbox layout above the team label
            team_widget.team_layout.addLayout(checkbox_layout)

            team_label = QLabel("     ", self)
            team_label.setAlignment(Qt.AlignCenter)
            team_widget.team_layout.addWidget(team_label)

            # Set up drop area
            team_widget.dragEnterEvent = self.dragEnterEvent
            team_widget.dropEvent = lambda event, index=i: self.dropEvent(event, index)

            self.team_layouts.append(team_widget)
            team_area.addWidget(team_widget)

        main_layout.addLayout(team_area)

        # Manage list button at the top
        manage_button_layout = QHBoxLayout()

        # Button to open the list manager
        manage_button = QPushButton("동반/분리 명단 관리", self)
        manage_button.setFixedWidth(150)
        manage_button.clicked.connect(self.openListManager)

        # Add the button and labels to the layout
        manage_button_layout.addWidget(manage_button)
        # Assign button
        assign_button = QPushButton("Random 배치 시작", self)
        assign_button.setFixedWidth(150)
        manage_button_layout.addWidget(assign_button)
        assign_button.clicked.connect(self.startAssignment)
        manage_button_layout.setAlignment(Qt.AlignCenter)
        main_layout.addLayout(manage_button_layout)

        # Set the layout to the window
        self.setLayout(main_layout)

        # Initialize timer for assigning members
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.assignMember)

    def openListManager(self):
        self.list_manager_window.show()

    def startAssignment(self):
        # Reset index and start timer
        self.current_index = 0
        self.timer.start(500)

    def assignMember(self):
        # Assign members randomly to teams
        if self.current_index < len(self.members):
            member = self.members[self.current_index]
            self.current_member_label.setText(member[1])  # Display the name
            self.animateAssignment(member)
            self.current_index += 1
        else:
            # Stop the timer when all members have been assigned
            self.timer.stop()
            self.current_member_label.setText("배치 완료")

    def animateAssignment(self, member):
        # Select a random team
        team_index = random.randint(0, len(self.teams) - 1)

        # Create a DraggableLabel for the member
        member_label = DraggableLabel(member, self)

        # Ensure current_member_label is above other widgets
        self.current_member_label.raise_()  # Bring current_member_label to the top

        # Set up animation
        self.current_member_label.setGeometry(350, 50, 100, 50)
        start_rect = self.current_member_label.geometry()
        team_layout = self.team_layouts[team_index].team_layout
        num_members = len(self.teams[team_index])
        team_x = self.team_layouts[team_index].geometry().x()
        team_y = self.team_layouts[team_index].geometry().y() + (member_label.height() * (num_members + 1))

        end_rect = QRect(team_x, team_y, self.current_member_label.width(), self.current_member_label.height())
        self.animation = QPropertyAnimation(self.current_member_label, b"geometry")
        self.animation.setDuration(300)
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.finished.connect(lambda: self.addMember(team_index, member_label))
        self.animation.start()

    def addMember(self, team_index, member_label):
        # Actually add the member
        self.teams[team_index].append(member_label)
        self.teams[team_index].sort(key=lambda x: (x.member_tuple[3], x.member_tuple[2], x.member_tuple[1]))
        # Update the UI for the team
        self.updateTeamLayout(team_index)

    def dragEnterEvent(self, event):
        # Allow drag events
        event.accept()

    def updateWarning(self):
        # Check if any team has both '김원호' and '박찬호'
        rule_violation = False
        for team in self.teams:
            names = [label.text() for label in team]
            if '김원호' in names and '최지훈' in names:
                rule_violation = True
                break

        # if rule_violation:
        #     self.warning_label.setText("규칙 위반")
        # else:
        #     self.warning_label.setText("")

    def handleDrop(self, member_name, index):
        # Remove the member from the existing team and add to the new team
        for team_index, team in enumerate(self.teams):
            for label in team:
                if label.text() == member_name:
                    # Remove label from the existing team
                    self.teams[team_index].remove(label)
                    self.team_layouts[team_index].team_layout.removeWidget(label)
                    self.updateTeamLayout(team_index)
                    # Add label to the new team
                    self.teams[index].append(label)

                    self.teams[index].sort(key=lambda x: (x.member_tuple[3], x.member_tuple[2], x.member_tuple[1]))

                    # Update the UI for the team
                    self.updateTeamLayout(index)

                    # Update warning after dropping
                    self.updateWarning()
                    return  # Exit after processing the drop

    def dropEvent(self, event, index):
        # Handle drop event to move members
        member_name = event.mimeData().text()
        self.handleDrop(member_name, index)

    def updateTeamLayout(self, team_index):
        team_layout = self.team_layouts[team_index].team_layout
        # Re-add members sorted by name
        members = []
        for member_label in self.teams[team_index]:
            team_layout.addWidget(member_label)
            members.append(member_label.member_tuple)
        self.team_layouts[team_index].statistics_widget.updateCharts(members)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    allocator = TeamAllocator()
    allocator.show()
    sys.exit(app.exec_())
