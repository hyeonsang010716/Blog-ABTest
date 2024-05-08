from flask import Flask , jsonify , request , render_template , make_response , session
from flask_login import LoginManager , current_user , login_required , login_user , logout_user
from flask_cors import CORS 
from blog_view import blog
from blog_control.user_mgmt import User
import os
#https 만을 지원하는 기능을 http에서도 지원할 수 있도록 테스트 가능하게 만듬
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app = Flask(__name__ , static_url_path='/static') #html에서 가져올 데이터는 static 에서 가지고 와라
CORS(app) #별도 서버 간에 rest api 지원을 하기 위해서 
app.secret_key = 'hyeonsang_server3'


app.register_blueprint(blog.blog_abtest , url_prefix = '/blog')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return make_response(jsonify(success = False) , 401)


@app.before_request
def app_befor_request():
    if 'client_id' not in session:
        session['client_id'] = request.environ.get('HTTP_X_REAL_IP' , request.remote_addr)

if __name__ == '__main__':
    app.run(host = '0.0.0.0' , port='8080' , debug=True)
    