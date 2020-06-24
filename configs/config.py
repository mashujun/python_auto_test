import os

CONFIG_FILE = os.path.abspath(__file__)
# 配置文件路径
CONFIG_PATH = os.path.dirname(CONFIG_FILE)
# 项目路径
BASE_PATH = os.path.dirname(CONFIG_PATH)
# 测试用例类路径
CASES_PATH = os.path.join(BASE_PATH, 'test_cases')
# 测报告路径
REPORTS_PATH = os.path.join(BASE_PATH, 'reports')
# 测试数据excel路径
DATA_PATH = os.path.join(BASE_PATH, 'data')
# 日志路径
LOG_PATH = os.path.join(BASE_PATH, 'logs')
