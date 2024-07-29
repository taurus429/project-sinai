from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QTimer, QPoint, QMimeData
from PyQt5.QtGui import QDrag, QPixmap, QPainter
import sys, random, util

class DraggableLabel(QLabel):
    def __init__(self, member, parent=None):
        super().__init__(member, parent)
        self.member = member
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 1px solid red; background-color: white;")
        self.setFixedSize(100, 30)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            # 드래그 시작
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.member)
            drag.setMimeData(mime_data)
            drag.setHotSpot(event.pos() - self.rect().topLeft())

            # 드래그 중인 박스의 이미지 생성
            pixmap = QPixmap(self.size())
            self.render(pixmap)  # 현재 위젯의 시각적 상태를 pixmap에 렌더링

            drag.setPixmap(pixmap)
            drag.setPixmap(pixmap)  # 드래그 중인 이미지 설정

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

        # Get the drop position relative to this widget
        drop_pos = self.mapFromGlobal(event.globalPos())

        # Process the drop event
        self.parent().handleDrop(member_name, self.index)
        event.accept()


class TeamAllocator(QWidget):
    def __init__(self):
        super().__init__()

        self.util = util.Util()
        마을원 = self.util.마을원전체조회()[1:]
        print(마을원)

        # 팀원 이름 리스트 생성
        self.members = 마을원

        # 팀 공간을 나타내는 리스트
        self.teams = [[] for _ in range(6)]

        # 현재 배치 중인 팀원 인덱스
        self.current_index = 0

        # UI 초기화
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Random Team Allocator')
        self.setGeometry(100, 100, 800, 600)

        # 메인 레이아웃 설정
        main_layout = QVBoxLayout()

        # 상단에 팀원 표시 영역
        self.current_member_label = QLabel("", self)
        self.current_member_label.setAlignment(Qt.AlignCenter)
        self.current_member_label.setStyleSheet("background-color: lightblue; font-size: 20px;")
        self.current_member_label.setFixedSize(100, 50)

        main_layout.addWidget(self.current_member_label, alignment=Qt.AlignCenter)

        # 팀 공간 레이아웃
        self.team_layouts = []
        team_area = QHBoxLayout()

        for i in range(6):
            team_layout = QVBoxLayout()
            team_label = QLabel(f"Team {i + 1}", self)
            team_label.setAlignment(Qt.AlignCenter)
            team_layout.addWidget(team_label)

            # 드롭 영역 설정
            team_widget = TeamWidget(i, self)
            team_widget.setLayout(team_layout)
            team_widget.dragEnterEvent = self.dragEnterEvent
            team_widget.dropEvent = lambda event, index=i: self.dropEvent(event, index)

            self.team_layouts.append(team_widget)
            team_area.addWidget(team_widget)

        main_layout.addLayout(team_area)

        # 할당 버튼
        self.assign_button = QPushButton("Assign Teams", self)
        self.assign_button.clicked.connect(self.startAssigningTeams)
        main_layout.addWidget(self.assign_button, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    def startAssigningTeams(self):
        # 할당 버튼 비활성화
        self.assign_button.setEnabled(False)

        # 모든 팀원을 무작위로 섞음
        random.shuffle(self.members)

        # QTimer를 사용하여 주기적으로 assignNextTeam을 호출
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.assignNextTeam)
        self.timer.start(300)  # 1초마다 호출

    def assignNextTeam(self):
        # 팀원이 남아있으면 다음 팀원 할당
        if self.current_index < len(self.members):
            member = self.members[self.current_index][2]
            self.current_member_label.setText(member)
            self.animateAssignment(member)
            self.current_index += 1
        else:
            # 모든 팀원을 할당했으면 타이머 정지
            self.timer.stop()
            self.current_member_label.setText("Done!")

    def animateAssignment(self, member):
        # 팀을 무작위로 선택
        team_index = random.randint(0, 5)

        # 팀 공간에 이름 추가
        member_label = DraggableLabel(member, self)

        # 애니메이션 설정
        start_rect = self.current_member_label.geometry()
        team_layout = self.team_layouts[team_index].layout()
        num_members = len(self.teams[team_index])
        team_x = self.team_layouts[team_index].geometry().x()
        team_y = self.team_layouts[team_index].geometry().y() + (member_label.height() * (num_members + 1))

        # 실제 팀원 추가
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
        # 애니메이션 종료 후 현재 팀원 라벨을 상단 중앙으로 되돌림
        self.current_member_label.setGeometry(350, 50, 100, 50)

    def dragEnterEvent(self, event):
        # 드래그 이벤트 허용
        event.accept()

    def dropEvent(self, event, index):
        # 드롭된 데이터 가져오기
        member_name = event.mimeData().text()

        # 기존 팀에서 팀원을 제거하고 새 팀에 추가
        for team_index, team in enumerate(self.teams):
            for label in team:
                if label.text() == member_name:
                    # 기존 팀에서 라벨 제거
                    self.teams[team_index].remove(label)
                    self.team_layouts[team_index].layout().removeWidget(label)

                    # 새 팀에 라벨 추가
                    self.teams[index].append(label)
                    self.team_layouts[index].layout().addWidget(label)

                    return  # 드롭 처리 후 종료


if __name__ == '__main__':
    app = QApplication(sys.argv)
    allocator = TeamAllocator()
    allocator.show()
    sys.exit(app.exec_())
