import unittest
from common.get_response import Response
from ddt import ddt, data
import json
import random
from middleware.handler import Handler

yaml = Handler.yaml_data
logger = Handler.logger
url_header = yaml["url"]

logger.info('正在准备register测试数据>>>')
my_data = Handler.excel.data_trans('register')
logger.info('测试数据准备完毕。')


@ddt
class TestRegister(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls) -> None:
    #     cls.db = Handler.db_class()
    #     # my_logger.info('准备执行所有接口测试用例--->')
    #
    # @classmethod
    # def tearDownClass(cls) -> None:
    #     cls.db.close()
    #     # my_logger.info('所有接口用例执行完毕。。。')

    def setUp(self):
        logger.info('连接数据库>>>')
        self.db = Handler.db_class()

    def tearDown(self):
        logger.info('关闭数据库。')
        self.db.close()

    @data(*my_data)
    def test_register(self, data_item):
        logger.info('正在执行{}用例第{}条>>>'.format(data_item["interface"], data_item["case_id"]))
        if "#mobile_phone#" in data_item["data"]:
            phone = self.get_random_phone()
            data_item["data"] = data_item["data"].replace("#mobile_phone#", phone)
        #     print(data_item["data"])

        exp_res = json.loads(data_item['expected_result'])
        act_res = Response(url_header+data_item["url"], data_item["method"]).get_response(
            headers=json.loads(data_item["headers"]),
            json=json.loads(data_item["data"])
        )
        # print(act_res, exp_res)
        # self.assertTrue(act_res["code"] == exp_res["code"])
        # self.assertTrue(act_res["msg"] == exp_res["msg"])
        try:
            for k, v in exp_res.items():
                self.assertTrue(act_res[k] == v)
            if act_res['code'] == 0:
                logger.info('手机号{}注册成功！'.format(json.loads(data_item["data"])["mobile_phone"]))
                # logger.info('初始化数据库>>>')
                # db = Handler.db_class()
                # logger.info('数据库初始化完毕！')
                logger.info('正在查询{}的数据库信息>>>'.format(json.loads(data_item["data"])["mobile_phone"]))
                phone = json.loads(data_item["data"])["mobile_phone"]
                sql = "select * from futureloan.member where mobile_phone={};".format(phone)
                mysql_data = self.db.query(sql)
                # db.close()
                # 注册成功的手机号需能在数据库中查询到
                self.assertTrue(mysql_data)
                logger.info('此用户已成功存入数据库！')
            logger.info('用例{}通过。'.format(data_item["case_id"]))
            # 测试结果回写到excel
            Handler.excel.data_write('register', data_item["case_id"] + 1, 9, "pass")
        except AssertionError as e:
            logger.error('用例{}不通过！！'.format(data_item["case_id"]))
            Handler.excel.data_write('register', data_item["case_id"] + 1, 9, "fail")
            raise e

    @staticmethod
    def get_random_phone():
        while True:
            phone = '1' + random.choice(['3', '8'])
            for i in range(0, 9):
                phone += str(random.randint(0, 9))
            db = Handler.db_class()
            sql = "SELECT * FROM futureloan.member WHERE mobile_phone={};".format(phone)
            sql_res = db.query(sql)
            if not sql_res:
                db.close()
                return phone
            db.close()
