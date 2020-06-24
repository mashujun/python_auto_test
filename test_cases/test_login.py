import unittest
from common.get_response import Response
from ddt import ddt, data
import json
from middleware.handler import Handler

yaml = Handler.yaml_data
logger = Handler.logger
url_header = yaml["url"]

logger.info('正在准备login测试数据>>>')
my_data = Handler.excel.data_trans('login')
logger.info('测试数据准备完毕。')


@ddt
class TestLogin(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     my_logger.info('准备执行所有接口测试用例--->')
    #
    # @classmethod
    # def tearDownClass(cls):
    #     my_logger.info('所有接口用例执行完毕。。。')
    #
    # def setUp(self):
    #     logger.info('连接数据库>>>')
    #     self.db = Handler.db_class()
    #
    # def tearDown(self):
    #     logger.info('关闭数据库。')
    #     self.db.close()

    @data(*my_data)
    def test_register(self, data_item):
        logger.info('正在执行{}用例第{}条>>>'.format(data_item["interface"], data_item["case_id"]))
        exp_res = json.loads(data_item['expected_result'])
        act_res = Response(url_header+data_item["url"], data_item["method"]).get_response(
            headers=json.loads(data_item["headers"]),
            json=json.loads(data_item["data"])
        )
        try:
            for k, v in exp_res.items():
                self.assertTrue(act_res[k] == v)
            logger.info('用例{}通过。'.format(data_item["case_id"]))
            # 将测试结果回写到excel
            Handler.excel.data_write('login', data_item["case_id"]+1, 9, "pass")
        except AssertionError as e:
            logger.error('用例{}不通过！！'.format(data_item["case_id"]))
            Handler.excel.data_write('login', data_item["case_id"]+1, 9, "fail")
            raise e
