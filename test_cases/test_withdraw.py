from jsonpath import jsonpath
from ddt import ddt, data
import unittest

from middleware.handler import Handler
import json
from decimal import Decimal


yaml = Handler.yaml_data
logger = Handler.logger
url_header = yaml["url"]

logger.info('正在准备recharge测试数据>>>')
my_data = Handler.excel.data_trans('withdraw')
logger.info('测试数据准备完毕。')
# 初始化Handler
even_data = Handler()


@ddt
class TestWithdraw(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # cls.member_id = Handler().member_id
        setattr(even_data, "member_id", even_data.login(even_data.yaml_data["user"])[0])
        # cls.token = Handler().token
        setattr(even_data, "token", even_data.login(even_data.yaml_data["user"])[1])

    # @classmethod
    # def tearDownClass(cls):
    #     pass

    # def setUp(self):
    #     setattr(even_data, "member_id", even_data.member_id)
    #     setattr(even_data, "token", even_data.token)
    #     self.db = Handler.db_class()
    #
    # def tearDown(self):
    #     self.db.close()

    @data(*my_data)
    def test_withdraw(self, data_item):
        logger.info('正在执行{}用例第{}条>>>'.format(data_item["interface"], data_item["case_id"]))

        data_item["headers"] = even_data.data_replace(data_item["headers"])

        data_item["data"] = even_data.data_replace(data_item["data"])
        db = Handler.db_class()

        # 如果测试余额不足的用例，就先将余额更新为250000.01
        if '余额不足' in data_item["title"]:
            sql_1 = "UPDATE futureloan.member SET leave_amount=250000.01 WHERE id={};".format(even_data.member_id)
            sql_2 = "COMMIT;"
            db.query(sql_1)
            db.query(sql_2)
        # 如果不是余额不足的用例，就先将余额更新为500000.01
        if 'OK' in data_item["expected_result"]:
            sql_1 = "UPDATE futureloan.member SET leave_amount=500000.01 WHERE id={};".format(even_data.member_id)
            sql_2 = "COMMIT;"
            db.query(sql_1)
            db.query(sql_2)
        sql_3 = "select leave_amount from futureloan.member where id={};".format(even_data.member_id)
        # 访问接口前获取提现前的余额
        before_amount = db.query(sql_3)["leave_amount"]
        db.close()
        # print(type(before_amount),before_amount)

        # print(type(amount),amount)
        exp_res = json.loads(data_item['expected_result'])
        act_res = Handler.res_class(url_header+data_item["url"], data_item["method"]).get_response(
            headers=json.loads(data_item["headers"]),
            json=json.loads(data_item["data"])
        )
        # print(act_res)
        try:
            for k, v in exp_res.items():
                self.assertTrue(act_res[k] == v)
            if act_res['code'] == 0:
                logger.info('提现成功！')
                amount = json.loads(data_item['data'])["amount"]
                # 校验响应中的数据和期望数据一致
                self.assertTrue(
                    Decimal(str(jsonpath(act_res, "$..leave_amount")[0])) == before_amount - Decimal(str(amount))
                )
                logger.info('响应数据中余额与期望金额一致。')
                db = Handler.db_class()
                leave_amount = db.query(sql_3)["leave_amount"]
                db.close()
                # print(type(leave_amount),leave_amount)
                # 校验数据库的数据与期望一致
                self.assertTrue(leave_amount == before_amount - Decimal(str(amount)))
                logger.info('数据库会员{}余额与期望金额一致'.format(even_data.member_id))
            logger.info('用例{}通过。'.format(data_item["case_id"]))
            # 测试结果回写到excel
            Handler.excel.data_write('withdraw', data_item["case_id"] + 1, 9, "pass")
        except AssertionError as e:
            print(act_res,exp_res)
            logger.error('用例{}不通过！！'.format(data_item["case_id"]))
            Handler.excel.data_write('withdraw', data_item["case_id"] + 1, 9, "fail")
            raise e
