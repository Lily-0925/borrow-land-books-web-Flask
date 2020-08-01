import os


DEBUG = True

SQLALCHEMY_DATABASE_URI = "mysql+cymysql://root:123456@localhost:3306/fisher"
SECRET_KEY = os.environ.get('SECRET_KEY') or b'"[\xe8\x9cZ\xaaL/\xaaw\xcf\xdf\x893\xb0|'

#email 配置
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = "2711279210@qq.com"
MAIL_PASSWORD = ""