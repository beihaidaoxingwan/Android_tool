import pandas as pd
import subprocess
import time
from math import fabs

#定义读取excel表格
def read_excel(filename):
    requirements = pd.read_excel(filename)
    return requirements

#定义写入excel表格
def write_excel(df):
    filename = time.strftime("%Y-%m-%d_%H-%M-%S.xlsx", time.localtime(time.time()))
    df.to_excel(filename, index=False)

#定义python到adb的接口
def adb_shell(cmd):
    result = subprocess.getstatusoutput(cmd);
    return  result

#获取系统版本
def  get_sys_version():
    cmd = "adb shell \"getprop ro.build.version.release\""
    result = adb_shell(cmd)
    if result[0] == 0:
        version = float(result[1].strip())
        return version

#获取内存配置
def get_sys_meminfo():
    cmd = "adb shell \"cat /proc/meminfo\""
    result = adb_shell(cmd)
    if result[0] == 0:
        lines = result[1].strip().split("\n")
        # 解析并存储为字典
        mem_info = {}
        for line in lines:
            key, value = line.split(':')
            mem_info[key.strip()] = int(value.split()[0])  # 只取数值部分并转换为整数
        return mem_info

def judge_exact(requirement, actual):
    if requirement == actual:
        ret = 1.0
    else:
        ret = 0.0
    return  ret

def judge_rough(requirement, actual):
    if fabs(requirement - actual) <= 1.0:
        ret = 1.0
    else:
        ret = 0.0
    return  ret

def compare(requirement):
    #判断安卓版本
    version_requirement = requirements.get("Android_version")[0]
    version_actual = get_sys_version()
    requirements.loc[requirements["mode"] == "actual", "Android_version"] = version_actual
    requirements.loc[requirements["mode"] == "satisfy", "Android_version"] = judge_exact(version_requirement, version_actual)

    #判断内存条件
    meminfo = get_sys_meminfo()
    mem_requirement = requirements.get("Memory")[0]
    mem_actual = meminfo.get("MemTotal") / 1024 / 1024  # 单位MB
    print(mem_actual)
    requirements.loc[requirements["mode"] == "actual", "Memory"] = mem_actual
    requirements.loc[requirements["mode"] == "satisfy", "Memory"] = judge_rough(mem_requirement, mem_actual)

    return requirement

if __name__ == '__main__':
    requirements = read_excel("requirements.xlsx")
    print(requirements)
    result = compare(requirements)
    print(result)
    write_excel(requirements)