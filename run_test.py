"""运行测试用例，生成测试报告"""
from common import test_suite
from libs.HTMLTestRunner import HTMLTestRunner
from middleware.handler import Handler
import os
from datetime import datetime

ts = datetime.now().strftime('-%y%m%d-%H%M%S')
filename = 'test_report{}.html'.format(ts)
reports_file = os.path.join(Handler.config.REPORTS_PATH, filename)
with open(reports_file, mode='wb') as file:
    runner = HTMLTestRunner(file,
                            title='第一个测试报告',
                            description='测试登陆功能')
    runner.run(test_suite.get_test_suite(Handler.config.CASES_PATH))
