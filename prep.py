import MetaTrader5 as mt5
import json


def get_symbols_info():
    """
    Retrieves all available symbols and their essential details.
    
    Returns:
        dict: A dictionary containing symbol information.
    """
    if not mt5.initialize():
        print("Failed to initialize MetaTrader 5")
        return None

    symbols = mt5.symbols_get()
    if not symbols:
        print("No symbols found or unable to retrieve symbols.")
        mt5.shutdown()
        return None

    # Extract essential details for each symbol
    symbols_info = {}
    for index, symbol in enumerate(symbols):
        symbols_info[symbol.name] = {
            "name": symbol.name,
            "description": symbol.description,
            "path": symbol.path,
            "bid": symbol.bid,
            "ask": symbol.ask,
            "point": symbol.point,
            "digits": symbol.digits,
            "spread": symbol.spread,
            "tick_size": symbol.tick_size,
            "trade_contract_size": symbol.trade_contract_size,
            "margin_initial": symbol.margin_initial,
        }

        # symbols_info[index] = {
        #     "name": symbol.name,
        #     "description": symbol.description,
        #     "path": symbol.path,
        #     "bid": symbol.bid,
        #     "ask": symbol.ask,
        #     "point": symbol.point,
        #     "digits": symbol.digits,
        #     "spread": symbol.spread,
        #     "tick_size": symbol.tick_size,
        #     "trade_contract_size": symbol.trade_contract_size,
        #     "margin_initial": symbol.margin_initial,
        # }

    mt5.shutdown()
    return symbols_info


def get_actions_list():
    """
    Returns the possible trade actions in MetaTrader 5.
    
    Returns:
        list: A list of possible trade actions.
    """
    actions = [
        "buy",   # Open a buy order
        "sell",  # Open a sell order
        "close"  # Close an existing position
    ]
    return actions


# Fetch symbols and actions
symbols_info = get_symbols_info()
actions_list = get_actions_list()

# Save to JSON
if symbols_info:
    with open("symbols_info.json", "w") as file:
        json.dump(symbols_info, file, indent=4)
    print("Symbols information saved to symbols_info.json")

# Display actions
print("Possible trade actions:", actions_list)
