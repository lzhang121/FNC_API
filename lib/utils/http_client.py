import requests
from lib.utils.logger import get_logger
from urllib.parse import urljoin

logger = get_logger()

class ApiClient(requests.Session):
    def __init__(self, base_url: str, token: str = None):
        super().__init__()
        self.base_url = base_url
        if token:
            self.headers.update({
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            })
        logger.info(f"ApiClient initialized for base_url: {self.base_url}")

    def request(self, method, url, **kwargs):
        # Use urljoin for robust URL construction
        full_url = urljoin(self.base_url, url)
        
        logger.info(f"[HTTP] {method.upper()} {full_url}")
        if kwargs.get("json"):
            logger.debug(f"[HTTP] Payload: {kwargs['json']}")
        
        try:
            response = super().request(method, full_url, **kwargs)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            
            logger.info(f"[HTTP] Status: {response.status_code}")
            # Log response body at a lower level to avoid clutter
            logger.debug(f"[HTTP] Response: {response.text}")
            
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"[HTTP] Request failed: {e}")
            # You might want to return None or a custom error object
            # depending on how you want your tests to handle failures.
            return None