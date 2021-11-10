from common import Parse
from common import config
from Plugins import scanner
if __name__ == '__main__':
    Info = config.HostInfo()
    Parse.argParse(Info)  # 解析命令
    Parse.parse(Info)     # 根据解析的命令参数进行一些初始化
    scanner.Scan(Info)    # （根据用户的命令参数）调用具体的模块进行扫描



