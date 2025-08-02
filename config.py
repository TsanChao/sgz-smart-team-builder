# 配置文件

class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'sgz-smart-team-builder-secret-key'
    
    # 数据文件路径
    DATA_FILE_PATH = 'data/consolidated_ocr_data.json'
    
    # 静态资源路径
    ASSETS_PATH = 'assets/portraits/'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}