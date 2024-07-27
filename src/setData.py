import util
import os
u = util.Util()
u.init()
u.마을원저장("../data/마을원명단.xlsx")
dirname = "../data/사랑보고서"
filenames = os.listdir(dirname)
file_list = []
for filename in filenames:
    full_filename = os.path.join(dirname, filename)
    file_list.append(full_filename)

u.출석파일저장(file_list)
u.모임저장("../data/참석.xlsx")
마을원 = u.마을원전체조회()[1:]
장결자 = [("고희주",	941105),
("권진혁",	970421),
("김동빈",	940129),
("김성령",	980111),
("김수현",	980729),
("김은수",	980216),
("김정우",	960812),
('김주은',	950314),
('박명수',	951115),
("송영준",	950426),
('제주안',	930320),
('진정재',	960531),
('진희정',	970525)]

for g in 장결자:
    for m in 마을원:
        if g[0] == m[2]:
            u.장결등록(m[0])
            break
졸업자 = [("이은수",	910227),
("성열오",	910529),
("장서영",	910731),
("김민정",	911030)]
for g in 졸업자:
    for m in 마을원:
        if g[0] == m[2]:
            u.졸업등록(m[0])
            break

빠른 = [("방유진",	920217),
("김가림",	960113),
("박주은",	960129)]
for g in 빠른:
    for m in 마을원:
        if g[0] == m[2]:
            u.빠른등록(m[0])
            break

또래장 = [("이은수",	920217),
("황예진",	920928),
("김정욱",	931209),
("황현수",	941024),
("배의환",	950713),
("박찬호",	931209),
("이경호",	931209)]
for g in 또래장:
    for m in 마을원:
        if g[0] == m[2]:
            u.또래장등록(m[0])
            break

u.업데이트_사랑장_리더여부()
# u.select_all("마을원")
# u.select_all("참석")
# u.select_all("모임")
#
