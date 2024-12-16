import logging
from logging.handlers import RotatingFileHandler
import os

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

info_handler = RotatingFileHandler(f"{log_dir}/info.log", maxBytes=1000000, backupCount=5)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(log_format))

error_handler = RotatingFileHandler(f"{log_dir}/error.log", maxBytes=1000000, backupCount=5)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(log_format))


# 로거 설정
logger = logging.getLogger("portfolio_api")
logger.setLevel(logging.DEBUG)

# 콘솔 핸들러
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 포맷터 설정
formatter = logging.Formatter(log_format)
console_handler.setFormatter(formatter)

# 핸들러 추가
logger.addHandler(console_handler)
logger.addHandler(info_handler)
logger.addHandler(error_handler)
