import os


from pymysql.cursors import DictCursor

from common import yaml_handler, get_logger
from common.excel_handler import ExcelHandler
from common.mysql_handler import MysqlHandler
from common.get_response import Response
from configs import config
from jsonpath import jsonpath


class MysqlHandlerMid(MysqlHandler):
    def __init__(self):
        super().__init__(
                        host=Handler.yaml_data['db']['host'],
                        port=Handler.yaml_data['db']['port'],
                        user=Handler.yaml_data['db']['user'],
                        password=Handler.yaml_data['db']['password'],
                        charset=Handler.yaml_data['db']['charset'],
                        cursorclass=DictCursor
        )


# yaml_file = os.path.join(config.CONFIG_PATH, 'config.yml')
# yaml_data = yaml_handler.read_yaml(yaml_file)




# def get_random_phone():
#
#     while True:
#         import random
#         phone = '1' + random.choice(['3', '8'])
#         for i in range(0, 9):
#             phone += str(random.randint(0, 9))
#         db = MysqlHandlerMid()
#         sql = "SELECT * FROM futureloan.member WHERE mobile_phone={};".format(phone)
#         sql_res = db.query(sql)
#         if not sql_res:
#             db.close()
#             return phone
#         db.close()


class Handler(object):

    # 加载配置文件
    config = config

    # 加载yml配置
    __yaml_file = os.path.join(config.CONFIG_PATH, 'config.yml')
    yaml_data = yaml_handler.read_yaml(__yaml_file)

    # 初始化日志管理器
    __log_file = os.path.join(config.LOG_PATH, yaml_data["log"]["filename"])
    logger = get_logger.get_logger(
                                   logger_name=yaml_data["log"]["logger_name"][1],
                                   level=yaml_data["log"]["level"],
                                   filemode=yaml_data["log"]["filemode"],
                                   filename=__log_file
    )

    # 初始化excel数据
    __excel_file = os.path.join(config.DATA_PATH, yaml_data["excel"]["filename"])
    excel = ExcelHandler(__excel_file)

    # 加载数据库类，方便管理。不要实例化数据库--->因为有很多不同的对象去访问数据库。
    db_class = MysqlHandlerMid

    # 加载响应类
    res_class = Response

    # 获取随机手机号
    # mobile_phone = get_random_phone()

    # 登陆获取member_id和token
    # @property
    # def member_id(self):
    #     return login()[0]
    # @property
    # def token(self):
    #     return login()[1]
    # @property
    # def member_id(self):
    #     return self.login(self.yaml_data["user"])[0]
    member_id = None
    token = None
    # @property
    # def token(self):
    #     return self.login(self.yaml_data["user"])[1]

    # 管理员登陆
    admin_token = None
    # def admin_token(self):
    #     return self.login(self.yaml_data["admin_user"])[1]

    def login(self, user):
        headers = {"X-Lemonban-Media-Type": "lemonban.v2", "Content-Type": "application/json"}
        res = Response(self.yaml_data["url"] + "/member/login", 'post').get_response(headers=headers, json=user)
        member_id = jsonpath(res, "$..id")[0]
        token_type = jsonpath(res, "$..token_type")[0]
        token = token_type + ' ' + jsonpath(res, "$..token")[0]
        return member_id, token

    loan_id = None

    def get_loan_id(self):
        headers = {"X-Lemonban-Media-Type": "lemonban.v2",
                   "Content-Type": "application/json",
                   "Authorization": self.token
                   }
        data = {"member_id": self.member_id,
                "title": "xx借钱买手机",
                "amount": 1000.00,
                "loan_rate": 10.11,
                "loan_term": 2,
                "loan_date_type": 1,
                "bidding_days": 1
                }
        res = Response(self.yaml_data["url"] + "/loan/add", 'post').get_response(headers=headers, json=data)
        loan_id = jsonpath(res, "$..id")[0]
        return loan_id

    def data_replace(self, string):
        import re
        pattern = r"#(.*?)#"
        while re.search(pattern, string):
            key = re.search(pattern, string).group(1)
            value = getattr(self, key, '')
            string = re.sub(pattern, str(value), string, count=1)
        return string


if __name__ == '__main__':
    # db = Handler.db_class().query("select * from futureloan.member where mobile_phone=18200000000;")
    # print(db)
    # token1 = Handler.admin_token
    # print(token1)
    # my_string = '{"loan_id":"#member_id#","approved_or_not":true}'
    print(Handler().member_id)

