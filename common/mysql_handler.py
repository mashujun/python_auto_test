import pymysql
from pymysql.cursors import DictCursor


class MysqlHandler(object):

    def __init__(self,
                 host=None,
                 port=0,
                 user=None,
                 password=None,
                 charset='utf8',
                 cursorclass=DictCursor
                 ):
        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset=charset,
            cursorclass=cursorclass
        )
        self.cursor = self.conn.cursor()

    def query(self, sql, one=True):
        self.cursor.execute(sql)
        if one:
            data = self.cursor.fetchone()
        else:
            data = self.cursor.fetchall()
        return data

    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    db = MysqlHandler(
        host="120.78.128.25",
        port=3306,
        user="future",
        password="123456"
    )
    res = db.query("select * from futureloan.member where mobile_phone='18200000011';")
    print(res)