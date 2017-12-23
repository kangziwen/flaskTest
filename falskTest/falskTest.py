from flask import Flask, render_template, request, redirect, url_for,make_response
from werkzeug.routing import BaseConverter
from werkzeug.utils import secure_filename
from os import path
from flask.ext.script import Manager


# 正则动态匹配url
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter
manger = Manager(app)

@app.route('/')
def hello_world():
    # 获取cookie
    # request.cookies['']

    return 'Hello World!1234'


@app.route('/index')
def index():
    print(request.cookies)
    # 设置cookie
    response = make_response(render_template('index.html', canshu='diyigejiemian....'))
    response.set_cookie('username','kzw')
    return response


@app.route('/index1')
def index1():
    return render_template('index1.html')


@app.route('/index2')
def index2():
    return render_template('index2.html')


@app.route('/user/<username>')
def user(username):
    return "名字 ： {}".format(username)


# int 整型 float 浮点型 path 路径
@app.route('/user1/<int:user_id>')
def user1(user_id):
    return "名字 ： {}".format(user_id)


# 自定义正则匹配
@app.route('/user2/<regex("[a-z]{3}[A-Z]"):user_id>')
def user2(user_id):
    return "名字 ： {}".format(user_id)


@app.route('/projects/')
@app.route('/out-works/')
def projects():
    return 'the project page'


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print('POST : ', username, password)
    elif request.method == 'GET':
        print("get : ", request.args)
        aa = request.args['aa']
        print('aa : ', aa)
    return render_template('login.html', method=request.method)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        print('upload post ....',request.files)
        f = request.files['file']
        basepath = path.basename(__file__)
        upload_path = path.join(basepath, '\\static\\uploads',secure_filename(f.filename))
        print('upload_path : ',upload_path,type(upload_path))
        print('f : ',f)

        f.save(upload_path)
        return redirect(url_for('upload'))
    return render_template('upload.html')

@app.errorhandler(404)
def page_not_found(error):
    print(error)
    return render_template('404.html'),404
@manger.command
def dev():
    # 命令行运行 python falskTest.py dev
    from livereload import Server
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url=True)
if __name__ == '__main__':
    # app.run(debug=True)
    # 运行
    # python falskTest.py runserver

    manger.run()