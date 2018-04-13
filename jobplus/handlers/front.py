from flask import render_template,redirect,url_for
from flask_login import login_user
from flask_wtf import Form
from jobplus.forms import LoginForm

@front.route('/login',methods=['GET','POST'])    #
def login():
    form = LoginForm
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()  #数据库表名字User，可以改。这里还缺少判断登录人员的类型。
        login_user(user,form.remember_me.data)
        return redirect(url_for('用户简历管理'))
    return render_template('login.html',form=form)
