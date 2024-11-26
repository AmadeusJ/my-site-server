import logging

# 로거 설정
logger = logging.getLogger("portfolio_api")
logger.setLevel(logging.DEBUG)

# 콘솔 핸들러
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 포맷터 설정
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

# 핸들러 추가
logger.addHandler(console_handler)