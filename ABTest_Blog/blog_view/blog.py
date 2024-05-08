from flask import Flask , Blueprint , request , render_template , make_response , jsonify , redirect , url_for, session
from blog_control.user_mgmt import User
from blog_control.session_mgmt import BlogSession
from flask_login import login_user , current_user , logout_user
import datetime
blog_abtest = Blueprint('blog' , __name__)


@blog_abtest.route('/set_email' , methods = ['GET' , 'POST'])
def set_email():
    if request == 'GET':
        #print('hi1')
        #print(request.args.get('user_email'))
        return redirect(url_for('blog.blog1'))
    else:
        #print('hi2')
        #print(request.form['user_email'])
        user = User.create(request.form['user_email'] , request.form['blog_id'])
        login_user(user , remember=True , duration= datetime.timedelta(days = 365))
        
        return redirect(url_for('blog.blog1'))


@blog_abtest.route('/logout')
def logout():
    User.delete(current_user.id)
    logout_user()
    return redirect(url_for('blog.blog1'))


@blog_abtest.route('/blog1')
def blog1():
    if current_user.is_authenticated:
        web_page_name = BlogSession.get_blog_page(current_user.blog_id)
        BlogSession.save_session_info(session['client_id'] , current_user.user_email , web_page_name)
        return render_template(web_page_name , user_email = current_user.user_email)
    else:
        web_page_name = BlogSession.get_blog_page()
        BlogSession.save_session_info(session['client_id'] , 'annoymous' , web_page_name)
        return render_template(web_page_name)