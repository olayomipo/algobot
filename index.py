
from login import login_to_mt5, place_trade
import MetaTrader5 as mt5

account = 12345678  # Replace with your account number
password = "your_password"  # Replace with your account password
server = "YourBroker-Server"  # Replace with your broker's server name

if login_to_mt5(account, password, server):
    print("Login successful")
else:
    print("Login failed")

symbol = "EURUSD"
action = "buy" #["buy", "sell", "close"]
lot_size = 0.1  # 0.1 lot

trade_result = place_trade(symbol, action, lot_size, sl=1.0800, tp=1.1000)
if trade_result:
    print(f"Trade result: {trade_result}")

mt5.shutdown()
