import subprocess

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

#获取kernel版本
def get_kernel_version():
    cmd = "adb shell \"uname -r\""
    result = adb_shell(cmd)
    if result[0] == 0:
        kernel_version = result[1].split('-')[0].strip()
        return kernel_version

#获取user版本
def get_user_version():
    cmd = "adb shell getprop ro.build.type"
    result = adb_shell(cmd)
    if result[0] == 0:
        version = result[1].strip()
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

#获取CPU核心数
def get_cpu_kernel_count():
    cmd = "adb shell \"cat /proc/cpuinfo | grep 'processor' | wc -l\""
    result = adb_shell(cmd)
    if result[0] == 0:
        kernel_c = int(result[1].strip())
        return kernel_c

#获取CPU负载
def get_cpu_load():
    cmd = "adb shell uptime"
    labels = ["CPU_load_1min", "CPU_load_5min", "CPU_load_15min"]
    result = adb_shell(cmd)[1].split("load average:")[1].split(",")
    loads = {}
    kernel_c = get_cpu_kernel_count()
    for i in range (0, len(result)):
        result[i] = float(result[i].strip())
        loads[labels[i]] = result[i] / kernel_c
    return loads

#获取主板温度
def get_board_temp():
    cmd = "adb shell \"i=0; while [[ $i -lt 70 ]]; do (type=`cat /sys/class/thermal/thermal_zone$i/type`; temp=`cat /sys/class/thermal/thermal_zone$i/temp`; echo \"$i $type : $temp\"); i=$((i+1)); done | grep msm\""
    result = adb_shell(cmd)[1].split(":")
    tmp = float(result[1].strip()) / 1000
    return tmp
