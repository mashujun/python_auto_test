from ddt import ddt, data
import unittest

from common.get_response import Response
from middleware.handler import Handler
import json


yaml = Handler.yaml_data
logger = Handler.logger
url_header = yaml["url"]

logger.info('正在准备add测试数据>>>')
my_data = Handler.excel.data_trans('add')
logger.info('测试数据准备完毕。')

even_data = Handler()


@ddt
class TestAdd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setattr(even_data, "member_id", even_data.login(even_data.yaml_data["user"])[0])
        setattr(even_data, "token", even_data.login(even_data.yaml_data["user"])[1])

    # @classmethod
    # def tearDownClass(cls):
    #     pass

    # def setUp(self):
    #     self.db = Handler.db_class()
    #
    # def tearDown(self):
    #     self.db.close()

    @data(*my_data)
    def test_add(self, data_item):
        logger.info('正在执行{}用例第{}条>>>'.format(data_item["interface"], data_item["case_id"]))
        data_item['headers'] = even_data.data_replace(data_item['headers'])
        data_item['data'] = even_data.data_replace(data_item['data'])

        sql = "SELECT * FROM futureloan.loan WHERE member_id={};".format(even_data.member_id)

        # 访问接口前获取loan的记录条数
        db = Handler.db_class()
        before_loan_num = len(db.query(sql, one=False))
        db.close()
        # print(type(before_amount),before_amount)

        # print(type(amount),amount)
        exp_res = json.loads(data_item['expected_result'])
        act_res = Response(url_header+data_item["url"], data_item["method"]).get_response(
            headers=json.loads(data_item["headers"]),
            json=json.loads(data_item["data"])
        )
        # print(act_res)
        try:
            for k, v in exp_res.items():
                self.assertTrue(act_res[k] == v)
            if act_res['code'] == 0:
                logger.info('项目添加成功！')
                # 访问接口后获取loan的记录条数
                db = Handler.db_class()
                after_loan_num = len(db.query(sql, one=False))
                db.close()
                # print(type(leave_amount),leave_amount)
                # 校验数据库的数据与期望一致
                self.assertTrue(after_loan_num == before_loan_num + 1)
                logger.info('数据库新增一条记录')
            logger.info('用例{}通过。'.format(data_item["case_id"]))
            # 测试结果回写到excel
            Handler.excel.data_write('add', data_item["case_id"] + 1, 9, "pass")
        except AssertionError as e:
            logger.error('用例{}不通过！！'.format(data_item["case_id"]))
            # print(act_res, exp_res)
            Handler.excel.data_write('add', data_item["case_id"] + 1, 9, "fail")
            raise e
