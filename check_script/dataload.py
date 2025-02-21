import pandas as pd
import time

#定义读取excel表格
def read_excel(filename):
    requirements = pd.read_excel(filename, index_col=0)
    return requirements

#定义写入excel表格
def write_excel(df):
    filename = time.strftime("%Y-%m-%d_%H-%M-%S.xlsx", time.localtime(time.time()))
    df.to_excel(filename, index=True)