from math import fabs

#精确比较（需要两值相等）
#在判断Android_version,CPU核心数时被调用
def judge_exact(requirement, actual):
    if requirement == actual:
        ret = 1.0
    else:
        ret = 0.0
    return  ret

#粗略比较（需要两值相差小于1）
#判断内存时候被调用
def judge_rough(requirement, actual):
    if fabs(requirement - actual) <= 1.0:
        ret = 1.0
    else:
        ret = 0.0
    return  ret

#大小比较
#判断CPU负载，温度时被调用
def judge_size(requirement, actual):
    if actual <= requirement:
        ret = 1.0
    else:
        ret = 0.0
    return  ret