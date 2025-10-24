import logging
from binance import Client  # [cite: 13]
from binance.exceptions import BinanceAPIException

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True): # [cite: 15]
        """
        Initializes the BasicBot.
        :param api_key: Your Binance API key
        :param api_secret: Your Binance API secret
        :param testnet: Flag to use testnet URLs
        """
        self.client = Client(api_key, api_secret) # [cite: 16]
        self.logger = logging.getLogger(__name__)
        
        if testnet:
            # Set client to use Binance Futures Testnet URL [cite: 8]
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
            self.logger.info("Bot configured to use Binance Futures Testnet.")
        
        self.logger.info("Bot initialized.")
        self._test_connectivity()

    def _test_connectivity(self):
        """Tests API connectivity."""
        try:
            self.client.futures_account_balance()
            self.logger.info("API connection successful.")
        except BinanceAPIException as e:
            self.logger.error(f"API connection failed: {e}")
        except Exception as e:
            self.logger.error(f"An unexpected error occurred during connection test: {e}")

    def place_market_order(self, symbol, side, quantity):
        """
        Places a market order. [cite: 20]
        :param symbol: e.g., "BTCUSDT"
        :param side: "BUY" or "SELL" [cite: 21]
        :param quantity: Amount to trade, e.g., 0.001
        """
        side = side.upper()
        self.logger.info(f"Attempting MARKET {side} order: {quantity} {symbol}")
        
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            self.logger.info(f"MARKET order successful. Response: {order}") # [cite: 11]
            return order # [cite: 24]
        except BinanceAPIException as e:
            self.logger.error(f"MARKET order API error: {e}") # 
            return {"error": str(e)}
        except Exception as e:
            self.logger.error(f"MARKET order unexpected error: {e}") # [cite: 25]
            return {"error": str(e)}

    def place_limit_order(self, symbol, side, quantity, price):
        """
        Places a limit order. [cite: 20]
        :param symbol: e.g., "BTCUSDT"
        :param side: "BUY" or "SELL" [cite: 21]
        :param quantity: Amount to trade, e.g., 0.001
        :param price: Price to set the limit order at
        """
        side = side.upper()
        self.logger.info(f"Attempting LIMIT {side} order: {quantity} {symbol} @ {price}")
        
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                quantity=quantity,
                price=price,
                timeInForce='GTC'  # Good 'Til Canceled
            )
            self.logger.info(f"LIMIT order successful. Response: {order}") # [cite: 11]
            return order # [cite: 24]
        except BinanceAPIException as e:
            self.logger.error(f"LIMIT order API error: {e}") # 
            return {"error": str(e)}
        except Exception as e:
            self.logger.error(f"LIMIT order unexpected error: {e}") # [cite: 25]
            return {"error": str(e)}