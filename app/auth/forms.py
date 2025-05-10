from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models.user import User

class LoginForm(FlaskForm):
    """用户登录表单"""
    username = StringField('用户名', validators=[DataRequired(message='请输入用户名')])
    password = PasswordField('密码', validators=[DataRequired(message='请输入密码')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class RegistrationForm(FlaskForm):
    """用户注册表单"""
    username = StringField('用户名', validators=[
        DataRequired(message='请输入用户名'), 
        Length(min=3, max=20, message='用户名长度必须在3-20个字符之间')
    ])
    email = StringField('邮箱', validators=[
        DataRequired(message='请输入邮箱'), 
        Email(message='请输入有效的邮箱地址')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='请输入密码'),
        Length(min=6, message='密码长度不能少于6个字符')
    ])
    password2 = PasswordField('确认密码', validators=[
        DataRequired(message='请再次输入密码'), 
        EqualTo('password', message='两次密码不一致')
    ])
    role = SelectField('角色', choices=[
        ('customer', '客户'), 
        ('manager', '客户经理'),
        ('admin', '管理员')
    ], validators=[DataRequired(message='请选择角色')])
    submit = SubmitField('注册')

    def validate_username(self, username):
        """验证用户名是否已存在"""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('该用户名已被使用，请选择其他用户名')

    def validate_email(self, email):
        """验证邮箱是否已存在"""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('该邮箱已被注册，请使用其他邮箱')

class ChangePasswordForm(FlaskForm):
    """修改密码表单"""
    old_password = PasswordField('原密码', validators=[DataRequired(message='请输入原密码')])
    password = PasswordField('新密码', validators=[
        DataRequired(message='请输入新密码'),
        Length(min=6, message='密码长度不能少于6个字符')
    ])
    password2 = PasswordField('确认新密码', validators=[
        DataRequired(message='请再次输入新密码'), 
        EqualTo('password', message='两次密码不一致')
    ])
    submit = SubmitField('更新密码') 