# diyun

目录

common
    |----config.py 保存全局配置(在解析用户输入的参数时会设置里面的一些变量)
    |----log.py   日志文件和命令行输出运行状态的接口（程序运行过程中的产生的 info warnning 和 error等信息 统一用log.py 里面的函数进程输出 ）
    |----Parse.py ParseIP.py ParsePort.py  解析用户的运行参数 具体每个函数的作用有注释
Plugins
    |----scanner.py 里面的Scan()是扫描功能的入口，根据用户的运行参数（从上面的config模块里面获取）调用相应的扫描模块（具体扫描模块的实现就是这个文件夹下的其他文件）
    |----fcgiscan.py  文件名就是功能（字面意思，哈哈）
    |----findnet.py
    |----ftpscan.py
    |----memcached.py 
    |----.......
main.py 