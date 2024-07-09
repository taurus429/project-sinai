import datetime
import sqlite3
import pandas as pd


class Util:
    def __init__(self):
        self.conn = sqlite3.connect('db.sqlite3')
        self.cursor = self.conn.cursor()
    def select_all(self, table):

        # 학생 테이블 조회
        self.cursor.execute(f"SELECT * FROM {table};")
        res = self.cursor.fetchall()

        # 학생 데이터 출력
        for r in res:
            print(r)
        return res

    def __del__(self):
        # 변경 사항 저장 및 연결 종료
        self.conn.commit()
        self.conn.close()