import psycopg2
import bcrypt


def create_conn():
    """ 连接数据库 """
    database = ''  # 选择数据库名称
    user = ''  # 数据库用户名
    password = ''  # 数据库密码
    host = ''  # 数据库ip
    port = ''  # 端口号
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)  # 连接数据库
    return conn
