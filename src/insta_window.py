import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QMainWindow, QFileDialog, QMessageBox,
    QRadioButton, QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox, QDialog, QCalendarWidget, QGroupBox, QGridLayout,
    QAction
)
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from src import util
from src import setting as s
from datetime import datetime

class CalendarPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a QCalendarWidget instance
        self.calendar = QCalendarWidget()

        # Set the grid lines to be visible
        self.calendar.setGridVisible(True)

        # Set the current date as the selected date
        self.calendar.setSelectedDate(QDate.currentDate())

        # Hide the vertical header (week numbers)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)

        # Connect the calendar's clicked signal to the date selection handler
        self.calendar.clicked.connect(self.on_date_selected)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.calendar)
        self.setLayout(layout)

        # Set the window title and modality
        self.setWindowTitle('날짜 선택')
        self.setModal(True)

    def on_date_selected(self, date):
        # Store the selected date and close the dialog
        self.selected_date = date
        self.accept()


class TextGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setting = s.Setting()
        self.settings = self.setting.get_settings()
        self.util = util.Util()

        if 'darkmode' in self.settings.keys():
            self.dark_mode = self.settings["darkmode"]
        else:
            self.dark_mode = False

        if 'birthday_file' in self.settings.keys():
            self.birthday_file = util.count_birthday_db()
        else:
            self.birthday_file = '파일없음'

        self.initUI()
        self.news_list = []
        self.schedule_list = []


    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 날짜 입력 위젯
        self.date_label = QLabel('날짜 입력:')
        self.date_edit = QLineEdit()
        self.date_edit.setText(QDate.currentDate().toString('yyyy-MM-dd'))
        self.date_button = QPushButton('날짜 선택')
        self.date_button.clicked.connect(self.show_calendar_popup)

        date_layout = QHBoxLayout()
        date_layout.addWidget(self.date_edit)
        date_layout.addWidget(self.date_button)

        # 글 유형 입력용 드롭다운 위젯
        self.type_label = QLabel('게시글 유형 선택:')
        self.type_combo = QComboBox()
        self.type_combo.addItems(['마하나임 예배', '더원 예배', '설렘 축제', '마을 리트릿', '마을 아웃팅', '블로그'])
        # self.type_combo.currentIndexChanged.connect(self.on_type_changed)

        # 설교 제목 입력 용 텍스트 위젯
        self.title_label = QLabel('설교 제목 입력:')
        self.title_edit = QLineEdit()

        # 설교 본문 입력 용 텍스트 위젯
        self.scripture_label = QLabel('설교 본문 입력:')
        self.scripture_edit = QLineEdit()

        # 글 내용 입력 용 텍스트 위젯
        self.content_label = QLabel('글 내용 입력:')
        self.content_edit = QTextEdit()

        # 글 생성용 버튼
        self.generate_button = QPushButton('생성')
        self.generate_button.clicked.connect(self.generate_text)
        self.generate_button.setStyleSheet("""
                            QPushButton {
                                background-color: #1E90FF;
                                color: white;
                            }
                            QPushButton:hover {
                                background-color: #63B8FF;
                            }
                        """)

        # 결과 생성용 텍스트 영역 위젯
        self.result_label = QLabel('게시물 미리보기:')
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)

        # 이번 주 소식
        self.this_week_news = QLabel('이번 주 소식')
        self.news_add_button = QPushButton('소식 추가')
        self.news_add_button.clicked.connect(self.add_news_input)
        self.news_dynamic_layout = QVBoxLayout()

        # 이번 주 일정
        self.this_week_schedule = QLabel('이번 주 일정')
        self.schedule_add_button = QPushButton('일정 추가')
        self.schedule_add_button.clicked.connect(self.add_schedule_input)
        self.schedule_dynamic_layout = QVBoxLayout()

        # 생일자

        self.birthday_label = QLabel('생일자 파일')
        self.birthday_layout = QWidget()
        file_layout = QHBoxLayout()

        # 파일 첨부용 버튼
        attach_file_button = QPushButton('파일 첨부')
        attach_file_button.clicked.connect(self.attach_file)
        self.attach_file_text = QLabel('파일없음')
        file_layout.addWidget(self.attach_file_text)
        file_layout.addWidget(attach_file_button)

        self.birthday_layout.setLayout(file_layout)

        # 파일 첨부용 버튼

        self.birthday_label2 = QLabel('마을원 등록')
        self.birthday_layout2 = QWidget()
        file_layout2 = QHBoxLayout()

        attach_file_button2 = QPushButton('파일 첨부')
        attach_file_button2.clicked.connect(self.attach_file2)
        self.attach_file_text2 = QLabel('파일없음')
        file_layout2.addWidget(self.attach_file_text2)
        file_layout2.addWidget(attach_file_button2)

        self.birthday_layout2.setLayout(file_layout2)

        # 이번 주 기도인도
        self.pray_label = QLabel('이번 주 기도 인도')
        self.pray_combo = QComboBox()
        self.pray_combo.addItems(['예진 사랑', '희원 사랑', '예지 사랑', '소윤 사랑', '현도 사랑', '찬호 사랑', '없음'])

        # 글 작성자 선택용 라디오 버튼 위젯
        self.author_label = QLabel('글 작성자 선택:')
        self.author_group = QGroupBox()
        self.author_radio1 = QRadioButton('작성자 A')
        self.author_radio2 = QRadioButton('작성자 B')
        self.author_radio1.setChecked(True)  # 기본 선택
        author_layout = QHBoxLayout()
        author_layout.addWidget(self.author_radio1)
        author_layout.addWidget(self.author_radio2)
        self.author_group.setLayout(author_layout)

        # 예배 뒤 아웃팅
        self.outing_label = QLabel('마지막 주 아웃팅')
        self.outing_group = QGroupBox()
        self.outing_radio1 = QRadioButton('있음')
        self.outing_radio2 = QRadioButton('없음')
        self.outing_radio2.setChecked(True)  # 기본 선택
        outing_layout = QHBoxLayout()
        outing_layout.addWidget(self.outing_radio1)
        outing_layout.addWidget(self.outing_radio2)
        self.outing_group.setLayout(outing_layout)

        # 큐티 모임
        self.qt_label = QLabel('주중 큐티 모임')
        self.qt_group = QGroupBox()
        self.qt_check1 = QCheckBox('월')
        self.qt_check2 = QCheckBox('화')
        self.qt_check3 = QCheckBox('수')
        self.qt_check4 = QCheckBox('목')
        self.qt_check5 = QCheckBox('금')
        self.qt_check1.setChecked(True)  # 기본 선택
        self.qt_check4.setChecked(True)  # 기본 선택
        qt_layout = QHBoxLayout()
        qt_layout.addWidget(self.qt_check1)
        qt_layout.addWidget(self.qt_check2)
        qt_layout.addWidget(self.qt_check3)
        qt_layout.addWidget(self.qt_check4)
        qt_layout.addWidget(self.qt_check5)
        self.qt_group.setLayout(qt_layout)

        # 주와나
        self.joowana_label = QLabel('주와나')
        self.joowana_group = QGroupBox()
        self.joowana_radio1 = QRadioButton('수요일 벧엘데이')
        self.joowana_radio2 = QRadioButton('주와나 특새')
        self.joowana_radio1.setChecked(True)  # 기본 선택
        joowana_layout = QHBoxLayout()
        joowana_layout.addWidget(self.joowana_radio1)
        joowana_layout.addWidget(self.joowana_radio2)
        self.joowana_group.setLayout(joowana_layout)

        # 결과 복사 버튼
        self.copy_button = QPushButton('결과 복사')
        self.copy_button.clicked.connect(self.copy_result_to_clipboard)
        self.copy_button.setStyleSheet("""
                            QPushButton {
                                background-color: #36a866;
                                color: white;
                            }
                            QPushButton:hover {
                                background-color: #70c493;
                            }
                        """)

        # 그리드 레이아웃 설정
        layout = QGridLayout()
        layout.addWidget(self.date_label, 0, 0)
        layout.addLayout(date_layout, 0, 1)
        layout.addWidget(self.type_label, 1, 0)
        layout.addWidget(self.type_combo, 1, 1)
        layout.addWidget(self.title_label, 2, 0)
        layout.addWidget(self.title_edit, 2, 1)
        layout.addWidget(self.scripture_label, 3, 0)
        layout.addWidget(self.scripture_edit, 3, 1)
        layout.addWidget(self.content_label, 4, 0)
        layout.addWidget(self.content_edit, 4, 1)
        layout.addWidget(self.this_week_news, 5, 0)
        layout.addLayout(self.news_dynamic_layout, 5, 1)
        layout.addWidget(self.news_add_button, 6, 1)
        layout.addWidget(self.this_week_schedule, 7, 0)
        layout.addLayout(self.schedule_dynamic_layout, 7, 1)
        layout.addWidget(self.schedule_add_button, 8, 1)
        layout.addWidget(self.pray_label, 9, 0)
        layout.addWidget(self.pray_combo, 9, 1)
        layout.addWidget(self.outing_label, 10, 0)
        layout.addWidget(self.outing_group, 10, 1)
        layout.addWidget(self.qt_label, 11, 0)
        layout.addWidget(self.qt_group, 11, 1)
        layout.addWidget(self.joowana_label, 12, 0)
        layout.addWidget(self.joowana_group, 12, 1)
        layout.addWidget(self.generate_button, 0, 3)
        layout.addWidget(self.result_label, 0, 2)
        layout.addWidget(self.result_text, 1, 2, 11, 2)
        layout.addWidget(self.copy_button, 12, 2, 1, 2)
        layout.addWidget(self.birthday_label, 13, 0)
        layout.addWidget(self.birthday_layout, 13, 1)
        layout.addWidget(self.birthday_label2, 14, 0)
        layout.addWidget(self.birthday_layout2, 14, 1)

        central_widget.setLayout(layout)

        # Create a menu bar and menus
        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu('파일')
        self.settings_menu = self.menu_bar.addMenu('설정')

        # 파일 메뉴에 액션 추가
        self.file_action1 = QAction('파일 탭 1', self)
        self.file_action2 = QAction('파일 탭 2', self)
        self.file_menu.addAction(self.file_action1)
        self.file_menu.addAction(self.file_action2)

        self.dark_mode_action = QAction('다크 모드', self, checkable=True)
        self.dark_mode_action.setChecked(self.dark_mode)
        self.settings_menu.addAction(self.dark_mode_action)
        self.dark_mode_action.triggered.connect(self.toggle_dark_mode)
        self.dark_stylesheet = """
                    QMainWindow {
                        background-color: #333;
                        color: white;
                    }
                    QMenuBar {
                        background-color: #555;
                        color: white;
                    }
                    QMenuBar::item {
                        background-color: #555;
                        color: white;
                        padding: 4px 10px;
                        border-radius: 4px;
                    }
                    QMenuBar::item:selected {
                        background-color: #888;
                    }
                    QMenu {
                        background-color: #555;
                        color: white;
                        border: 1px solid #888;
                    }
                    QMenu::item {
                        background-color: transparent;
                    }
                    QMenu::item:selected {
                        background-color: #888;
                    }
                    QPushButton {
                        background-color: #1E90FF;
                        color: white;
                    }
                    QPushButton:hover {
                        background-color: #63B8FF;
                    }
                    QTextEdit, QLineEdit, QComboBox, QCheckBox, QRadioButton {
                        background-color: #444;
                        color: white;
                        border: 1px solid #888;
                        border-radius: 4px;
                    }
                    QLabel {
                        color: white;
                    }
                """
        self.light_stylesheet = ""
        self.birthday_list = []
        # 초기 테마 설정
        self.set_theme()

        self.statusBar().showMessage('Ready')

        self.setWindowTitle('마을 인스타 게시물 생성기')
        self.show()

    def toggle_dark_mode(self):
        self.setting.set_settings("darkmode", not self.dark_mode)
        self.dark_mode = not self.dark_mode
        self.set_theme()

    def set_theme(self):
        if self.dark_mode:
            self.setStyleSheet(self.dark_stylesheet)
        else:
            self.setStyleSheet(self.light_stylesheet)

    def show_calendar_popup(self):
        calendar_popup = CalendarPopup(self)
        if calendar_popup.exec_():
            selected_date = calendar_popup.selected_date.toString('yyyy-MM-dd')
            self.date_edit.setText(selected_date)
            selected_date = calendar_popup.selected_date.toString('yyMMdd')
            if self.setting.get_settings("birthday_file") is not None:
                self.birthday_list = self.util.이번주생일자조회(selected_date)

    def on_type_changed(self):
        if self.type_combo.currentText() == '블로그':
            self.author_label.hide()
            self.author_group.hide()
        else:
            self.author_label.show()
            self.author_group.show()

    def add_news_input(self):
        new_text_edit = QLineEdit()
        delete_button = QPushButton('삭제')
        delete_button.clicked.connect(lambda: self.delete_news_input(new_text_edit, delete_button))
        delete_button.setStyleSheet("""
                            QPushButton {
                                background-color: #d43526;
                                color: white;
                            }
                            QPushButton:hover {
                                background-color: #d16c62;
                            }
                        """)


        new_layout = QHBoxLayout()
        new_layout.addWidget(new_text_edit)
        new_layout.addWidget(delete_button)

        self.news_dynamic_layout.addLayout(new_layout)
        self.news_list.append(new_text_edit)

    def delete_news_input(self, text_widget, button_widget):
        text_widget.hide()
        button_widget.hide()
        self.news_list.remove(text_widget)

    def add_schedule_input(self):
        new_text_edit = QLineEdit()
        delete_button = QPushButton('삭제')
        delete_button.clicked.connect(lambda: self.delete_schedule_input(new_text_edit, delete_button))
        delete_button.setStyleSheet("""
                            QPushButton {
                                background-color: #d43526;
                                color: white;
                            }
                            QPushButton:hover {
                                background-color: #d16c62;
                            }
                        """)

        new_layout = QHBoxLayout()
        new_layout.addWidget(new_text_edit)
        new_layout.addWidget(delete_button)

        self.schedule_dynamic_layout.addLayout(new_layout)
        self.schedule_list.append(new_text_edit)

    def delete_schedule_input(self, text_widget, button_widget):
        text_widget.hide()
        button_widget.hide()
        self.schedule_list.remove(text_widget)

    def generate_text(self):
        date = self.date_edit.text()
        text_type = self.type_combo.currentText()
        title = self.title_edit.text()
        scripture = self.scripture_edit.text()
        content = self.content_edit.toPlainText()
        pray = self.pray_combo.currentText()

        weekday = datetime.date(int(date[:4]), int(date[5:7]), int(date[8:10])).weekday()
        week = ['월', '화', '수', '목', '금', '토', '일']
        if text_type in ['마하나임 예배', '더원 예배'] and weekday != 6:
            QMessageBox.warning(self, '요일 오입력 방지', f'{text_type} 날짜가 {week[weekday]}요일로 입력되어있습니다.')


        result = f"{date[2:4]}.{date[5:7]}.{date[8:10]} {text_type}\n\n"
        if title:
            result += f"[{title}] {scripture}\n\n"
        result += f"{content}\n\n"

        if len(self.news_list) > 0:
            result += f"🪨이번 주 소식🪨\n"
            for news in self.news_list:
                result += f"✔️{news.text()}\n"
            result += "\n"

        if len(self.schedule_list) > 0:
            result += f"🪨이번 주 일정🪨\n"
            for schedule in self.schedule_list:
                result += f"✔️{schedule.text()}\n"
            result += "\n"

        result += f"📣 이번 주 기도인도: {pray}\n"
        if self.outing_radio1.isChecked():
            result += "❗️ 더원 예배 뒤에 아웃팅 있습니다!\n"

        if len(self.birthday_list) != 0:
            result += "🎂 이번 주 생일자: "
            for b in self.birthday_list:
                result += f"{b}, "
            result = result[:-2]
            result += "\n"

        if self.qt_check1 or self.qt_check2 or self.qt_check3 or self.qt_check4 or self.qt_check5:
            day = ""
            if self.qt_check1.isChecked():
                day += "월, "
            if self.qt_check2.isChecked():
                day += "화, "
            if self.qt_check3.isChecked():
                day += "수, "
            if self.qt_check4.isChecked():
                day += "목, "
            if self.qt_check5.isChecked():
                day += "금, "
            day = day[0:-2]
            result += f"📖 {day} 큐티모임\n"

        if self.joowana_radio1.isChecked():
            result += "🙏🏻 수요일 주와나 벧엘데이\n"
        else:
            result += "🙏🏻 주와나 특새\n"
        self.result_text.setPlainText(result)

    def copy_result_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.result_text.toPlainText())

    def attach_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog  # macOS에서 필수: 네이티브 파일 대화상자 사용 안 함
        file_names, _ = QFileDialog.getOpenFileNames(self, "파일 첨부", "", "Excel Files (*.xls *.xlsx)",
                                                   options=options)
        # 파일을 저장하는 함수 호출
        success = util.출석파일저장(file_names)
        if success:
            QMessageBox.information(self, "성공", "파일이 성공적으로 저장되었습니다.")
            self.setting.set_settings("birthday_file", util.count_birthday_db())
        else:
            QMessageBox.warning(self, "오류", "파일 저장 중 오류가 발생했습니다.")


    def attach_file2(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog  # macOS에서 필수: 네이티브 파일 대화상자 사용 안 함
        file_name, _ = QFileDialog.getOpenFileName(self, "파일 첨부", "", "Excel Files (*.xls *.xlsx)",
                                                   options=options)
        if file_name:
            # 확장자 확인 (csv 또는 excel 파일만 허용)
            if file_name.lower().endswith(('.csv', '.xls', '.xlsx')):
                self.attach_file_text.setText(file_name)
                # 파일을 저장하는 함수 호출
                success = util.마을원저장(file_name)
                if success:
                    QMessageBox.information(self, "성공", "파일이 성공적으로 저장되었습니다.")
                    self.setting.set_settings("birthday_file", util.count_birthday_db())
                else:
                    QMessageBox.warning(self, "오류", "파일 저장 중 오류가 발생했습니다.")

            else:
                QMessageBox.warning(self, "잘못된 파일 형식", "CSV 파일 또는 Excel 파일만 첨부할 수 있습니다.")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = TextGeneratorApp()
    sys.exit(app.exec_())