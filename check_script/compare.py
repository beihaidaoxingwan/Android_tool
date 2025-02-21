#自定义函数
import judge
import adbinfo

#信息比较函数
def compare(requirements):
    #判断安卓版本
    version_requirement = requirements.loc["Android_version", "requirements"]
    version_actual = adbinfo.get_sys_version()
    requirements.loc["Android_version", "actual"] = version_actual
    requirements.loc["Android_version", "satisfy"] = judge.judge_exact(version_requirement, version_actual)

    #判断kernel版本
    kernel_requirement = requirements.loc["Kernel_version", "requirements"]
    kernel_actual = adbinfo.get_kernel_version()
    requirements.loc["Kernel_version", "actual"] = str(kernel_actual)
    requirements.loc["Kernel_version", "satisfy"] = judge.judge_exact(kernel_requirement, kernel_actual)

    #判断是否是user版本
    user_requirement = requirements.loc["User_version", "requirements"]
    user_actual = adbinfo.get_user_version()
    requirements.loc["User_version", "actual"] = user_actual
    requirements.loc["User_version", "satisfy"] = judge.judge_exact(user_requirement, user_actual)

    #判断内存条件
    meminfo = adbinfo.get_sys_meminfo()
    mem_requirement = requirements.loc["Memory", "requirements"]
    mem_actual = meminfo.get("MemTotal") / 1024 / 1024  # 单位MB
    requirements.loc["Memory", "actual"] = mem_actual
    requirements.loc["Memory", "satisfy"] = judge.judge_rough(mem_requirement, mem_actual)

    #判断CPU核心数
    kernel_c_requirement = requirements.loc["CPU_kernel_count", "requirements"]
    kernel_c_actual = adbinfo.get_cpu_kernel_count()
    requirements.loc["CPU_kernel_count", "actual"] = kernel_c_actual
    requirements.loc["CPU_kernel_count", "satisfy"] = judge.judge_exact(kernel_c_requirement, kernel_c_actual)

    #判断CPU负载
    cpuload_requirements = requirements.loc[["CPU_load_1min", "CPU_load_5min", "CPU_load_15min"], "requirements"]
    cpuload_actual = adbinfo.get_cpu_load()
    for key, value in cpuload_actual.items():
        requirements.loc[key, "actual"] = value
        requirements.loc[key, "satisfy"] = judge.judge_size(cpuload_requirements[key], value)

    #判断温度
    temp_actual = adbinfo.get_board_temp()
    requirements.loc["Temperature", "actual"] = temp_actual
    requirements.loc["Temperature", "satisfy"] = judge.judge_size(requirements.loc["Temperature", "requirements"], temp_actual)

    return requirements