import logging
import sys
import os
from logging.handlers import TimedRotatingFileHandler

# 自定义日志处理器，将 print 输出重定向到日志
class StreamToLogger:
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level

    def write(self, message):
        if message.strip():  # 忽略空行
            self.logger.log(self.log_level, message.strip())

    def flush(self):
        pass  # 不需要实现



# 确保logs目录存在
log_dir = './logs'
if not os.path.exists(log_dir):
    try:
        os.makedirs(log_dir)
        logging.info(f"Created logs directory: {log_dir}")
    except Exception as e:
        logging.error(f"Failed to create logs directory: {e}")

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # 输出到控制台
        TimedRotatingFileHandler(
            filename=os.path.join(log_dir, 'pet.log'),  # 日志文件路径
            when='midnight',  # 每天午夜轮转
            encoding='utf-8'  # 设置编码
        )
    ]
)

# 创建logger
logger = logging.getLogger('pet')
logger.setLevel(logging.DEBUG)  # 设置日志级别

# 重定向 sys.stdout 和 sys.stderr 到日志记录器
sys.stdout = StreamToLogger(logger, logging.INFO)
sys.stderr = StreamToLogger(logger, logging.ERROR)