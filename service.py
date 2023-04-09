import pymysql
import time


# 根据字段把数据存入数据库todolist下的表格task,返回
def create_task(id, title, content, status, end_time):
    code = 200
    db = pymysql.connect(host="localhost", user="root", password="123456", db="todolist")
    cursor = db.cursor()
    # 这些数据都是none
    data = {
        "id": id,
        'title': title,
        'content': content,
        'status': status,
        'add_time': time.localtime(),
        'end_time': end_time,
    }
    table = "task"
    # 获取键
    keys = ",".join(data.keys())
    # 根据数量创建相同个数的%s
    escape = ",".join(["%s"] * len(data))
    # 创建sql语句
    sql = "INSERT INTO {table} ({keys}) VALUES ( {escape});".format(table=table, keys=keys, id=id, escape=escape)
    try:
        cursor.execute(sql, tuple(data.values()))
        print('Success')
        # 提交数据库保存
        db.commit()
    except Exception as e:
        code = 404
        print('Failed')
        print(e)
        db.rollback()
    db.close()
    return code


# 根据id查询单条数据
def show_task(tid):
    code = 200
    db = pymysql.connect(host="localhost", user="root", password="123456", db="todolist")
    cursor = db.cursor()
    sql = "SELECT * FROM task WHERE ID = %s"
    try:
        # 执行sql
        cursor.execute(sql, tid)
        response = cursor.fetchall()
        fields = cursor.description
        # 这是干什么的
        db.commit()
        cursor.close()
        db.close()
    except Exception as e:
        code = 404
        print(e)
        db.rollback()
        cursor.close()
        db.close()
        # 获取数据响应失败
        return {
            "data": "",
            "code": code
        }
    # 字段列表
    column_list = []
    for i in fields:
        # 提取字段名，追加到列表中
        column_list.append(i[0])
    for row in response:
        # 对每条数据（也是元组）
        data = {}  # 创建字典
        for i in range(len(column_list)):
            data[column_list[i]] = str(row[i])
            #  Python字段格式 和json字段格式转换
        return {
            'data': data,
            'code': code,
        }


# 查看所有事项(可选择状态)
def list_task(page, status):
    code = 200
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='todolist')
    cursor = db.cursor()
    # 给的状态非空
    if status != '' and str(status) != 'None':
        # limit 取出条数 offset 偏移量,从0开始,第六条为5
        sql = 'SELECT * FROM task where status = {status} ORDER BY id ASC LIMIT {limit} offset {offset}'.format(
            status=status, limit=5, offset=(5 * int(page) - 5))
    else:
        sql = 'SELECT * FROM task  ORDER BY id ASC LIMIT {limit} offset {offset}'.format(limit=5,
                                                                                         offset=(5 * int(page) - 5))
    try:
        cursor.execute(sql)
        response = cursor.fetchall()
        # 字段格式
        fields = cursor.description
        db.commit()
        cursor.close()
        db.close()
    except Exception as e:
        code = 404
        print(e)
        db.rollback()
        cursor.close()
        db.close()
        return {
            "data": "",
            "code": code
        }
    column_list = []
    for i in fields:
        column_list.append(i[0])
    data = {}
    # 记录数据条数
    number = 0
    # 对每条数据进行操作
    for row in response:
        # row是tuple
        number += 1
        # 创建一个字典task存一条临时数据
        task = {}
        for i in range(len(column_list)):
            # i从0到len-1
            task[column_list[i]] = str(row[i])
        # 这里好像有点问题
        data[number] = task
    return {
        'data': data,
        'total': number,
        'code': code,
    }


def update_task(tid, status):
    code = 200
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='todolist')
    cursor = db.cursor()
    sql = "UPDATE task SET status=%s WHERE id = %s"
    try:
        # 执行SQL语句
        cursor.execute(sql, (status, tid))
        # 提交到数据库执行
        db.commit()
        cursor.close()
    except Exception as e:
        print(e)
        code = 404
        # 发生错误时回滚
        db.rollback()
    db.close()
    return code


def update_tasks(status):
    code = 200
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='todolist')
    cursor = db.cursor()
    sql = "UPDATE task SET status=%s "
    try:
        # 执行SQL语句
        cursor.execute(sql, status)
        # 提交到数据库执行
        db.commit()
        cursor.close()
    except Exception as e:
        print(e)
        code = 404
        # 发生错误时回滚
        db.rollback()
    db.close()
    return code


def delete_task(tid):
    code = 200
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='todolist')
    cursor = db.cursor()
    sql = "DELETE FROM task WHERE id=%s;"
    try:
        cursor.execute(sql, tid)  # 注意tid是字符串
        cursor.close()
        db.commit()
    except Exception as e:
        code = 404
        print(e)
        db.rollback()
    db.close()
    return code


def delete_tasks(status):
    code = 200
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='todolist')
    cursor = db.cursor()
    if status != '' and str(status) != 'None':
        sql = "DELETE FROM task where status = '{status}'".format(status=status)
    else:
        sql = "DELETE FROM task"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        print(e)
        code = 404
        # 发生错误时回滚
        db.rollback()
    db.close()
    return code


def find_task(page, keyword):
    code = 200
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='todolist')
    cursor = db.cursor()
    sql = "SELECT * FROM task  WHERE (title like'%{keyword}%' or content like '%{keyword}%') ORDER BY id ASC LIMIT {limit} offset {offset}".format(
        limit=5,
        offset=(5 * int(page) - 5), keyword=keyword)
    # 执行SQL语句
    cursor.execute(sql)
    res = cursor.fetchall()
    fields = cursor.description
    # 提交到数据库执行
    db.commit()
    cursor.close()
    db.close()
    column_list = []
    for i in fields:
        # 提取字段名，追加到列表中
        column_list.append(i[0])
    data = {}
    number = 0
    for row in res:
        number += 1
        task = {}
        for i in range(len(column_list)):
            task[column_list[i]] = str(row[i])
        data[number] = task
    return {
        'data': data,
        'total': number,
        'code': code,
    }