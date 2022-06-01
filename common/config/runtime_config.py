
class DevelopmentRuntimeConfig:
    AUTHENTICATION_CLASSES = (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
    REST_FRAMEWORK_DEFAULT_PERMISSION_CLASSES = (
        # 'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    )

    DEBUG = True
    ALLOWED_HOSTS = [
        '127.0.0.1',
        'localhost',
        '0.0.0.0',
        '192.168.0.127',
        '192.168.0.207',
        '192.168.0.257',
   
    ]
    #

    MYSQL_DB_URL = '192.168.0.257'
    MYSQL_DB_PORT = 3306
    MYSQL_DB_USERNAME = "root"
    MYSQL_DB_PASSWORD = "root"
    MYSQL_DB_SCHEMA = "face_recognition_login"

    DATA_DIR = '/home/mamad/'
class RuntimeConfig(DevelopmentRuntimeConfig):
    pass
