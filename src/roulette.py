from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QTimer, QMimeData
from PyQt5.QtGui import QDrag, QPixmap
import sys
import random
from list_manager import ListManager  # Assuming this is a custom module
from src import util


class DraggableLabel(QLabel):
    def __init__(self, member_tuple, parent=None):
        super().__init__(member_tuple[1], parent)  # Use the name for display
        self.member_tuple = member_tuple
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 1px solid red; background-color: white;")
        self.setFixedSize(100, 30)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            # Start the drag operation
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.member_tuple[1])  # Use the name for drag data
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

        # Sample data with tuples (uid, name, age, phone number)
        self.members = []
        for b in 배치대상:
            self.members.append((b[0], b[2], b[1], b[3], b[5]))
        self.members = sorted(self.members, key=lambda x: x[1])
        self.teams = [[] for _ in range(6)]

        # Initialize UI
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Random Team Allocator')
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        main_layout = QVBoxLayout()

        # Manage list button at the top
        manage_button_layout = QHBoxLayout()

        # Button to open the list manager
        manage_button = QPushButton("명단 관리", self)
        manage_button.clicked.connect(self.openListManager)

        manage_button_layout.addWidget(manage_button)

        main_layout.addLayout(manage_button_layout)

        # Display area for current member
        self.current_member_label = QLabel("", self)
        self.current_member_label.setAlignment(Qt.AlignCenter)
        self.current_member_label.setStyleSheet("background-color: lightblue; font-size: 20px;")
        self.current_member_label.setFixedSize(100, 50)

        main_layout.addWidget(self.current_member_label, alignment=Qt.AlignCenter)

        # Team area layout
        self.team_layouts = []
        team_area = QHBoxLayout()
        self.current_index = 0
        for i in range(6):
            team_layout = QVBoxLayout()
            team_label = QLabel(f"Team {i + 1}", self)
            team_label.setAlignment(Qt.AlignCenter)
            team_layout.addWidget(team_label)

            # Set up drop area
            team_widget = TeamWidget(i, self)
            team_widget.setLayout(team_layout)
            team_widget.dragEnterEvent = self.dragEnterEvent
            team_widget.dropEvent = lambda event, index=i: self.dropEvent(event, index)

            self.team_layouts.append(team_widget)
            team_area.addWidget(team_widget)

        main_layout.addLayout(team_area)

        # Assign button
        self.assign_button = QPushButton("Assign Teams", self)
        self.assign_button.clicked.connect(self.startAssigningTeams)
        main_layout.addWidget(self.assign_button, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    def openListManager(self):
        # Open the list manager window for managing both separate and companion lists
        self.list_manager_window = ListManager(self, self.members)
        self.list_manager_window.show()

    def startAssigningTeams(self):
        # Disable assign button
        self.assign_button.setEnabled(False)

        # Shuffle all members randomly
        random.shuffle(self.members)

        # Use QTimer to periodically call assignNextTeam
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.assignNextTeam)
        self.timer.start(300)  # Call every 300ms

    def assignNextTeam(self):
        # Assign the next team member if there are any left
        if self.current_index < len(self.members):
            member = self.members[self.current_index]
            self.current_member_label.setText(member[1])  # Display the name
            self.animateAssignment(member)
            self.current_index += 1
        else:
            # Stop the timer when all members have been assigned
            self.timer.stop()
            self.current_member_label.setText("Done!")

    def animateAssignment(self, member):
        # Select a random team
        team_index = random.randint(0, 5)

        # Add the name to the team area
        member_label = DraggableLabel(member, self)

        # Set up animation
        start_rect = self.current_member_label.geometry()
        team_layout = self.team_layouts[team_index].layout()
        num_members = len(self.teams[team_index])
        team_x = self.team_layouts[team_index].geometry().x()
        team_y = self.team_layouts[team_index].geometry().y() + (member_label.height() * (num_members + 1))

        # Actually add the member
        self.teams[team_index].append(member_label)
        team_layout.addWidget(member_label)

        end_rect = QRect(team_x, team_y, self.current_member_label.width(), self.current_member_label.height())
        self.animation = QPropertyAnimation(self.current_member_label, b"geometry")
        self.animation.setDuration(200)
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.finished.connect(self.resetCurrentMemberLabel)
        self.animation.start()

    def resetCurrentMemberLabel(self):
        # Return the current member label to the top center after animation ends
        self.current_member_label.setGeometry(350, 50, 100, 50)

    def dragEnterEvent(self, event):
        # Allow drag events
        event.accept()

    def dropEvent(self, event, index):
        # Get the dropped data
        member_name = event.mimeData().text()

        # Remove the member from the existing team and add to the new team
        for team_index, team in enumerate(self.teams):
            for label in team:
                if label.text() == member_name:
                    # Remove label from the existing team
                    self.teams[team_index].remove(label)
                    self.team_layouts[team_index].layout().removeWidget(label)

                    # Add label to the new team
                    self.teams[index].append(label)
                    self.team_layouts[index].layout().addWidget(label)

                    return  # Exit after processing the drop


if __name__ == '__main__':
    app = QApplication(sys.argv)
    allocator = TeamAllocator()
    allocator.show()
    sys.exit(app.exec_())
