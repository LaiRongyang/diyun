import time
from common import config
import logging

Results = []

Silent = False  # 沉默

LogWG = 0  # 同步用的

LogSucTime = 0

WaitTime = 0

End = 0

Num = 0

Start = True

LogErrTime = 0

inited = False

logger=None

class LogFilter(logging.Filter):
    def filter(self, record):
        # record也是logging的一个类LogRecord, 常用的属性有name, level, pathname, lineno, msg, args, exc_info
        if "[+]" in record.msg or "[*]" in record.mag:
            return True
        return False


def genLogger():
    logger = logging.getLogger("")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        # 创建handler
        fh = logging.FileHandler(config.Outputfile, encoding="utf-8")
        ch = logging.StreamHandler()
        nh = logging.NullHandler()

        # 设置输出日志格式
        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s %(message)s",
            datefmt='[%Y-%m-%d %H:%M:%S]',
        )

        # 为handler指定输出格式
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 为logger添加的日志处理器handler
        if config.IsSave:
            logger.addHandler(fh)
        if not Silent:
            logger.addHandler(ch)
        logger.addHandler(nh)

        # 如需过滤，则解除一下注释
        # logger.addFilter(LogFilter())

    return logger



# 初始化
def init():
    global logger
    logger = genLogger()
    return


# 把所有缓存的日志信息打印到控制台和保存到文件
def SaveLog():
    '''
    for result in Results:
        if Silent == False or "[+]" in result or "[*]" in result:
            print(result)
        if config.IsSave:
            WriteFile(result, config.Outputfile)
        LogWG = LogWG - 1
    '''
    return


'''
# 把一条日志信息写到文件
def WriteFile(result, filename):
    
    text = result + "\n"
    f = open(filename)  # 打开方式为 os.O_WRONLY|os.O_CREATE|os.O_APPEND ，文件的权限为0777
    # 如果打开失败则提示错误 并return
    f.write(text)
    f.Close()
    # 如果写入失败 则 输出 Write %s error, %v\n", filename, err
'''


# 增加一条日志信息
def LogSuccess(result):
    global LogWG
    if not logger:
        init()
    LogWG = LogWG + 1
    LogSucTime = time.time()
    logger.info(result)




# 打印错误信息
# errObj 在这里应该是一个错误或者异常对象
def LogError(errObj):
    global LogErrTime
    if WaitTime == 0:
        print("已完成 %d/%d %s" % ( End, Num, errObj.__str__()))
        for arg in errObj.args:
            print(arg)
    elif (time.time() - LogSucTime) > WaitTime and (time.time() - LogErrTime) > WaitTime:
        print("已完成 %d/%d %s" % ( End, Num, errObj.__str__()))
        for arg in errObj.args:
            print(arg)
        LogErrTime = time.time()


# 根据错误信息检查错误是不是已知的通信错误几种类型？
# 这里的err是错误或者异常对象
# 对象的args属性是一个错误信息的元组
def CheckErrs(errObj):  # 这里的err是对象
    if errObj == None:
        return False
    errs = [
        "closed by the remote host", "too many connections",
        "i/o timeout", "EOF", "A connection attempt failed",
        "established connection failed", "connection attempt failed",
        "Unable to read", "is not allowed to connect to this",
        "no pg_hba.conf entry",
        "No connection could be made",
        "invalid packet size",
        "bad connection",
    ]
    for err in errs:
        for arg in errObj.args:
            if err in arg:
                return True
    return False

def logDebug(result):
    logger.debug(result)
def logInfo(result):
    logger.info(result)
def logWarning(result):
    logger.warning(result)
def logError(result):
    logger.error(result)
def logCritical(result):
    logger.critical(result)


if __name__ == "__main__":
    LogSuccess("success")
