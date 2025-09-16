import requests
from tests.utils.logger import get_logger

logger = get_logger()

def create_logged_session(base_url: str, token: str = None):
    """
    创建带日志功能的 requests.Session
    :param base_url: 基础 URL (例如 http://test01.gateway.fncjob.com:48080/)
    :param token: 认证 Token，可选
    :return: 带日志功能的 session
    """
    session = requests.Session()
    if token:
        session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })

    logger.info(f"token: {token} session.header:{session.headers}")
    # 保存原始 request 方法
    original_request = session.request

    def request_with_log(method, url, **kwargs):
        # 拼接 URL，防止双斜杠问题
        full_url = f"{base_url.rstrip('/')}/{url.lstrip('/')}"
        logger.info(f"[HTTP] {method.upper()} {full_url}")
        if kwargs.get("json"):
            logger.info(f"[HTTP] Payload: {kwargs['json']}")
        logger.info(f"[HTTP] Headers: {session.headers}")

        resp = original_request(method, full_url, **kwargs)

        logger.info(f"[HTTP] Status: {resp.status_code}")
        logger.info(f"[HTTP] Response: {resp.text}")
        return resp

    session.request = request_with_log
    return session
