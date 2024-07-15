from datetime import datetime, timedelta


def get_next_sunday(date_string):
    date = datetime.strptime(date_string, '%Y-%m-%d')

    # 입력된 날짜가 일요일인 경우
    if date.weekday() == 6:
        return date.strftime('%Y-%m-%d')

    # 다가오는 가장 가까운 일요일 날짜 구하기
    days_to_sunday = 6 - date.weekday()
    next_sunday = date + timedelta(days=days_to_sunday)

    return next_sunday.strftime('%Y-%m-%d')


def get_week_of_month(date_string):
    date_time_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    date_only_str = date_time_obj.strftime('%Y-%m-%d')

    date_string = get_next_sunday(date_only_str)
    date = datetime.strptime(date_string, '%Y-%m-%d')

    # 해당 날짜가 속한 연도와 월
    year = date.year
    month = date.month

    # 해당 월의 첫 번째 날 구하기
    first_day_of_month = datetime(year, month, 1)

    # 해당 월의 첫 번째 일요일 구하기
    if first_day_of_month.weekday() == 6:  # 첫째날이 일요일인 경우
        first_sunday = first_day_of_month
    else:
        days_to_sunday = 6 - first_day_of_month.weekday()
        first_sunday = first_day_of_month + timedelta(days=days_to_sunday)

    # 해당 날짜와 첫 번째 일요일 사이의 일수 차이 계산
    delta_days = (date - first_sunday).days

    # 몇 주차인지 계산
    if delta_days < 0:
        # 입력된 날짜가 해당 월의 첫 번째 일요일 이전인 경우 이전 달의 마지막 주로 처리
        if month == 1:
            prev_month = 12
            prev_year = year - 1
        else:
            prev_month = month - 1
            prev_year = year

        last_day_of_prev_month = datetime(prev_year, prev_month, 1) + timedelta(days=-1)
        delta_days_prev = (date - last_day_of_prev_month).days
        week_number = delta_days_prev // 7 + 1
    else:
        week_number = (delta_days // 7) + 1

    return f"{year}년 {month}월 {week_number}주차"


def convert_date_format(date_str):
    # 입력 받은 날짜 문자열을 '-'로 분리
    year, month, day = date_str.split('-')

    # 새로운 형식으로 변환
    formatted_date = f"{year}년 {int(month)}월 {int(day)}일"

    return formatted_date