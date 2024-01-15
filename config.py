class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:user@mysql/invitation_sender'
    SECRET_KEY = 'password'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False  # from row 4 to row 7 is setup for gmail via SSL
    MAIL_USE_SSL = True  # now app is not working because the confidential data is removed
    MAIL_USERNAME = ''  # your email address
    MAIL_PASSWORD = ''  # your 16 digit password
    MAIL_DEFAULT_SENDER = ''  # your email address
