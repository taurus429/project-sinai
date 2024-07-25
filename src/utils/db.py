import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout

# 데이터베이스 연결 (데이터베이스 파일이 존재하지 않으면 생성됩니다)
conn = sqlite3.connect('example.db')

# 커서 생성
cursor = conn.cursor()

# 테이블 생성
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )
''')

# 데이터 삽입
cursor.execute('''
    INSERT INTO users (name, age)
    VALUES ('Alice', 30), ('Bob', 25), ('Charlie', 35)
''')

# 데이터 저장 (커밋)
conn.commit()

# 데이터 조회
cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()
for row in rows:
    print(row)

# 연결 종료
conn.close()


class DB_access():

    def __init__(self):
        super().__init__()
        print("dbacess 생성 완료")

    def insert(self, data):
        print(data)