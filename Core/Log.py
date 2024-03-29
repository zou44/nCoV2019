import sys
#logging为python内置的库,不需要安装,可以直接使用
import  logging

#默认的配置DEBUG
LOG_LEVEL = logging.INFO #默认等级
LOG_FMT= '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s'
#默认的时间格式
LOG_DATEFMT='%Y-%m-%d %H:%M:%S'
#默认日志文件名称
LOG_FILENAME='./logs.txt'

class Logger(object):
    def __init__(self):
        #1. 获取一个logger对象
        self._logger = logging.getLogger()
        #2. 设置format对象
        self.formatter = logging.Formatter(fmt=LOG_FMT, datefmt=LOG_DATEFMT)
        #3. 设置日志输出
        #  3.1 设置文件日志模式
        self._logger.addHandler(self._get_file_handler(LOG_FILENAME))
        # 3.2 设置终端日志模式
        self._logger.addHandler(self._get_console_handler())
        #4. 设置日志等级
        self._logger.setLevel(LOG_LEVEL)

    def _get_file_handler(self, filename):
        '''返回一个文件日志handler'''
        #1. 获取一个文件日志handler
        filehandler = logging.FileHandler(filename=filename, encoding="utf8")
        #2. 设置日志格式
        filehandler.setFormatter(self.formatter)
        #3. 返回
        return filehandler

    def _get_console_handler(self):
        '''返回一个输出到终端日志handler'''
        #1. 获取一个输出到终端日志handler
        console_handler = logging.StreamHandler(sys.stdout)
        #2. 设置日志格式
        console_handler.setFormatter(self.formatter)
        #3. 返回handler
        return console_handler

    @property
    def logger(self):
        return self._logger

#初始化并配一个logger对象，达到单例的
#使用时,直接导入logger就可以使用
# logger = Logger().logger
