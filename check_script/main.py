#自定义函数
import dataload
import compare

if __name__ == '__main__':
    requirements = dataload.read_excel("requirements.xlsx")
    print(requirements)
    result = compare.compare(requirements)
    print(result)
    dataload.write_excel(requirements)