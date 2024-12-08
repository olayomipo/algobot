import MetaTrader5 as mt5

def login_to_mt5(account, password, server):
    """
    Logs into an MT5 account.
    
    Parameters:
        account (int): The account number.
        password (str): The account password.
        server (str): The trading server name.
    
    Returns:
        bool: True if login is successful, False otherwise.
    """
    if not mt5.initialize():
        print("MetaTrader5 initialization failed")
        return False

    if mt5.login(account, password=password, server=server):
        print(f"Successfully logged in to account {account}")
        return True
    else:
        print(f"Login failed. Error: {mt5.last_error()}")
        mt5.shutdown()
        return False


def place_trade(symbol, action, lot_size, sl=None, tp=None):
    """
    Places a trade on the MT5 account.
    
    Parameters:
        symbol (str): The trading symbol (e.g., "EURUSD").
        action (str): The trade action ("buy" or "sell").
        lot_size (float): The volume of the trade in lots.
        sl (float, optional): Stop loss price. Default is None.
        tp (float, optional): Take profit price. Default is None.
    
    Returns:
        dict: The trade result dictionary.
    """
    # Get symbol information
    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        print(f"Symbol {symbol} not found")
        return None
    if not symbol_info.visible:
        if not mt5.symbol_select(symbol, True):
            print(f"Failed to select symbol {symbol}")
            return None

    # Determine trade type
    if action.lower() == "buy":
        trade_type = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).ask
    elif action.lower() == "sell":
        trade_type = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).bid
    else:
        print("Invalid trade action. Use 'buy' or 'sell'.")
        return None

    # Prepare the trade request
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": trade_type,
        "price": price,
        "sl": sl,  # Stop Loss
        "tp": tp,  # Take Profit
        "deviation": 10,  # Slippage tolerance in points
        "magic": 234000,  # Custom identifier for the trade
        "comment": "Trade placed by Python",
    }

    # Send the trade request
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Trade failed. Retcode: {result.retcode}. Error: {mt5.last_error()}")
        return None

    print(f"Trade successful. Order placed with ticket: {result.order}")
    return result._asdict()

def place_pending_order(symbol, order_type, lot_size, price, sl=None, tp=None):
    """
    Places a pending order on the MT5 account.

    Parameters:
        symbol (str): The trading symbol (e.g., "EURUSD").
        order_type (int): The type of order (e.g., mt5.ORDER_TYPE_BUY_LIMIT).
        lot_size (float): The volume of the trade in lots.
        price (float): The price at which the order will trigger.
        sl (float, optional): Stop loss price. Default is None.
        tp (float, optional): Take profit price. Default is None.

    Returns:
        dict: The trade result dictionary.
    """
    # Prepare the trade request
    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": lot_size,
        "type": order_type,
        "price": price,
        "sl": sl,  # Stop Loss
        "tp": tp,  # Take Profit
        "deviation": 10,  # Slippage tolerance in points
        "magic": 234000,  # Custom identifier for the trade
        "comment": "Pending order placed by Python",
    }

    # Send the trade request
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Order failed. Retcode: {result.retcode}. Error: {mt5.last_error()}")
        return None

    print(f"Order successful. Ticket: {result.order}")
    return result._asdict()


# # Example usage
# symbol = "EURUSD"
# lot_size = 0.1
# price = 1.1150  # Example price below current market
# order_type = mt5.ORDER_TYPE_BUY_LIMIT

# mt5.ORDER_TYPE_BUY 
# mt5.ORDER_TYPE_SELL 
# mt5.ORDER_TYPE_BUY_LIMIT
# mt5.ORDER_TYPE_SELL_LIMIT
# mt5.ORDER_TYPE_BUY_STOP
# mt5.ORDER_TYPE_SELL_STOP
# mt5.ORDER_TYPE_BUY_STOP_LIMIT
# mt5.ORDER_TYPE_SELL_STOP_LIMIT

# result = place_pending_order(symbol, order_type, lot_size, price, sl=1.1100, tp=1.1200)
# if result:
#     print(f"Order result: {result}")
