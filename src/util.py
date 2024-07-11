import datetime
import sqlite3
import pandas as pd


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
            "DROP TABLE IF EXISTS 사랑;",
            "DROP TABLE IF EXISTS 마을원;",
            "DROP TABLE IF EXISTS 모임_코드;"
        ]

        # 테이블 생성 쿼리
        create_table_queries = [
            """
            CREATE TABLE 마을원 (
                uid INTEGER PRIMARY KEY AUTOINCREMENT,
                이름 VARCHAR(100) NOT NULL,
                생년월일 DATE NOT NULL,
                성별 VARCHAR(7) NOT NULL,
                전화번호 VARCHAR(15)
            );
            """,
            """
            CREATE TABLE 사랑 (
                uid INTEGER PRIMARY KEY AUTOINCREMENT,
                사랑장_uid INTEGER,
                설립일자 DATE NOT NULL,
                FOREIGN KEY (사랑장_uid) REFERENCES 마을원(uid)
            );
            """,
            """
            CREATE TABLE 사랑_소속 (
                마을원_uid INTEGER,
                사랑_uid INTEGER,
                PRIMARY KEY (마을원_uid, 사랑_uid),
                FOREIGN KEY (마을원_uid) REFERENCES 마을원(uid),
                FOREIGN KEY (사랑_uid) REFERENCES 사랑(uid)
            );
            """,
            """
            CREATE TABLE 모임 (
                uid INTEGER PRIMARY KEY AUTOINCREMENT,
                모임_구분 VARCHAR(50) NOT NULL,
                날짜 DATE NOT NULL
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
                설명 VARCHAR(50) NOT NULL
            )
            """
        ]
        # 초기 데이터
        initial_data = [
            ('자체예배',),
            ('더원',),
            ('사랑모임',),
            ('금철',),
            ('대예배',)
        ]
        # 초기 데이터 삽입 쿼리
        insert_table_queries = [
            """
        INSERT INTO 모임_코드 (설명) VALUES (?)
        """
        ]

        # 기존 테이블 삭제
        for query in drop_table_queries:
            self.cursor.execute(query)

        # 새 테이블 생성
        for query in create_table_queries:
            self.cursor.execute(query)
        
        # 초기 데이터 입력
        for query in insert_table_queries:
            self.cursor.executemany(query, initial_data)


    def show(self):

        # 데이터베이스 안의 모든 테이블 이름 조회
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()

        # 각 테이블의 컬럼 정보 조회 및 출력
        for table in tables:
            table_name = table[0]
            print(f"Table: {table_name}")

            self.cursor.execute(f"PRAGMA table_info({table_name});")
            columns = self.cursor.fetchall()

            for column in columns:
                print(f"  Column: {column[1]}, Type: {column[2]}")
            print()


    def save(self, file_path):
        try:
            # 파일 확장자에 따라 pandas로 파일 읽기
            if file_path.lower().endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.lower().endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file type")


            # 데이터프레임을 테이블로 저장 (테이블 이름: data_table)
            df.to_sql('data_table', self.conn, if_exists='replace', index=False)


            return True

        except Exception as e:
            print(f"Error: {e}")
            return False


    def read(self):
        try:
            # SQL 쿼리를 사용하여 테이블에서 데이터 읽기
            query = "SELECT * FROM data_table"
            df = pd.read_sql_query(query, self.conn)
            print(df)

            return df

        except Exception as e:
            print(f"Error: {e}")
            return None

    def 출석파일저장(self, file_paths):
        time = [(0, 12), (0, 15), (0, 17), (-2, 21)]
        for file_path in file_paths:
            try:
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
                            date = datetime.datetime(year, month, day)
                            for i in range(4):
                                time_date = date + datetime.timedelta(days=time[i][0], hours=time[i][1])
                                full_date = time_date.strftime('%Y-%m-%d %H:%M:%S')
                                df.iloc[2, col+i] = full_date
                    # 지난 금철 => 금철로 바꾸기
                    for col in range(3, df.shape[1]):
                        if df.iloc[3, col] == "지난 금철":
                            df.iloc[3, col] = "금철"

                    #사랑원 데이터 추출
                    people_list = []
                    for row in range(4, df.shape[0]):
                        if df.iloc[row,0] == "합계":
                            break
                        people_list.append((df.iloc[row, 0], df.iloc[row, 1], df.iloc[row, 2]))

                    #모임 데이터 입력
                    for col in range(3, df.shape[1]):
                        if not pd.isna(df.iloc[3, col]):
                            모임날짜 = df.iloc[2, col]
                            모임구분 = df.iloc[3, col]
                            self.cursor.execute("SELECT uid FROM 모임 WHERE 모임_구분=? AND 날짜=?", (모임구분, 모임날짜))
                            result = self.cursor.fetchone()
                            if result is None:
                                self.cursor.execute("INSERT INTO 모임 (모임_구분, 날짜) VALUES (?, ?)", (모임구분, 모임날짜))
                                #(f"모임 추가: {모임구분}, {모임날짜}")

                    #마을원 데이터
                    for person in people_list:
                        이름 = person[1]
                        생년월일 = person[2]
                        self.cursor.execute("SELECT uid FROM 마을원 WHERE 이름=? AND 생년월일=?", (이름, 생년월일))
                        result = self.cursor.fetchone()
                        마을원_uid = result[0]
                        for col in range(3, df.shape[1]):
                            if not pd.isna(df.iloc[3, col]):
                                모임날짜 = df.iloc[2,col]
                                모임구분 = df.iloc[3,col]
                                참석여부 = df.iloc[person[0]+3, col]
                                self.cursor.execute("SELECT uid FROM 모임 WHERE 모임_구분=? AND 날짜=?", (모임구분, 모임날짜))
                                result = self.cursor.fetchone()
                                모임_uid = result[0]

                                self.cursor.execute("SELECT 참석여부 FROM 참석 WHERE 마을원_uid=? AND 모임_uid=?", (마을원_uid, 모임_uid))
                                result = self.cursor.fetchone()
                                if result: #업데이트
                                    self.cursor.execute("UPDATE 참석 SET 참석여부=? WHERE 마을원_uid=? AND 모임_uid=?", (참석여부, 마을원_uid, 모임_uid))
                                    #print(f"참석 수정: {마을원_uid}, {모임_uid}, {참석여부}")
                                else: #인서트
                                    self.cursor.execute("INSERT INTO 참석 (마을원_uid, 모임_uid, 참석여부) VALUES (?, ?, ?)", (마을원_uid, 모임_uid, 참석여부))
                                    #print(f"참석 추가: {마을원_uid}, {모임_uid}, {참석여부}")

                print(f"{file_path} 저장 성공")
            except Exception as e:
                print(f"Error: {e}")
                print(f"{file_path} 저장 중 에러 발생")
                continue
        return True


    def 마을원저장(self, file_path):
        try:
            if file_path.lower().endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file_path, header=None)
            else:
                raise ValueError("Unsupported file type")

            for index, row in df.iterrows():
                이름, 생년월일, 전화번호, 성별 = row[0].split()[1], row[1], row[2], row[3]
                self.cursor.execute("SELECT uid FROM 마을원 WHERE 이름=? AND 생년월일=?", (이름, 생년월일))
                result = self.cursor.fetchone()
                if result is None:
                    self.cursor.execute("INSERT INTO 마을원 (이름, 생년월일, 성별, 전화번호) VALUES (?, ?, ?, ?)", (이름, 생년월일, 성별, 전화번호))
                    #print(f"마을원 추가: {이름}, {생년월일}, {성별}, {전화번호}")


            return True

        except Exception as e:
            print(f"Error: {e}")
            return False

    def read_from_db(self):
        try:

            # SQL 쿼리를 사용하여 테이블에서 데이터 읽기
            query = "SELECT * FROM birthday ORDER BY 생일"
            df = pd.read_sql_query(query, self.conn)

            return df

        except Exception as e:
            print(f"Error: {e}")
            return None

    def check_birthday_db(self):
        try:

            # SQL 쿼리를 사용하여 테이블에서 데이터 읽기
            query = "SELECT * FROM 마을원"
            df = pd.read_sql_query(query, self.conn)
            return df

        except Exception as e:
            print(f"Error: {e}")
            return None

    def count_birthday_db(self):
        try:

            # SQL 쿼리를 사용하여 테이블에서 데이터 읽기
            query = "SELECT COUNT(*) as COUNT FROM birthday"
            res = pd.read_sql_query(query, self.conn)
            res = res.at[0, 'COUNT']

            return res

        except Exception as e:
            print(f"Error: {e}")
            return None

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
            self.cursor.execute("SELECT A.참석여부, C.모임_구분, C.날짜 "
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

    def truncate(self, table):
        # 마을원 테이블 조회
        self.cursor.execute(f"DELETE FROM {table};")

    def __del__(self):
        # 변경 사항 저장 및 연결 종료
        self.conn.commit()
        self.conn.close()

u = Util()
u.init()
u.마을원저장("C:/Users/85350/Desktop/마을원명단.xlsx")
u.출석파일저장(["C:/Users/85350/Documents/카카오톡 받은 파일/6월 박찬호사랑 (1).xlsx","C:/Users/85350/Documents/카카오톡 받은 파일/1월 박찬호사랑.xlsx"
           ,"C:/Users/85350/Documents/카카오톡 받은 파일/5월 박찬호사랑.xlsx","C:/Users/85350/Documents/카카오톡 받은 파일/4월 박찬호사랑.xlsx"
           ,"C:/Users/85350/Documents/카카오톡 받은 파일/2월 박찬호사랑.xlsx","C:/Users/85350/Documents/카카오톡 받은 파일/3월 박찬호사랑.xlsx"
           ,"C:/Users/85350/Documents/카카오톡 받은 파일/12월 박찬호사랑.xlsx","C:/Users/85350/Documents/카카오톡 받은 파일/11월 박찬호사랑.xlsx"
           ,"C:/Users/85350/Documents/카카오톡 받은 파일/10월 박찬호사랑.xlsx"])

u.select_all("마을원")
u.select_all("참석")
u.select_all("모임")