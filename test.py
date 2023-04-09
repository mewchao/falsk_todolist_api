import time

import pymysql

# from service import create_task
# # title ='title'
# # content = 'content'
# # status = 'status'
# # end_time = 'end_time'
# # code = create_task(title, content, status, end_time)
# # print(code)
# print(time.time())
# data = {
#     'title': "title",
#     'content': "content",
#     'status': "status",
#     'add_time': time.time(),
#     'end_time': "end_time",
# }
# table="task"
# key=data.keys()
# keys = ', '.join(data.keys())
# values = ', '.join(['%s'] * len(data))
#
#
# print(keys)
# print(key)
# print(values)
# print(sql)
db = pymysql.connect(host="localhost", user="root", password="123456", db="todolist")
cursor = db.cursor()
sql = "SELECT * FROM task WHERE ID = 1;"
cursor.execute(sql)
response = cursor.fetchall()
fields = cursor.description
# 这是干什么的
db.commit()
cursor.close()
db.close()
print(response)
# ((1, 'c', 'homeword', 'yes', datetime.datetime(2002, 1, 2, 0, 0), datetime.datetime(2023, 2, 14, 0, 0)),)
print(fields)
# (('id', 3, None, 11, 11, 0, True), ('title', 253, None, 200, 200, 0, True), ('content', 253, None, 200, 200, 0, True), ('status', 253, None, 40, 40, 0, True), ('add_time', 7, None, 19, 19, 0, True), ('end_time', 7, None, 19, 19, 0, True))

for i in range(3):
    print(i)
print('加油，你可以的！！！')

print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
