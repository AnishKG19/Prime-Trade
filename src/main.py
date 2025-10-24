import logging
import sys
import pprint
from src.logger import setup_logging
from src import config
from src.bot import BasicBot

# Setup logging
setup_logging()

def get_validated_input(prompt, validator_type):
    """
    Gets and validates user input from the CLI. 
    :param prompt: The message to display to the user
    :param validator_type: 'symbol', 'side', 'quantity', or 'price'
    :return: A validated and formatted value
    """
    while True:
        value = input(prompt).strip()
        
        if validator_type == 'symbol':
            if not value:
                print("Error: Symbol cannot be empty.")
                continue
            return value.upper()
            
        elif validator_type == 'side':
            if value.lower() not in ['buy', 'sell']:
                print("Error: Side must be 'buy' or 'sell'.")
                continue
            return value.upper() # [cite: 21]
            
        elif validator_type == 'quantity' or validator_type == 'price':
            try:
                f_value = float(value)
                if f_value <= 0:
                    print(f"Error: {validator_type.capitalize()} must be positive.")
                    continue
                return f_value
            except ValueError:
                print(f"Error: Invalid {validator_type}. Please enter a number.")
                continue
        
        # Fallback for unhandled validator types
        return value

def handle_market_order(bot):
    """Guides user through placing a market order."""
    print("\n--- Place Market Order ---")
    symbol = get_validated_input("Enter symbol (e.g., BTCUSDT): ", 'symbol')
    side = get_validated_input("Enter side (buy/sell): ", 'side')
    quantity = get_validated_input("Enter quantity (e.g., 0.001): ", 'quantity')
    
    print("\nConfirming order...")
    result = bot.place_market_order(symbol, side, quantity)
    print("--- Order Result ---")
    pprint.pprint(result) # [cite: 24]
    print("----------------------")

def handle_limit_order(bot):
    """Guides user through placing a limit order."""
    print("\n--- Place Limit Order ---")
    symbol = get_validated_input("Enter symbol (e.g., BTCUSDT): ", 'symbol')
    side = get_validated_input("Enter side (buy/sell): ", 'side')
    quantity = get_validated_input("Enter quantity (e.g., 0.001): ", 'quantity')
    price = get_validated_input(f"Enter limit price (for {symbol}): ", 'price')
    
    print("\nConfirming order...")
    result = bot.place_limit_order(symbol, side, quantity, price)
    print("--- Order Result ---")
    pprint.pprint(result) # [cite: 24]
    print("----------------------")

def main_menu(bot):
    """Displays the main CLI menu."""
    while True:
        print("\n===== Binance Futures Bot Menu =====")
        print("1. Place Market Order")
        print("2. Place Limit Order")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            handle_market_order(bot)
        elif choice == '2':
            handle_limit_order(bot)
        elif choice == '3':
            print("Exiting bot. Goodbye!")
            logging.info("User exited the application.")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

def main():
    """Main application entry point."""
    logger = logging.getLogger(__name__)
    logger.info("Application starting...")
    
    # Validate configuration 
    if not config.validate_config():
        sys.exit(1) # Exit if keys are missing
        
    try:
        # Initialize the bot [cite: 15]
        bot = BasicBot(
            api_key=config.API_KEY,
            api_secret=config.API_SECRET,
            testnet=True
        )
        
        # Run the main menu
        main_menu(bot)
        
    except Exception as e:
        logger.critical(f"A critical error occurred: {e}", exc_info=True)
        print(f"A critical error occurred. Check the log file for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()