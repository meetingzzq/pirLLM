import logging
import os
from datetime import datetime

def setup_logger(name, log_folder='logs'):
    """设置日志配置"""
    # 创建日志文件夹
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    
    # 生成日志文件名，包含日期
    today = datetime.now().strftime('%Y%m%d')
    log_file = os.path.join(log_folder, f'{name}_{today}.log')
    
    # 创建logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # 文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 设置日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger 