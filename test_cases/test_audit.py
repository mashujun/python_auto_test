from ddt import ddt, data
import unittest

from common.get_response import Response
from middleware.handler import Handler
import json


yaml = Handler.yaml_data
logger = Handler.logger
url_header = yaml["url"]

logger.info('正在准备add测试数据>>>')
my_data = Handler.excel.data_trans('audit')
logger.info('测试数据准备完毕。')

env_data = Handler()


@ddt
class TestAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setattr(env_data, "member_id", env_data.login(env_data.yaml_data["user"])[0])
        setattr(env_data, "token", env_data.login(env_data.yaml_data["user"])[1])
        setattr(env_data, "admin_token", env_data.login(env_data.yaml_data["admin_user"])[1])
    #     cls.loan_id = Handler.loan_id
    #     cls.admin_token = Handler.admin_token

    # @classmethod
    # def tearDownClass(cls):
    #     pass
    def setUp(self):
        setattr(env_data, "loan_id", env_data.get_loan_id())
        self.db = Handler.db_class()

    def tearDown(self):
        self.db.close()

    @data(*my_data)
    def test_audit(self, data_item):
        logger.info('正在执行{}用例第{}条>>>'.format(data_item["interface"], data_item["case_id"]))

        data_item['headers'] = env_data.data_replace(data_item['headers'])

        if "#pass_loan_id#" in data_item['data']:
            loan_id = self.db.query("SELECT id FROM futureloan.loan WHERE status != 1")["id"]
            data_item['data'] = data_item['data'].replace('#pass_loan_id#', str(loan_id))
        else:
            data_item['data'] = env_data.data_replace(data_item['data'])

        # db = Handler.db_class()
        # sql = "SELECT status FROM futureloan.loan WHERE id={};".format(json.loads(data_item['data'])["loan_id"])

        # 访问接口前查询新建项目的status
        # if db.query(sql):
        #     before_status = db.query(sql)["status"]
        # print(before_status)
        # db.close()
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
                logger.info('项目审核完毕！')
                # 访问接口后获取loan的status
                # db = Handler.db_class()
                sql = "SELECT status FROM futureloan.loan WHERE id={};".format(
                                       json.loads(data_item['data'])["loan_id"])
                # 查询审核是否通过
                after_loan_id = self.db.query(sql)["status"]
                # db.close()
                # print(type(leave_amount),leave_amount)
                # 校验数据库的status与期望一致
                # self.assertTrue(data_item["status"] = after_loan_id)
                if json.loads(data_item["data"])["approved_or_not"]:
                    self.assertTrue(after_loan_id == 2)
                    logger.info('审核通过')
                else:
                    self.assertTrue(after_loan_id == 5)
                    logger.info('审核不通过')
            logger.info('用例{}通过。'.format(data_item["case_id"]))
            # 测试结果回写到excel
            Handler.excel.data_write('audit', data_item["case_id"] + 1, 9, "pass")
        except AssertionError as e:
            logger.error('用例{}不通过！！'.format(data_item["case_id"]))
            print(act_res, exp_res)
            Handler.excel.data_write('audit', data_item["case_id"] + 1, 9, "fail")
            raise e
