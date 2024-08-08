import random
from collections import defaultdict, deque
import util

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

    # 제약사항 처리
    must_together = defaultdict(set)  # '동반'해야 하는 멤버 정보
    must_separate = defaultdict(set)  # '분리'해야 하는 멤버 정보

    for member1_uid, member2_uid, condition in constraints:
        # UID로 멤버 튜플 찾기
        member1 = member_lookup.get(member1_uid, leader_lookup.get(member1_uid))
        member2 = member_lookup.get(member2_uid, leader_lookup.get(member2_uid))

        if member1 and member2:
            if condition == '동반':
                must_together[member1].add(member2)
                must_together[member2].add(member1)
            elif condition == '분리':
                must_separate[member1].add(member2)
                must_separate[member2].add(member1)

    # Step 2: 팀장 먼저 배정
    for idx, team in enumerate(teams):
        _, leader = team  # 팀장 정보 추출
        leader_uid = leader[0]  # 팀장의 UID 추출
        leader_tuple = leader_lookup[leader_uid]  # 팀장의 멤버 튜플 추출
        team_dict[leader].append(leader_tuple)  # 팀장 배정

    # Step 3: 등급별로 멤버를 팀에 배정
    for grade, members_list in member_dict.items():
        # 현재 등급을 받을 수 있는 팀 목록 찾기
        valid_teams = [team for team, grades in grade_dict.items() if grades[grade]]

        # 멤버들을 랜덤하게 섞어 배정 순서를 무작위로 만듦
        random.shuffle(members_list)

        # 동반 배정이 필요한 멤버들을 우선 처리하기 위해 큐 사용
        queue = deque(members_list)

        while queue:
            member = queue.popleft()
            uid = member[0]
            # 멤버를 배정할 수 있는 유효한 팀을 찾았는지 여부
            valid_team_found = False

            # 팀의 현재 배정된 멤버 수를 기준으로 정렬하여 배정
            for team in sorted(valid_teams, key=lambda x: len(team_dict[x])):
                # 제약사항을 만족하는지 확인
                can_assign = True

                # '동반' 제약사항 확인
                if member in must_together:
                    # 동반해야 하는 멤버가 이미 배정된 팀에 있는지 확인
                    for together_member in must_together[member]:
                        if together_member not in team_dict[team]:
                            can_assign = False
                            break

                # '분리' 제약사항 확인
                if member in must_separate:
                    # 분리해야 하는 멤버가 현재 팀에 있는지 확인
                    for separate_member in must_separate[member]:
                        if separate_member in team_dict[team]:
                            can_assign = False
                            break

                # 제약사항을 만족하면 팀에 멤버 배정
                if can_assign:
                    team_dict[team].append(member)
                    valid_team_found = True
                    break

            # 제약사항 때문에 배정할 팀을 찾지 못한 경우
            if not valid_team_found:
                # 우선 가능한 팀에 배정하고 나중에 조정
                for team in sorted(valid_teams, key=lambda x: len(team_dict[x])):
                    team_dict[team].append(member)
                    break

    # 제약사항에 따라 배정 조정
    # '동반' 제약사항에 따라 조정
    for member1 in must_together:
        for member2 in must_together[member1]:
            member1_team = None
            member2_team = None
            # 멤버1과 동반 멤버2의 팀을 찾기
            for team in team_dict:
                if member1 in team_dict[team]:
                    member1_team = team
                if member2 in team_dict[team]:
                    member2_team = team
            # 두 멤버가 서로 다른 팀에 있을 경우
            if member1_team and member2_team and member1_team != member2_team:
                # 동반 멤버가 다른 팀에 있을 경우, 같은 팀으로 조정
                team_dict[member2_team].remove(member2)
                team_dict[member1_team].append(member2)

    # '분리' 제약사항에 따라 조정
    for member1 in must_separate:
        for member2 in must_separate[member1]:
            for team in team_dict:
                if member1 in team_dict[team] and member2 in team_dict[team]:
                    # 같은 팀에 배정되어 있으면 다른 팀으로 이동
                    for new_team in team_dict:
                        if new_team != team and len(team_dict[new_team]) < len(team_dict[team]):
                            team_dict[team].remove(member2)
                            team_dict[new_team].append(member2)
                            break
    print(team_dict)
    return team_dict
