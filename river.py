# -*- coding: utf-8 -*-
# 传教士与野人的数量设置
missionary = beast = 3
boat_limit = 2
# temp 作临时存储， open_list保存已经生成但是还没考察的节点，closed记录已经访问的节点
temp = []
open_list = []
closed_list = []


class State(object):
    # 初始化，其中 b 表示船所在位置，1表示左岸 0 表示右岸；f是代价估计；g是实际代价；father表示上一个状态；node表示当前状态数组
    def __init__(self, missionary, beast, b):
        self.missionary = missionary
        self.beast = beast
        self.b = b
        self.g = 0
        self.f = 0
        self.father = None
        self.node = [missionary, beast, b]


# 初始状态：所有人都在左岸
init = State(missionary, beast, 1)
# 终止状态：所有人都在右岸
goal = State(0, 0, 0)

# 判断状态是否合理、安全
def safe(s):
    if s.missionary > missionary or s.missionary < 0 or (s.missionary != 0 and s.missionary < s.beast) or \
            (s.missionary != missionary and missionary - s.missionary < beast - s.beast):
        return False
    return True

# 启发函数 估算当前状态和目标状态的距离，用于路径决策c
def h(s):
    return s.missionary + s.beast - boat_limit * s.b

# 判断两个状态是否相同  依据状态数组判定
def equal(a, b):
    if a.node == b.node:
        return True
    return False

# 判断是否状态回滚
def back(new, s):
    if s.father is None:
        return False
    return equal(new, s.father)

# 排序 依据代价估计排序
def open_sort(l):
    l.sort(key=lambda x: x.f)

# 扩展节点时在open表和closed表中找原来是否存在相同mcb属性的节点
def in_list(new, l):
    for item in l:
        if equal(new, item):
            return True, item
    return False, None

# A*函数
def A_star(s):
    global open_list, closed_list
    open_list = [s]
    closed_list = []
    # 生成的节点仍未检查的
    while open_list:
        current_state = open_list.pop(0)
        closed_list.append(current_state)
        if equal(current_state, goal):
            return current_state
        print('当前状态：%s' % current_state.node)
        # 上船到下一个状态 i表示上船的传教士人数，j表示上船的野人人数
        for i in range(1 + min(current_state.missionary, boat_limit) if current_state.b == 1 else 2):
            for j in range(1 + min(current_state.beast, boat_limit) if current_state.b == 1 else 2):
                # 非法和不安全的情况
                if i + j <= 0 or i + j > boat_limit or (i != 0 and i < j):
                    continue
                print(i, j)
                # 当前船在左岸
                if current_state.b == 1:
                    new_state = State(current_state.missionary - i, current_state.beast - j, 0)
                # 当前船在右岸
                if current_state.b == 0:
                    new_state = State(current_state.missionary + i, current_state.beast + j, 1)
                if safe(new_state) and not back(new_state, current_state):
                    print('新状态：%s' % new_state.node)
                    new_state.father = current_state
                    new_state.g = current_state.g + 1
                    new_state.f = new_state.g + h(current_state)
                    print(new_state.f)
                    # 新状态数组是否在 open_list 中
                    flag = in_list(new_state, open_list)
                    if flag[0]:
                        old_state = flag[1]
                        if new_state.f < old_state.f:
                            open_list.remove(old_state)
                    # 新状态数组是否在 closed_list中
                    flag = in_list(new_state, closed_list)
                    if flag[0]:
                        old_state = flag[1]
                        if new_state.f < old_state.f:
                            closed_list.remove(old_state)
                    open_list.append(new_state)
                    open_sort(open_list)


def printPath(f):
    if f is None:
        return
    printPath(f.father)
    print(f.node)


if __name__ == '__main__':
    final = A_star(init)
    print(final)
    if final:
        print('有解')
        printPath(final)
    else:
        print('无解')
