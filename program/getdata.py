import pandas as pd
import datetime
import time
 
import pymysql
MYSQL_HOST = 'localhost'
MYSQL_DB = 'stockdatabase'
MYSQL_USER = 'root'
MYSQL_PASS = 'b123456'
insert_total = 0
#主程式

def connect_mysql():  #連線資料庫
    global connect, cursor
    connect = pymysql.connect(host = MYSQL_HOST, db = MYSQL_DB, user = MYSQL_USER, password = MYSQL_PASS,
    charset = 'utf8', use_unicode = True)
    cursor = connect.cursor()


def getdata():
    connect_mysql()
    getdb_st_date = "select st_date from stockdatabase.wespai_p49048 where st_stockno = 1101 order by st_date desc"
    cursor.execute(getdb_st_date)  #執行查詢的SQL
    getdb_st_date = cursor.fetchone()  #如果有取出第一筆資料
    getdb_st_date_result = getdb_st_date[0].strftime('%Y%m%d')
    return getdb_st_date_result


if __name__ == "__main__":  
    getdata()
