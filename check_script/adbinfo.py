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

#获取lmk参数
def get_lmk_params():
    cmd = "adb shell \"getprop | grep sys.lmk.minfree_levels\""
    result = adb_shell(cmd)
    if result[0] == 0:
        lmk = result[1].split("]:")[1].split(",")
        #去除首尾中括号，此处写的不严谨，随着机型改变可能会出现改变，但是核心思想不变
        lmk[0] = lmk[0].strip(' [')
        lmk[-1] = lmk[-1].strip(']')
        lmk_params = {}
        for param in lmk:
                key, value = param.split(":")
                lmk_params[eval(key.strip()) / 1024 / 10] = eval(value.strip())
        return lmk_params

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
    result = adb_shell(cmd)
    if result[0] == 0:
        result = result[1].split("load average:")[1].split(",")
        loads = {}
        kernel_c = get_cpu_kernel_count()
        for i in range (0, len(result)):
            result[i] = float(result[i].strip())
            loads[labels[i]] = result[i] / kernel_c
        return loads

#获取主板温度
def get_board_temp():
    cmd = "adb shell \"i=0; while [[ $i -lt 70 ]]; do (type=`cat /sys/class/thermal/thermal_zone$i/type`; temp=`cat /sys/class/thermal/thermal_zone$i/temp`; echo \"$i $type : $temp\"); i=$((i+1)); done | grep msm\""
    result = adb_shell(cmd)
    if result[0] == 0:
        result = result[1].split(":")
        tmp = float(result[1].strip()) / 1000
        return tmp

#获取wirte_back参数
def get_write_back_params():
    cmd_dirty_ratio = "adb shell \"cat /proc/sys/vm/dirty_ratio\"" # 表示内存中可以有多少百分比的数据是“脏”数据（即尚未写入磁盘的数据）。
    cmd_dirty_background_ratio = "adb shell \"cat /proc/sys/vm/dirty_background_ratio\"" # 绝对的脏数据限制，内存里的脏数据百分比不能超过这个值。
    dirty_ratio = adb_shell(cmd_dirty_ratio)
    dirty_background_ratio = adb_shell(cmd_dirty_background_ratio)
    if dirty_ratio[0] == 0 and dirty_background_ratio[0] == 0:
        dirty_ratio = int(dirty_ratio[1].strip())
        dirty_background_ratio = int(dirty_background_ratio[1].strip())
        return dirty_ratio, dirty_background_ratio

#获取readahead参数
def get_readahead_params(device):
    cmd = f"adb shell \"blockdev --getra /dev/block/{device}\""
    result = adb_shell(cmd)
    if result[0] == 0:
        readahead = int(result[1].strip())
        return readahead

#获取IO调度器参数
def get_io_scheduler_params(device):
    cmd = f"adb shell \"cat /sys/block/{device}/queue/scheduler\""
    result = adb_shell(cmd)
    if result[0] == 0:
        schedulers = result[1].strip().split(' ')
        for scheduler in schedulers:
            if scheduler.startswith('[') and scheduler.endswith(']'):
                return scheduler[1:-1]