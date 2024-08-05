import datetime
import sqlite3
import pandas as pd
import os

from PyQt5.QtWidgets import QMessageBox

import 날짜유틸
from datetime import datetime, timedelta
class Util:
    def __init__(self):
        self.conn = sqlite3.connect('db.sqlite3')
        self.cursor = self.conn.cursor()

    def init(self):
        # 테이블 삭제 쿼리
        drop_table_queries = [
            "DROP TABLE IF EXISTS 참석;",
            "DROP TABLE IF EXISTS 모임;",
            "DROP TABLE IF EXISTS 사랑_소속;",
            "DROP TABLE IF EXISTS 텀;",
            "DROP TABLE IF EXISTS 마을원;",
            "DROP TABLE IF EXISTS 모임_코드;",
            "DROP TABLE IF EXISTS 구분_코드;",
            "DROP TABLE IF EXISTS 배치관계;"
        ]

        # 테이블 생성 쿼리
        create_table_queries = [
            """
            CREATE TABLE 마을원 (
                uid INTEGER PRIMARY KEY AUTOINCREMENT,
                또래 VARCHAR(3) NOT NULL,
                이름 VARCHAR(100) NOT NULL,
                구분 VARCHAR(2), 
                생년월일 DATE NOT NULL,
                성별 VARCHAR(7) NOT NULL,
                전화번호 VARCHAR(15),
                사랑장 VARCHAR(15), 
                장결여부 BOOLEAN NOT NULL DEFAULT FALSE,
                졸업여부 BOOLEAN NOT NULL DEFAULT FALSE,
                리더여부 BOOLEAN NOT NULL DEFAULT FALSE,
                빠른여부 BOOLEAN NOT NULL DEFAULT FALSE,
                또래장 BOOLEAN NOT NULL DEFAULT FALSE,
                FOREIGN KEY (구분) REFERENCES 구분_코드(구분이름)
            );
            """,
            """
            CREATE TABLE 텀 (
                uid INTEGER PRIMARY KEY AUTOINCREMENT,
                텀이름 VARCHAR(100) NOT NULL,
                시작주일 DATE NOT NULL,
                마지막주일 DATE NOT NULL,
                목자_uid INTEGER,
                FOREIGN KEY (목자_uid) REFERENCES 마을원(uid)
            );
            """,
            """
            CREATE TABLE 사랑_소속 (
                uid INTEGER PRIMARY KEY AUTOINCREMENT,
                사랑장_uid INTEGER NOT NULL,
                사랑원_uid INTEGER NOT NULL,
                날짜 DATE NOT NULL,
                FOREIGN KEY (사랑장_uid) REFERENCES 마을원(uid),
                FOREIGN KEY (사랑원_uid) REFERENCES 마을원(uid)
            );
            """,
            """
            CREATE TABLE 모임 (
                uid INTEGER PRIMARY KEY AUTOINCREMENT,
                모임_코드 INTEGER NOT NULL,
                날짜 DATE NOT NULL,
                상세 VARCHAR(100),
                FOREIGN KEY (모임_코드) REFERENCES 모임_코드(코드)
            );
            """,
            """
            CREATE TABLE 참석 (
                마을원_uid INTEGER,
                모임_uid INTEGER,
                참석여부 BOOLEAN NOT NULL,
                PRIMARY KEY (마을원_uid, 모임_uid),
                FOREIGN KEY (마을원_uid) REFERENCES 마을원(uid),
                FOREIGN KEY (모임_uid) REFERENCES 모임(uid)
            );
            """,
            """
            CREATE TABLE 모임_코드 (
                코드 INTEGER PRIMARY KEY AUTOINCREMENT,
                설명 VARCHAR(50) NOT NULL,
                배경색깔 VARCHAR(10) NOT NULL,
                글자색깔 VARCHAR(10) NOT NULL,
                모임횟수 INTEGER
            )
            """,
            """
            CREATE TABLE 구분_코드 (
                코드 INTEGER PRIMARY KEY AUTOINCREMENT,
                구분이름 VARCHAR(50) NOT NULL,
                구분색깔 VARCHAR(10) NOT NULL,
                설명 VARCHAR(50),
                자동할당 BOOLEAN NOT NULL DEFAULT TRUE,
                사랑배치 BOOLEAN NOT NULL DEFAULT TRUE,
                순서 INTEGER
            )
            """,
            """
            CREATE TABLE 배치관계 (
                마을원1_uid INTEGER NOT NULL,
                마을원2_uid INTEGER NOT NULL,
                배치 VARCHAR(4) NOT NULL,
                FOREIGN KEY (마을원1_uid) REFERENCES 마을원(uid),
                FOREIGN KEY (마을원2_uid) REFERENCES 마을원(uid)
            )
            """
        ]
        # 초기 데이터
        init_data = [
            [('자체예배', '#ff595e', '#ffffff'), ('더원', '#ff595e', '#ffffff'), ('사랑모임', '#f79824', '#ffffff'), ('소울기도회', '#008148', '#ffffff'), ('금철', '#1982c4', '#ffffff'), ('대예배', '#6a4c93', '#ffffff'), ('주와나', '#ffb5a7', '#ffffff'), ('벧엘의밤', '#000000', '#ffffff'),
             ('아웃팅', '#00a896', '#ffffff'), ('리트릿', '#e9589e', '#ffffff'), ('큐티모임', '#27187e', '#ffffff'), ('선교모임', '#656d4a', '#ffffff'), ('아웃리치', '#000000', '#ffffff'), ('또래모임', '#b37dff', '#ffffff'), ('수련회', '#3e71ff', '#ffffff')]
            , [('23년 3텀', '2023-10-15', '2023-12-31', '20'),
               ('24년 1텀', '2024-01-07', '2024-03-31', '20'),
               ('24년 2텀', '2024-04-07', '2024-12-31', '20')]
            , [('L', '#cdb4db', '리더', False, False, 1), ('T', '#b0c4b1', '타지', False, True, 2), ('G', '#d6ccc2', '졸업', False, False, 3), ('J', '#f7e1d7', '장결', False, True, 4), ('S', '#ffc8dd', '새가족', False, True, 5),
               ('A', '#e76f51', '출석구분', True, True, 6), ('B', '#f4a261', '출석구분', True, True, 7), ('C', '#e9c46a', '출석구분', True, True, 8), ('D', '#2a9d8f', '출석구분', True, True, 9), ('E', '#457b9d', '출석구분', True, True, 10), ]
        ]
        # 초기 데이터 삽입 쿼리
        insert_table_queries = [
            """
            INSERT INTO 모임_코드 (설명, 배경색깔, 글자색깔) VALUES (?, ?, ?)
        """,
            """
            INSERT INTO 텀 (텀이름, 시작주일, 마지막주일, 목자_uid) VALUES (?, ?, ?, ?)
        """,
            """
            INSERT INTO 구분_코드 (구분이름, 구분색깔, 설명, 자동할당, 사랑배치, 순서) VALUES (?, ?, ?, ?, ?, ?)
        """
        ]

        # 기존 테이블 삭제
        for query in drop_table_queries:
            self.cursor.execute(query)

        # 새 테이블 생성
        for query in create_table_queries:
            self.cursor.execute(query)

        # 초기 데이터 입력
        for i in range(len(init_data)):
            self.cursor.executemany(insert_table_queries[i], init_data[i])


    def 출석파일저장(self, file_paths):
        time = [(0, 12), (0, 15), (0, 17), (-2, 21)]
        code2desc, desc2code = self.모임코드조회()
        for file_path in file_paths:
            if file_path:
                if file_path.lower().endswith(('.xls', '.xlsx')):
                    df = pd.read_excel(file_path, header=None)
                else:
                    raise ValueError("Unsupported file type")

                year = int(df.iloc[0, 0].split()[0][:4])

                # 날짜 형식 맞춰서 열마다 달아주기
                for col in range(3, df.shape[1], 4):
                    if not pd.isna(df.iloc[2, col]):
                        month = int(df.iloc[2, col].split()[1][0:-1])
                        day = int(df.iloc[2, col].split()[2][0:-1])
                        date = datetime(year, month, day)
                        for i in range(4):
                            time_date = date + timedelta(days=time[i][0], hours=time[i][1])
                            full_date = time_date.strftime('%Y-%m-%d %H:%M:%S')
                            df.iloc[2, col + i] = full_date
                # 지난 금철 => 금철로 바꾸기
                for col in range(3, df.shape[1]):
                    if df.iloc[3, col] == "지난 금철":
                        df.iloc[3, col] = "금철"

                # 사랑원 데이터 추출
                people_list = []
                for row in range(4, df.shape[0]):
                    if df.iloc[row, 0] == "합계":
                        break
                    people_list.append((df.iloc[row, 0], df.iloc[row, 1], df.iloc[row, 2]))

                # 모임 데이터 입력
                for col in range(3, df.shape[1]):
                    if not pd.isna(df.iloc[3, col]):
                        모임날짜 = df.iloc[2, col]
                        모임구분 = desc2code[df.iloc[3, col]][0]
                        self.cursor.execute("SELECT uid FROM 모임 WHERE 모임_코드=? AND 날짜=?", (모임구분, 모임날짜))
                        result = self.cursor.fetchone()
                        if result is None:
                            self.cursor.execute("INSERT INTO 모임 (모임_코드, 날짜) VALUES (?, ?)", (모임구분, 모임날짜))
                            # (f"모임 추가: {모임구분}, {모임날짜}")

                # 사랑장
                사랑장 = df.iloc[1, df.shape[1] - 2].split()[1]
                사랑장_생년월일 = None
                for person in people_list:
                    if person[1] == 사랑장:
                        사랑장_생년월일 = person[2]
                        break;
                self.cursor.execute("SELECT uid FROM 마을원 WHERE 이름=? AND 생년월일=?", (사랑장, 사랑장_생년월일))
                result = self.cursor.fetchone()
                사랑장_uid = result[0]

                # 마을원 데이터
                for person in people_list:
                    이름 = person[1]
                    생년월일 = person[2]
                    self.cursor.execute("SELECT uid FROM 마을원 WHERE 이름=? AND 생년월일=?", (이름, 생년월일))
                    result = self.cursor.fetchone()
                    마을원_uid = result[0]
                    for col in range(3, df.shape[1]):
                        if not pd.isna(df.iloc[3, col]):
                            모임날짜 = df.iloc[2, col]
                            모임구분 = desc2code[df.iloc[3, col]][0]
                            참석여부 = df.iloc[person[0] + 3, col]
                            self.cursor.execute("SELECT uid FROM 모임 WHERE 모임_코드=? AND 날짜=?", (모임구분, 모임날짜))
                            result = self.cursor.fetchone()
                            모임_uid = result[0]

                            self.cursor.execute("SELECT 참석여부 FROM 참석 WHERE 마을원_uid=? AND 모임_uid=?",
                                                (마을원_uid, 모임_uid))
                            result = self.cursor.fetchone()
                            if result:  # 업데이트
                                self.cursor.execute("UPDATE 참석 SET 참석여부=? WHERE 마을원_uid=? AND 모임_uid=?",
                                                    (참석여부, 마을원_uid, 모임_uid))
                                # print(f"참석 수정: {마을원_uid}, {모임_uid}, {참석여부}")
                            else:  # 인서트
                                self.cursor.execute("INSERT INTO 참석 (마을원_uid, 모임_uid, 참석여부) VALUES (?, ?, ?)",
                                                    (마을원_uid, 모임_uid, 참석여부))
                                # print(f"참석 추가: {마을원_uid}, {모임_uid}, {참석여부}

                        # 사랑 소속 데이터
                        if col % 4 == 3 and not pd.isna(df.iloc[person[0] + 3, col]):
                            날짜 = df.iloc[2, col].split()[0]
                            self.cursor.execute("SELECT uid FROM 사랑_소속 WHERE 사랑장_uid=? AND 사랑원_uid=? AND 날짜=?",
                                                (사랑장_uid, 마을원_uid, 날짜))
                            사랑소속_uid = self.cursor.fetchone()
                            if result:  # 업데이트
                                self.cursor.execute("UPDATE 사랑_소속 SET 사랑장_uid=?, 사랑원_uid=?, 날짜=? WHERE uid=?",
                                                    (사랑장_uid, 마을원_uid, 날짜, 사랑소속_uid[0]))
                            else:  # 인서트
                                self.cursor.execute("INSERT INTO 사랑_소속 (사랑장_uid, 사랑원_uid, 날짜) VALUES (?, ?, ?)",
                                                    (사랑장_uid, 마을원_uid, 날짜))

            print(f"{file_path} 저장 성공")

        return True

    def 마을원저장(self, file_path):
        try:
            if file_path.lower().endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file_path, header=None)
            else:
                raise ValueError("Unsupported file type")

            for index, row in df.iterrows():
                이름, 또래, 생년월일, 전화번호, 성별 = row[0].split()[1], str(row[1])[:2], row[1], row[2], row[3]
                self.cursor.execute("SELECT uid FROM 마을원 WHERE 이름=? AND 생년월일=?", (이름, 생년월일))
                result = self.cursor.fetchone()
                if result is None:
                    self.cursor.execute("INSERT INTO 마을원 (이름, 또래, 생년월일, 성별, 전화번호) VALUES (?, ?, ?, ?, ?)",
                                        (이름, 또래, 생년월일, 성별, 전화번호))
                    # print(f"마을원 추가: {이름}, {생년월일}, {성별}, {전화번호}")
            return True

        except Exception as e:
            print(f"Error: {e}")
            return False

    def 모임저장(self, file_path):
        try:
            if file_path.lower().endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file_path, header=None)
            else:
                raise ValueError("Unsupported file type")

            code2desc, desc2code = self.모임코드조회()
            meeting_names = df.iloc[0, 2:].values
            meeting_dates = df.iloc[1, 2:].values

            # Prepare the list to hold the tuples
            attendance_list = []

            # Iterate over each row of student data
            for i in range(2, df.shape[0]):
                name = df.iloc[i, 0].split()[1]
                birth_date = str(int(df.iloc[i, 1]))
                self.cursor.execute("SELECT uid FROM 마을원 WHERE 이름=? AND 생년월일=?", (name, birth_date))
                마을원_uid = self.cursor.fetchone()[0]

                # Iterate over each meeting column for the student
                for j in range(2, df.shape[1]):
                    attendance = df.iloc[i, j]
                    if not pd.isna(attendance):  # Skip NaN values
                        attendance_tuple = (name, birth_date, meeting_names[j - 2], meeting_dates[j - 2], attendance)
                        모임날짜 = meeting_dates[j - 2]
                        모임구분 = desc2code[meeting_names[j - 2]][0]
                        self.cursor.execute("SELECT uid FROM 모임 WHERE 모임_코드=? AND 날짜=?", (모임구분, 모임날짜))
                        모임_uid = self.cursor.fetchone()
                        if 모임_uid is None:
                            self.cursor.execute("INSERT INTO 모임 (모임_코드, 날짜) VALUES (?, ?)", (모임구분, 모임날짜))
                            self.cursor.execute("SELECT uid FROM 모임 WHERE 모임_코드=? AND 날짜=?", (모임구분, 모임날짜))
                            모임_uid = self.cursor.fetchone()
                        모임_uid = 모임_uid[0]
                        self.cursor.execute("SELECT 참석여부 FROM 참석 WHERE 마을원_uid=? AND 모임_uid=?",
                                            (마을원_uid, 모임_uid))
                        result = self.cursor.fetchone()
                        if result:  # 업데이트
                            self.cursor.execute("UPDATE 참석 SET 참석여부=? WHERE 마을원_uid=? AND 모임_uid=?",
                                                (attendance, 마을원_uid, 모임_uid))
                            # print(f"참석 수정: {마을원_uid}, {모임_uid}, {참석여부}")
                        elif not pd.isna(attendance):  # 인서트
                            self.cursor.execute("INSERT INTO 참석 (마을원_uid, 모임_uid, 참석여부) VALUES (?, ?, ?)",
                                                (마을원_uid, 모임_uid, attendance))
                        attendance_list.append(attendance_tuple)
            print("모임 저장 성공")
            return True

        except Exception as e:
            print(f"Error: {e}")
            return False


    def select_all(self, table):

        try:
            # 마을원 테이블 조회
            self.cursor.execute(f"SELECT * FROM {table};")
            res = self.cursor.fetchall()

            columns = [desc[0] for desc in self.cursor.description]

            # 헤더와 데이터를 포함한 결과 생성
            result_with_header = [columns] + res

            return result_with_header

        except Exception as e:
            print(f"Error: {e}")
            return None

    def 참석조회(self, 마을원_uid):
        try:
            self.cursor.execute("SELECT A.참석여부, C.모임_코드, C.날짜 "
                                "FROM 참석 A "
                                "LEFT JOIN 마을원 B ON A.마을원_uid = B.uid "
                                "LEFT JOIN 모임 C ON A.모임_uid = C.uid "
                                "WHERE A.마을원_uid=? "
                                "ORDER BY C.날짜 desc", (마을원_uid,))
        except Exception as e:
            print(f"Error: {e}")
            return None
        res = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]

        # 헤더와 데이터를 포함한 결과 생성
        result_with_header = [columns] + res

        return result_with_header

    def 마을원정보조회(self, 마을원_uid):
        try:
            self.cursor.execute("SELECT * FROM 마을원 WHERE uid = ?", (마을원_uid,))
        except Exception as e:
            print(f"Error: {e}")
            return None
        res = self.cursor.fetchone()

        columns = [desc[0] for desc in self.cursor.description]

        result = dict()
        for i in range(len(columns)):
            result[columns[i]] = res[i]

        return result

    def 사랑장조회(self, 사랑원_uid):
        try:
            self.cursor.execute("SELECT DISTINCT "
                                "m.이름 as 사랑장이름, t.텀이름, s.사랑장_uid = ? as 사랑장여부 "
                                "FROM 사랑_소속 s "
                                "JOIN 텀 t ON s.날짜 "
                                "BETWEEN t.시작주일 AND t.마지막주일 "
                                "JOIN 마을원 m ON s.사랑장_uid = m.uid "
                                "WHERE s.사랑원_uid = ? "
                                "ORDER BY t.텀이름 asc", (사랑원_uid, 사랑원_uid,))
        except Exception as e:
            print(f"Error: {e}")
            return None
        res = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]

        # 헤더와 데이터를 포함한 결과 생성
        result_with_header = [columns] + res

        return result_with_header

    def 모임조회(self):
        try:
            self.cursor.execute("SELECT "
                                "모임.uid AS 모임_UID, "
                                "모임.날짜 AS 날짜, "
                                "모임.모임_코드 AS 모임_코드, "
                                "SUM(참석.참석여부) AS 참석자수, "
                                "ROUND(AVG(CASE WHEN 참석.참석여부 = 1 THEN 100 ELSE 0 END), 2) AS 참석률 "
                                "FROM 모임 "
                                "LEFT JOIN "
                                "참석 ON 모임.uid = 참석.모임_uid "
                                "GROUP BY 모임.uid, 모임.날짜, 모임.모임_코드 "
                                "ORDER BY 날짜 DESC")
        except Exception as e:
            print(f"Error: {e}")
            return None
        res = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]

        # 헤더와 데이터를 포함한 결과 생성
        result_with_header = [columns] + res

        return result_with_header

    def 모임코드조회(self):
        try:
            # Update the meeting count
            self.cursor.execute('''
                UPDATE 모임_코드
                SET 모임횟수 = (
                    SELECT COUNT(*)
                    FROM 모임
                    WHERE 모임.모임_코드 = 모임_코드.코드
                )
            ''')

            # Commit the transaction to save changes
            self.conn.commit()

            # Fetch all records
            self.cursor.execute("SELECT * FROM 모임_코드")
        except Exception as e:
            print(f"Error: {e}")
            self.conn.rollback()  # Rollback changes on error
            return None

        res = self.cursor.fetchall()

        code2desc = dict()
        desc2code = dict()

        for r in res:
            code2desc[r[0]] = r
            desc2code[r[1]] = r

        return code2desc, desc2code

    def 마을원전체조회(self):
        try:
            self.cursor.execute("SELECT * FROM 마을원")
        except Exception as e:
            print(f"Error: {e}")
            return None
        res = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]

        # 헤더와 데이터를 포함한 결과 생성
        result_with_header = [columns] + res

        return result_with_header

    def 또래분포조회(self, 장결여부, 졸업여부):
        try:
            # Build the base query
            query = """
                SELECT 또래, COUNT(*) AS 인원수 
                FROM 마을원 
                WHERE 1=1
            """

            # Append conditions based on the given parameters
            if 장결여부 is not None:
                if 장결여부:
                    query += " AND (장결여부 = 1 OR 장결여부 = 0)"
                else:
                    query += " AND 장결여부 = 0"

            if 졸업여부 is not None:
                if 졸업여부:
                    query += " AND (졸업여부 = 1 OR 졸업여부 = 0)"
                else:
                    query += " AND 졸업여부 = 0"

            # Group by gender
            query += " GROUP BY 또래"

            # Execute the constructed query
            self.cursor.execute(query)
        except Exception as e:
            print(f"Error: {e}")
            return None

        # Fetch the results
        res = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]

        # Include headers in the result
        result_with_header = [columns] + res

        return result_with_header

    def 성별분포조회(self, 장결여부, 졸업여부):
        try:
            # Build the base query
            query = """
                SELECT 성별, COUNT(*) AS 인원수 
                FROM 마을원 
                WHERE 1=1
            """

            # Append conditions based on the given parameters
            if 장결여부 is not None:
                if 장결여부:
                    query += " AND (장결여부 = 1 OR 장결여부 = 0)"
                else:
                    query += " AND 장결여부 = 0"

            if 졸업여부 is not None:
                if 졸업여부:
                    query += " AND (졸업여부 = 1 OR 졸업여부 = 0)"
                else:
                    query += " AND 졸업여부 = 0"

            # Group by gender
            query += " GROUP BY 성별"

            # Execute the constructed query
            self.cursor.execute(query)
        except Exception as e:
            print(f"Error: {e}")
            return None

        # Fetch the results
        res = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]

        # Include headers in the result
        result_with_header = [columns] + res

        return result_with_header

    def 구분분포조회(self, 장결여부, 졸업여부):
        try:
            # Build the base query
            query = """
                SELECT 구분, COUNT(*) AS 인원수 
                FROM 마을원 
                WHERE 1=1
            """

            # Append conditions based on the given parameters
            if 장결여부 is not None:
                if 장결여부:
                    query += " AND (장결여부 = 1 OR 장결여부 = 0)"
                else:
                    query += " AND 장결여부 = 0"

            if 졸업여부 is not None:
                if 졸업여부:
                    query += " AND (졸업여부 = 1 OR 졸업여부 = 0)"
                else:
                    query += " AND 졸업여부 = 0"

            # Group by gender
            query += " GROUP BY 구분"

            # Execute the constructed query
            self.cursor.execute(query)
        except Exception as e:
            print(f"Error: {e}")
            return None

        # Fetch the results
        res = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]

        # Include headers in the result
        result_with_header = [columns] + res

        return result_with_header

    def 참석통계(self, 마을원_uid):
        참석횟수 = []
        try:
            for 모임코드 in self.모임코드조회()[0].keys():
                self.cursor.execute("""
                    WITH RankedAttendance AS (
                        SELECT 
                            참석.마을원_uid,
                            모임.모임_코드,
                            COUNT(*) AS 참석횟수, 
                            RANK() OVER (ORDER BY COUNT(*) DESC) AS 참석횟수랭킹
                        FROM 참석 
                        JOIN 모임 ON 참석.모임_uid = 모임.uid
                        WHERE 모임.모임_코드 = ? 
                          AND 참석.참석여부 = TRUE
                        GROUP BY 참석.마을원_uid
                    )
                    SELECT 모임_코드, 참석횟수, 참석횟수랭킹
                    FROM RankedAttendance
                    WHERE 마을원_uid = ?;
                """, (모임코드, 마을원_uid,))
                참석횟수.append(self.cursor.fetchall())
        except Exception as e:
            print(f"Error: {e}")
            return None

        참석률 = []
        try:
            for 모임코드 in self.모임코드조회()[0].keys():
                self.cursor.execute('''
                                    WITH AttendanceRates AS (
                                        SELECT 
                                            참석.마을원_uid,
                                            (SUM(CASE WHEN 참석.참석여부 = TRUE THEN 1 ELSE 0 END) * 1.0 / COUNT(*)) * 100 AS 참석률,
                                            RANK() OVER (ORDER BY (SUM(CASE WHEN 참석.참석여부 = TRUE THEN 1 ELSE 0 END) * 1.0 / COUNT(*)) DESC) AS 참석률랭킹
                                        FROM 참석 
                                        JOIN 모임 ON 참석.모임_uid = 모임.uid
                                        WHERE 모임.모임_코드 = ?
                                        GROUP BY 참석.마을원_uid
                                    )
                                    SELECT 참석률, 참석률랭킹
                                    FROM AttendanceRates
                                    WHERE 마을원_uid = ?;

                ''', (모임코드, 마을원_uid,))
                참석률.append(self.cursor.fetchall())
        except Exception as e:
            print(f"Error: {e}")
            return None
        res = []
        for i in range(len(참석횟수)):
            res.append(참석횟수[i]+참석률[i])
        columns = [desc[0] for desc in self.cursor.description]

        # 헤더와 데이터를 포함한 결과 생성
        result_with_header = [columns] + res

        return result_with_header

    def 장결등록(self, 마을원_uid):
        try:
            # Update the meeting count
            self.cursor.execute('''
                UPDATE 마을원
                SET 장결여부 = 1, 구분 = 'J' 
                WHERE uid = ?
            ''', (마을원_uid,))

            # Commit the transaction to save changes
            self.conn.commit()

        except Exception as e:
            print(f"Error: {e}")
            self.conn.rollback()  # Rollback changes on error
            return None

        return True

    def 졸업등록(self, 마을원_uid):
        try:
            # Update the meeting count
            self.cursor.execute('''
                UPDATE 마을원
                SET 졸업여부 = 1 , 구분 = 'G' 
                WHERE uid = ?
            ''', (마을원_uid,))

            # Commit the transaction to save changes
            self.conn.commit()

        except Exception as e:
            print(f"Error: {e}")
            self.conn.rollback()  # Rollback changes on error
            return None

        return True

    def 빠른등록(self, 마을원_uid):
        try:
            # Update the meeting count
            self.cursor.execute('''
                UPDATE 마을원
                SET 빠른여부 = 1, 또래 = (SELECT 또래 FROM 마을원 WHERE uid = ?) - 1  
                WHERE uid = ?
            ''', (마을원_uid, 마을원_uid))

            # Commit the transaction to save changes
            self.conn.commit()

        except Exception as e:
            print(f"Error: {e}")
            self.conn.rollback()  # Rollback changes on error
            return None

        return True

    def 또래장등록(self, 마을원_uid):
        try:
            # Update the meeting count
            self.cursor.execute('''
                UPDATE 마을원
                SET 또래장 = 1 
                WHERE uid = ?
            ''', (마을원_uid,))

            # Commit the transaction to save changes
            self.conn.commit()

        except Exception as e:
            print(f"Error: {e}")
            self.conn.rollback()  # Rollback changes on error
            return None

        return True

    def 업데이트_사랑장_리더여부(self):
        try:
            # Update the meeting count
            self.cursor.execute("""
    -- 먼저 사랑장 정보를 가져오기 위한 서브쿼리
WITH MostRecentLeader AS (
    SELECT
        소속.사랑원_uid,
        MAX(소속.날짜) AS 최근_날짜
    FROM 사랑_소속 소속
    GROUP BY 소속.사랑원_uid
),

-- 가장 최근의 사랑장_uid를 가져오기 위한 서브쿼리
RecentLeaders AS (
    SELECT
        소속.사랑원_uid,
        소속.사랑장_uid
    FROM 사랑_소속 소속
    JOIN MostRecentLeader mr ON 소속.사랑원_uid = mr.사랑원_uid AND 소속.날짜 = mr.최근_날짜
),

-- 사랑장 이름을 가져오기 위한 서브쿼리
LeaderNames AS (
    SELECT
        r.사랑원_uid,
        mw.이름 AS 사랑장_이름
    FROM RecentLeaders r
    JOIN 마을원 mw ON r.사랑장_uid = mw.uid
)

-- 최종 업데이트 쿼리
UPDATE 마을원
SET
    사랑장 = COALESCE(ln.사랑장_이름, 마을원.사랑장),  -- 사랑장 이름 업데이트
    리더여부 = CASE
        WHEN 마을원.이름 = ln.사랑장_이름 THEN TRUE
        ELSE FALSE
    END
FROM LeaderNames ln
WHERE 마을원.uid = ln.사랑원_uid;

    """)

            # Commit the transaction to save changes
            self.conn.commit()

        except Exception as e:
            print(f"Error: {e}")
            self.conn.rollback()  # Rollback changes on error
            return None

        return True

    def 목자이력조회(self, 마을원_uid):
        try:
            self.cursor.execute("SELECT 텀이름 FROM 텀 WHERE 목자_uid = ?", (마을원_uid,))
        except Exception as e:
            print(f"Error: {e}")
            return None
        res = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]

        # 헤더와 데이터를 포함한 결과 생성
        result_with_header = [columns] + res

        return result_with_header

    def 모임참석통계(self, 모임코드튜플):
        placeholders = ', '.join(['?'] * len(모임코드튜플))
        try:
            self.cursor.execute(f"""SELECT 
                                                m.날짜 AS 모임_날짜,
                                                mc.설명 AS 모임_이름,
                                                COUNT(a.마을원_uid) AS 참석자_수
                                            FROM 
                                                모임 AS m
                                            JOIN 
                                                참석 AS a ON m.uid = a.모임_uid
                                            JOIN 
                                                모임_코드 AS mc ON m.모임_코드 = mc.코드
                                            WHERE 
                                                m.모임_코드 IN ({placeholders}) 
                                                AND a.참석여부 = 1
                                            GROUP BY 
                                                m.날짜, mc.설명
                                            ORDER BY 
                                                m.날짜;
""", 모임코드튜플)
        except Exception as e:
            print(f"Error: {e}")
            return None
        res = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]

        # 헤더와 데이터를 포함한 결과 생성
        result_with_header = [columns] + res

        return result_with_header

    def 구분코드조회(self, 자동할당 = False):
        try:
            sql = "SELECT * FROM 구분_코드 "
            if 자동할당:
                sql += "WHERE 자동할당 = TRUE "
            sql += "ORDER BY 순서 ASC"
            self.cursor.execute(sql)

        except Exception as e:
            print(f"Error: {e}")
            return None
        res = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]

        # 헤더와 데이터를 포함한 결과 생성
        result_with_header = [columns] + res

        return result_with_header

    def 텀조회(self):
        try:
            self.cursor.execute("SELECT * FROM 텀")
        except Exception as e:
            print(f"Error: {e}")
            return None
        res = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]

        # 헤더와 데이터를 포함한 결과 생성
        result_with_header = [columns] + res

        return result_with_header

    def 참석통계조회(self, 시작날짜):
        try:
            sql = """
                    SELECT
                        m.uid, m.이름"""

            for 모임코드 in self.모임코드조회()[0].keys():
                sql += f""",
                        ROUND(
                            (CAST(COUNT(CASE WHEN mk.코드 = {모임코드} AND a.참석여부 = TRUE THEN 1 END) AS FLOAT) / 
                             NULLIF(COUNT(CASE WHEN mk.코드 = {모임코드} THEN a.모임_uid END), 0)) * 100, 2
                        ) AS 모임{모임코드}_참석률
                        """
            sql += """
                        FROM 
                            참석 a
                        INNER JOIN 
                            모임 mo ON a.모임_uid = mo.uid
                        INNER JOIN 
                            모임_코드 mk ON mo.모임_코드 = mk.코드
                        INNER JOIN 
                            마을원 m ON a.마을원_uid = m.uid
                        LEFT JOIN
                            구분_코드 g ON m.구분 = g.구분이름
                        WHERE 
                            mo.날짜 >= ? AND (m.구분 = '' or m.구분 IS NULL OR (g.자동할당 = TRUE AND m.구분 = g.구분이름))
                        GROUP BY 
                            m.uid;
                    """
            self.cursor.execute(sql, (시작날짜, ))
        except Exception as e:
            print(f"Error: {e}")
            return None
        res = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]

        # 헤더와 데이터를 포함한 결과 생성
        result_with_header = [columns] + res

        return result_with_header

    def 업데이트_구분(self, 구분리스트, 삭제_uid = []):
        try:
            for uid in 삭제_uid:
                self.cursor.execute("""DELETE FROM 구분_코드 WHERE 코드 = ? """, (uid,))
            for 구분 in 구분리스트:
                self.cursor.execute("""
                        INSERT INTO 구분_코드 (코드, 구분이름, 구분색깔, 설명, 자동할당, 사랑배치, 순서)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT(코드) DO UPDATE SET
                            구분이름 = excluded.구분이름,
                            구분색깔 = excluded.구분색깔,
                            설명 = excluded.설명,
                            자동할당 = excluded.자동할당,
                            사랑배치 = excluded.사랑배치,
                            순서 = excluded.순서;
                """, (구분["코드"], 구분["구분이름"], 구분["구분색깔"], 구분["설명"], 구분["자동할당"], 구분["사랑배치"], 구분["순서"], ))

            # Commit the transaction to save changes
            self.conn.commit()

        except Exception as e:
            print(f"Error: {e}")
            QMessageBox.critical(self, "저장 오류", f"데이터 저장 중 오류가 발생했습니다: {str(e)}")
            self.conn.rollback()  # Rollback changes on error
            return None

        return True

    def 구분부여(self, 부여리스트):
        try:
            for b in 부여리스트:
                self.cursor.execute("""UPDATE 마을원 SET 구분 = ? WHERE uid = ? """, (b[2], b[0]))
                # Commit the transaction to save changes
            self.conn.commit()

        except Exception as e:
            print(f"Error: {e}")
            QMessageBox.critical(self, "저장 오류", f"데이터 저장 중 오류가 발생했습니다: {str(e)}")
            self.conn.rollback()  # Rollback changes on error
            return None

        return True

    def 이번주생일자조회(self, yymmdd):
        try:
            # 입력 날짜를 datetime 객체로 변환
            base_date = datetime.strptime(yymmdd, "%y%m%d")
            end_date = base_date + timedelta(days=6)

            # 시작 날짜와 종료 날짜의 mmdd 형식을 추출
            base_mmdd = base_date.strftime("%m%d")
            end_mmdd = end_date.strftime("%m%d")

            # SQL 쿼리를 사용하여 yymmdd의 날짜로부터 7일 이내의 모든 생일자를 추출
            query = f"""
                        SELECT 생년, strftime('%m%d', 생년월일) AS 생일, 이름 FROM birthday
                        WHERE 
                            생일 BETWEEN '{base_mmdd}' AND '{end_mmdd}'
                        ORDER BY 생일 ASC
                        """
            self.cursor.execute(query)

        except Exception as e:
            print(f"Error: {e}")
            return None
        res = self.cursor.fetchall()
        birthday_list = []
        for index, row in res.iterrows():
            birthday_list.append(f"{row['생년']}또래 {row['이름']}({int(row['생일'][2:])}일)")

        return birthday_list

    def 배치대상조회(self):
        try:
            self.cursor.execute("""SELECT * FROM 마을원 m
                                    JOIN 구분_코드 g
                                    ON m.구분 = g.구분이름
                                    WHERE 사랑배치 = 1;""")
        except Exception as e:
            print(f"Error: {e}")
            return None
        res = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]

        # 헤더와 데이터를 포함한 결과 생성
        result_with_header = [columns] + res

        return result_with_header

    def 배치관계조회(self):
        try:
            self.cursor.execute("""SELECT * FROM 배치관계""")
        except Exception as e:
            print(f"Error: {e}")
            return None
        res = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]

        # 헤더와 데이터를 포함한 결과 생성
        result_with_header = [columns] + res

        return result_with_header

    def 업데이트_배치관계(self, 관계리스트):
        try:
            # Update the meeting count
            self.cursor.execute("""DELETE FROM 배치관계""")

            for 관계 in 관계리스트:
                self.cursor.execute("""INSERT INTO 배치관계 (마을원1_uid, 마을원2_uid, 배치) VALUES (?, ?, ?)"""
                                    , (관계[0], 관계[1], 관계[2],))
            # Commit the transaction to save changes
            self.conn.commit()

        except Exception as e:
            print(f"Error: {e}")
            self.conn.rollback()  # Rollback changes on error
            return None

        return True

    def truncate(self, table):
        # 마을원 테이블 조회
        self.cursor.execute(f"DELETE FROM {table};")

    def __del__(self):
        # 변경 사항 저장 및 연결 종료
        self.conn.commit()
        self.conn.close()

u = Util()
# u.init()
# u.마을원저장("C:/Users/85350/Desktop/마을원명단.xlsx")
# dirname = "../data/사랑보고서"
# filenames = os.listdir(dirname)
# file_list = []
# for filename in filenames:
#     full_filename = os.path.join(dirname, filename)
#     file_list.append(full_filename)
#
# u.출석파일저장(file_list)
# u.모임저장("../data/참석.xlsx")

# u.select_all("마을원")
# u.select_all("참석")
# u.select_all("모임")
#
# filtered_list = [tup for tup in u.참석조회(21)[1:] if tup[0] == 1 and tup[1] in (1, 2)]
#
# # 튜플 리스트의 날짜들을 추출하여 datetime 객체로 변환
# dates = [datetime.strptime(tup[2], '%Y-%m-%d %H:%M:%S') for tup in filtered_list]
#
# # 날짜들을 내림차순으로 정렬 (이미 정렬된 것으로 가정)
# dates.sort(reverse=True)
#
# # 가장 최근 날짜로부터 7일 간격으로 연속된 데이터 개수 계산
# continuous_count = 1  # 첫 번째 날짜는 이미 포함
#
# # 7일 간격 확인
# for i in range(1, len(dates)):
#     if (dates[i - 1] - dates[i]).days == 7:
#         continuous_count += 1
#     else:
#         break  # 7일 간격이 아닌 경우 중단
#
# # 결과 출력
# print("연속된 데이터의 개수:", continuous_count)
#
# filtered_list = [tup for tup in u.참석조회(4)[1:] if tup[0] == 1 and tup[1] == 3]
#
# # 튜플 리스트의 날짜들을 추출하여 datetime 객체로 변환
# dates = [datetime.strptime(tup[2], '%Y-%m-%d %H:%M:%S') for tup in filtered_list]
#
# # 날짜들을 내림차순으로 정렬 (이미 정렬된 것으로 가정)
# dates.sort(reverse=True)
#
# # 가장 최근 날짜로부터 7일 간격으로 연속된 데이터 개수 계산
# continuous_count = 1  # 첫 번째 날짜는 이미 포함
#
# # 7일 간격 확인
# for i in range(1, len(dates)):
#     if (dates[i - 1] - dates[i]).days == 7:
#         continuous_count += 1
#     else:
#         break  # 7일 간격이 아닌 경우 중단
#
# # 결과 출력
# print("연속된 데이터의 개수:", continuous_count)