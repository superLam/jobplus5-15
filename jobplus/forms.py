# coding=utf8
import os
from flask import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, IntegerField
from wtforms.validators import Required, Length, Email, EqualTo
from jobplus.models import db, User
from flask_wtf.file import FileField, FileRequired


class LoginForm(FlaskForm):  # 登录页面的内容
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_email(self, field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱未被注册')

    def validate_password(self, field):
        user = User.query.filter_by(password=self.password.data).first()
        # 原文件验证的是email，改为password。
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')


# <<<<<<< HEAD
class RegisterForm(FlaskForm):  # 求职者和公司的注册页面内容
    name = StringField('用户名', validators=[Required(message='请输入名字'), Length(1, 64)])
    email = StringField('邮箱', validators=[Required(message='请输入邮箱'), Email()])
    password = PasswordField('密码', validators=[Required(message='密码在6－24字符之内'), Length(6, 24)])
    repear_password = PasswordField(
        '重复密码',
        validators=[Required(), Length(6, 24),
                    EqualTo('password', message='密码要一致')]
    )
    submit = SubmitField('注册')
    '''
class RegisterForm(FlaskForm):  # 求职者和公司的注册页面内容
    name = StringField('用户名', validators=[Required(), Length(1, 64)])
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    # >>>>>>> dev
    '''

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被注册')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('名字已经被注册')

    def create_user(self):
        user = User()
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user


class UserProfileForm(FlaskForm):
    # <<<<<<< HEAD
    real_name = StringField('姓名', validators=[Required(), Length(1, 64)])
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码(no write no change)')
    phone = StringField('手机号', validators=[Required()])
    work_year = IntegerField('工作年限')
    resume_url = FileField('上传简历')
    submit = SubmitField('提交')
    '''
=======
    real_name = StringField('name', validators=[Required(), Length(1, 64)])
    email = StringField('email', validators=[Required(), Email()])
    password = PasswordField('password(no write no change)')
    phone = StringField('phone number', validators=[Required()])
    work_year = IntegerField('work year')
    resume_url = FileField('upload resume')
    submit = SubmitField('submit')
>>>>>>> dev
    '''

    def validate_phone(self, field):
        phone = field.data
        # <<<<<<< HEAD
        if phone[:2] not in ('13', '15', '18') and len(phone) != 11:
            raise ValidationError('请输入一个正确手机号')

    '''
=======
        if phone[:2] not in ('13', '15', '18') and len(phone) != 11:
            raise ValidationError('please enter a correct phone number')
>>>>>>> dev
    '''

    def upload_resume(self):
        f = self.resume.data
        filename = self.real_name.data + '.pdf'
        # <<<<<<< HEAD
        '''
        f.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'resume', filename))
        
        '''
        # =======
        f.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'resume', filename))
        # >>>>>>> dev

        return filename

    def update_profile(self, user):
        user.real_name = self.real_name.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data
        user.phone = self.phone.data
        user.work_year = self.work_year.data
        filename = self.upload_resume()
        user.resume_url = url_for('static', filename=os.path.join('resumes', filename))
        db.session.add(user)
        db.session.commit()
