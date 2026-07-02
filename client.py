import hmac
import hashlib
import time
import requests
from bot.logging_config import logger

class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str):
        self.base_url = "https://testnet.binancefuture.com"
        self.api_key = api_key
        self.api_secret = api_secret
        self.headers = {
            "X-MBX-APIKEY": self.api_key
        }

    def _generate_signature(self, query_string: str) -> str:
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def place_order(self, params: dict) -> dict:
        endpoint = "/fapi/v1/order"
        url = f"{self.base_url}{endpoint}"
        
        # Inject timestamp for Binance security window
        #params["timestamp"] = int(time.time() * 1000)
        # Inject timestamp for Binance security window
        params["timestamp"] = int(time.time() * 1000)
        params["recvWindow"] = 60000  # Isse Binance 60 seconds tak ka time gap accept karega
        
        # Prepare query string
        query_string = "&".join([f"{k}={v}" for k, v in params.items() if v is not None])
        signature = self._generate_signature(query_string)
        full_query = f"{query_string}&signature={signature}"
        
        logger.info(f"Sending API Request to {endpoint} with params: {query_string}")
        
        try:
            response = requests.post(f"{url}?{full_query}", headers=self.headers, timeout=10)
            response_json = response.json()
            
            if response.status_code == 200:
                logger.info(f"API Success Response: {response_json}")
                return response_json
            else:
                logger.error(f"API Error Response [Status {response.status_code}]: {response_json}")
                raise Exception(f"Binance API Error: {response_json.get('msg', 'Unknown Error')}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error encountered: {str(e)}")
            raise Exception(f"Network/Connection failure: {str(e)}")