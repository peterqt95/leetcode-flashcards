import os
import cx_Oracle

host = "localhost"
port = "1521"
SID = "orcl"
user = "system"
password = "Kittyboy1"
sid = cx_Oracle.makedsn(host, port, SID)

class Config(object):
    SQLALCHEMY_DATABASE_URI = "oracle://{user}:{password}@{sid}".format(
        user = user,
        password = password,
        sid = sid
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False