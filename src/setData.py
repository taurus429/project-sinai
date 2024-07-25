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

# u.select_all("마을원")
# u.select_all("참석")
# u.select_all("모임")
#
