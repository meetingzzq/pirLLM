import os
from typing import Dict, Any

class Config:
    # API配置
    API_BASE = 'https://api.siliconflow.cn/v1'
    API_KEY = 'sk-elgvqsyxgfpusvhxtypjdtxkppttswuefuieaijgemkmrtld'
    
    # 模型配置
    MODEL = 'deepseek-ai/DeepSeek-V2.5'
    TEMPERATURE = 0.1
    
    # 日志配置
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # 数据库配置
    DB_CONFIG = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'password',
        'database': 'email_system'
    }
    
    # 邮件系统配置
    EMAIL_FOLDERS = {
        'inbox': 'INBOX',
        'working': 'WORKING',
        'ignore': 'IGNORE',
        'create': 'CREATE',
        'update': 'UPDATE',
        'error': 'ERROR'
    }
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """获取所有配置"""
        return {
            'api': {
                'base': cls.API_BASE,
                'key': cls.API_KEY
            },
            'model': {
                'name': cls.MODEL,
                'temperature': cls.TEMPERATURE
            },
            'logging': {
                'level': cls.LOG_LEVEL,
                'format': cls.LOG_FORMAT
            },
            'database': cls.DB_CONFIG,
            'email_folders': cls.EMAIL_FOLDERS
        }
    
    @classmethod
    def setup_environment(cls):
        """设置环境变量"""
        os.environ['OPENAI_API_BASE'] = cls.API_BASE
        os.environ['OPENAI_API_KEY'] = cls.API_KEY 