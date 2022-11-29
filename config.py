from decouple import config

class Config:
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    AUTH_USER = config('AUTH_USER', default=None);
    AUTH_PWD_TOKEN = config('AUTH_PWD_TOKEN', default=None);
    ATLASSIAN_API_URL = config('ATLASSIAN_API_URL', default=None);
    
class ProductionConfig(Config):
    DEBUG = False
    AUTH_USER = config('AUTH_USER', default=None);
    AUTH_PWD_TOKEN = config('AUTH_PWD_TOKEN', default=None);
    ATLASSIAN_API_URL = config('ATLASSIAN_API_URL', default=None);

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}