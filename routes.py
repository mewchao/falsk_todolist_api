from flask import Flask, request, jsonify
from service import create_task, list_task, show_task, update_task, update_tasks, delete_task, delete_tasks, find_task

app = Flask(__name__)


def todolist(app):
    # 添加一条新的待办事项
    @app.route("/task/<int:id>", methods=["POST"])  # 在服务器新建一个资源
    def create(id):
        try:
            json = request.get_json()
            title = json["title"]
            content = json["content"]
            status = json["status"]
            end_time = json["end_time"]
            code = create_task(id, title, content, status, end_time)
            if code == 200:
                return jsonify(code=200, msg="success")
            elif code == 404:
                return jsonify(code=404, msg="该活动不存在")
        except Exception as e:
            print(e)
            return jsonify(code=404, msg="该活动不存在")

    # 通过id查询事项
    @app.route("/task/<int:tid>", methods=['GET'])
    def find_id(tid):
        response = show_task(tid)
        if response['code'] == 200:
            return jsonify(code=200, msg="success", data=response['data'])
        elif response["code"] == 404:
            return jsonify(code=404, msg="该活动不存在")

    # 查看所有事项(可选择状态)
    @app.route("/tasks/<int:page>", methods=['GET'])
    def show_all(page):
        status = request.args.get('status')
        # 当get请求时， 需要使用request.args来获取数据
        # 当post请求时，需要使用request.form来获取数据
        response = list_task(page, status)  # 返回的是字典
        if response["code"] == 200:
            return jsonify(code=200, msg="success", data=response["data"] )

    # 设置一条待办事项的状态
    @app.route("/task/<int:tid>", methods=['PUT'])
    def update_one(tid):
        status = request.args.get('status')
        code = update_task(tid, status)
        if code == 200:
            return jsonify(code=200, msg="success", )
        elif code == 404:
            return jsonify(code=404, msg="该活动不存在")

    # 设置所有待办事项的状态
    @app.route("/tasks", methods=['PUT'])
    def update_all():
        status = request.args.get('status')
        code = update_tasks(status)
        if code == 200:
            return jsonify(code=200, msg="success", )
        elif code == 404:
            return jsonify(code=404, msg="该活动不存在")

    # 删除一条事项
    @app.route("/task/<int:tid>", methods=['DELETE'])
    def delete_one(tid):
        code = delete_task(tid)
        if code == 200:
            return jsonify(code=200, msg="success")
        elif code == 404:
            return jsonify(code=404, msg="该活动不存在")

    # 删除所有已完成/所有待办/所有事项
    @app.route("/tasks", methods=['DELETE'])
    def delete_all():
        status = request.args.get('status')
        code = delete_tasks(status)
        if code == 200:
            return jsonify(code=200, msg="success", )
        elif code == 404:
            return jsonify(code=404, msg="该活动不存在")

    # 输入关键字查询事项
    @app.route("/tasks/find-keyword/<int:page>", methods=['GET'])
    def find_keyword(page):
        keyword = request.args.get('keyword')
        res = find_task(page, keyword)
        if res['code'] == 200:
            return jsonify(code=200, msg="success", data=res['data'], total=res['total'])
        elif res['code'] == 404:
            return jsonify(code=404, msg="该活动不存在")
    app.run()

    
todolist(app)