import logging
import sys
import os

def setup_logger(name="scanpy-mcp-server", log_file=None):
    """
    配置并返回一个日志记录器
    
    参数:
    name: 日志记录器名称
    log_file: 日志文件名，如果为None则使用name.log
    log_to_stdout: 是否输出到标准输出
    log_dir: 日志文件目录
    
    返回:
    配置好的日志记录器
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # 如果已经有处理器，则不再添加
    if logger.handlers:
        return logger
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        '%Y-%m-%d %H:%M:%S'
    )
    
    if log_file:
        log_handler = logging.FileHandler(log_file)
        log_handler.setFormatter(formatter)
        logger.addHandler(log_handler)
        
        logger.info(f"logging output: {log_file}")
    else:
        log_handler = logging.StreamHandler(sys.stdout)
        log_handler.setFormatter(formatter)
        logger.addHandler(log_handler)
        logger.info(f"loggin file output: stdout")
    return logger