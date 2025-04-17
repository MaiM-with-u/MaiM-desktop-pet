import logging

logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]  # 输出到控制台
)
# 创建logger
logger = logging.getLogger('pet')
logger.setLevel(logging.DEBUG)  # 设置日志级别