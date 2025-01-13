import copy
import random
from collections import defaultdict, deque
import src.util as util

def assign_members(members, teams):

    constraints = util.Util().배치관계조회()[1:]

    # Step 1: 데이터 구조 초기화
    member_dict = defaultdict(list)  # 멤버를 등급별로 그룹화
    team_dict = {team[1]: [] for team in teams}  # 팀에 배정된 멤버를 저장
    grade_dict = {team[1]: team[0] for team in teams}  # 각 팀이 받을 수 있는 등급 정보 저장

    # 멤버를 등급별로 그룹화
    for uid, name, birth_year, grade, gender in members:
        member_dict[grade].append((uid, name, birth_year, grade, gender))

    # UID로 멤버 튜플을 찾기 위한 딕셔너리
    member_lookup = {uid: (uid, name, birth_year, grade, gender) for uid, name, birth_year, grade, gender in members}

    # 팀의 리더를 UID로 멤버 튜플을 찾기 위한 딕셔너리
    leader_lookup = {leader[0]: leader for _, leader in teams}

    # Step 2: 팀장 먼저 배정
    for idx, team in enumerate(teams):
        _, leader = team  # 팀장 정보 추출
        leader_uid = leader[0]  # 팀장의 UID 추출
        leader_tuple = leader_lookup[leader_uid]  # 팀장의 멤버 튜플 추출
        team_dict[leader].append(leader_tuple)  # 팀장 배정

    best_assignment = None
    min_violations = float('inf')  # 제약 사항 위반의 최소값 (초기값은 무한대로 설정)
    iteration_count = 0

    while iteration_count < 10000:
        print(f"\n# 배정 시도 {iteration_count + 1}")

        # 팀 배정 시도
        current_member_dict = copy.deepcopy(member_dict)
        current_team_dict = {team: list(members) for team, members in team_dict.items()}
        assign_members_to_teams(current_member_dict, grade_dict, current_team_dict, constraints)

        # 제약 사항 위반 개수 확인
        violations = check_constraints(current_team_dict, constraints)

        # 제약 사항 위반 건수가 0건이면 바로 리턴
        if violations == 0:
            print(f"🎉 제약 사항 위반 0건으로 배정 완료!")
            return current_team_dict

        # 최소 제약 사항 위반 건수 기록
        if violations < min_violations:
            min_violations = violations
            best_assignment = current_team_dict

        iteration_count += 1

    # 1000번 반복 후 최소 제약 사항 위반 결과 리턴
    print(f"\n💥 10,000번 배정 후 최소 제약 사항 위반 결과 반환")
    return best_assignment


def assign_members_to_teams(member_dict, grade_dict, team_dict, constraints):
    # Step 3: 등급별로 멤버를 팀에 배정
    for grade, members_list in sorted(member_dict.items()):  # 1. grade 오름차순 순회
        valid_teams = [team for team, grades in grade_dict.items() if grades.get(grade, False)]

        # 배정 가능한 팀이 없는 경우 스킵
        if not valid_teams:
            #print(f"\n⚠️ [Grade {grade}] 배정 가능한 팀 없음! (스킵)")
            continue

        team_names = [team[1] for team in valid_teams]  # valid_teams의 2번째 원소(팀 이름) 리스트 추출
        random.shuffle(members_list)  # 팀원 랜덤 섞기

        # 2. 현재 valid_teams의 팀원 수 가져오기
        team_sizes = {team: len(team_dict[team]) for team in valid_teams}

        #print(f"\n🟢 [Grade {grade}] 배정 시작")
        #print(f"🔹 배정 가능 팀: {valid_teams} (팀 이름: {team_names})")
        #print(f"🔹 초기 팀원 수: {team_sizes}")
        #print(f"🔹 배정할 인원: {members_list}")

        # 3. 팀원 수 균등화: 팀원 수가 다를 때만 수행
        while len(set(team_sizes.values())) > 1 and members_list:
            min_team = min(team_sizes, key=team_sizes.get)  # 현재 가장 적은 팀원 수의 팀 찾기
            member = members_list.pop(0)  # 리스트에서 첫 번째 멤버 가져오기
            team_dict[min_team].append(member)
            team_sizes[min_team] += 1
            #print(f"✅ {member} → {min_team} ({min_team[1]}) (균등화 우선 배정)")

        random.shuffle(valid_teams)
        # 4. 남은 멤버 배정 (순차적으로 모든 멤버 배정)
        while members_list:
            for team in valid_teams:
                if not members_list:
                    break
                member = members_list.pop(0)
                team_dict[team].append(member)
                #print(f"✅ {member} → {team} ({team[1]}) (순차 배정)")

        #print(f"🔹 최종 팀원 수: { {team: len(team_dict[team]) for team in valid_teams} }")

    return team_dict


def check_constraints(team_dict, constraints):
    violation_count = 0

    for uid1, uid2, rule in constraints:
        team1 = team2 = None

        # 각 uid가 어느 팀에 속했는지 찾기
        for team, members in team_dict.items():
            member_uids = {m[0] for m in members}  # 팀원 uid 추출
            if uid1 in member_uids:
                team1 = team
            if uid2 in member_uids:
                team2 = team

        # 규칙 위반 확인
        if rule == "분리" and team1 == team2:
            #print(f"❌ [위반] {uid1} & {uid2} → 같은 팀에 배정됨! (분리 규칙 위반)")
            violation_count += 1
        elif rule == "동반" and team1 != team2:
            #print(f"❌ [위반] {uid1} & {uid2} → 서로 다른 팀에 배정됨! (동반 규칙 위반)")
            violation_count += 1

    print(f"\n🔴 총 {violation_count}개의 제약 사항 위반이 발생했습니다.")
    return violation_count