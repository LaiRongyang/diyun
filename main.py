from common import Parse
from common import config
from Plugins import scanner
if __name__ == '__main__':
    Info = config.HostInfo()
    # 解析命令和初始化配置文件
    Parse.argParse(Info)
    Parse.parse(Info)
    scanner.Scan(Info)




