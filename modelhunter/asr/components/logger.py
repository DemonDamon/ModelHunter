import logging
import os
from logging.handlers import RotatingFileHandler

class Logger:
    @staticmethod
    def get_logger(name: str, log_file: str = None, level=logging.INFO):
        """创建并配置日志记录器"""
        logger = logging.getLogger(name)

        # 如果已经配置过 handler，则跳过配置
        if not logger.handlers:
            logger.setLevel(level)

            # 创建控制台日志处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)

            # 日志格式
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)

            # 添加控制台处理器
            logger.addHandler(console_handler)

            # 如果提供了日志文件路径，则添加文件处理器
            if log_file:
                try:
                    # 使用 RotatingFileHandler 以处理日志文件轮换
                    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
                    file_handler.setLevel(level)
                    file_handler.setFormatter(formatter)
                    logger.addHandler(file_handler)
                except Exception as e:
                    logger.error(f"Failed to set up file handler: {str(e)}")
        
        return logger

# 设置日志目录和文件路径
LOG_DIR = os.getenv("LOG_DIR", "/var/log/myapp/")
if not os.path.exists(LOG_DIR):
    try:
        os.makedirs(LOG_DIR)
    except OSError as e:
        print(f"Error creating log directory {LOG_DIR}: {str(e)}")
        LOG_DIR = "./logs"  # 回退到当前目录的 logs 文件夹
        os.makedirs(LOG_DIR, exist_ok=True)

# 配置主日志文件路径
MAIN_LOG_FILE = os.path.join(LOG_DIR, "application.log")
