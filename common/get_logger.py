import logging


def get_logger(logger_name='root',
               level='DEBUG',
               filemode=False,
               filename=None,
               formatter='%(asctime)s-->%(name)s-->%(filename)s--line:%(lineno)d-%(levelname)s:%(message)s'
               ):
    """
    参数：
    logger_name：收集器名称
    formatter：日志输出格式
    level：日志等级
    filemode：日志输出方式
    filename：输出文件名称

    :return:返回收集器
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    if not filemode:
        handler = logging.StreamHandler()
    else:
        handler = logging.FileHandler(filename, encoding='utf8')
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(formatter))
    logger.addHandler(handler)

    return logger


if __name__ == '__main__':

    logger01 = get_logger()
    logger01.debug('this is a debug message')
    logger02 = get_logger(logger_name='user',
                          level='INFO',
                          filemode=True,
                          filename='E:\\python_test\\test_demo\\logs\\log.txt'
                          )
    logger02.info('this is a info message')
