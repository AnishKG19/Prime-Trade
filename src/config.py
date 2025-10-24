import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

def validate_config():
    """Validates that required API credentials are set."""
    if not API_KEY or not API_SECRET:
        logging.error("FATAL: BINANCE_API_KEY or BINANCE_API_SECRET is not set.")
        logging.error("Please create a .env file with your Binance Testnet credentials.")
        return False
    
    if "YOUR_TESTNET_API_KEY_HERE" in API_KEY:
        logging.warning("Warning: It looks like you are using the placeholder API key.")
        
    logging.info("Configuration loaded.")
    return True