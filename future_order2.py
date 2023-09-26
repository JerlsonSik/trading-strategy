from binance.client import Client
from pprint import pprint

# Replace with your Binance API key and secret
API_KEY = 't6dxBytsovc88DlFKHNb6sFmhgK6Pud7mMuNJ16JSLLjr5o8QkJV02FB8qd3iF8f'
API_SECRET = 'St8QBQ3kB8O4Ru3D9yO1aN0mNoeeCRbcyjYEORcF2IimPHyevWpDoZRqQjWPDPkQ'

client = Client(API_KEY, API_SECRET)


def place_limit_order(symbol, side, quantity, price, order_type):
    order = client.futures_create_order(
        symbol=symbol,
        side=side,
        quantity=quantity,
        price=price,
        type=order_type,
        # timeInForce='GTC'
    )
    return order

def place_market_order(symbol, side, quantity, order_type):
    order = client.futures_create_order(
        symbol=symbol,
        side=side,
        quantity=quantity,
        type=order_type,
    )
    return order

# Example usage
symbol = 'ETHBUSD'       # Replace with the trading pair you want
side = Client.SIDE_BUY   # or Client.SIDE_SELL
quantity = 0.005         # Quantity of the asset you want to buy/sell
# quantity = 0.300         # Quantity of the asset you want to buy/sell
# price = 40000.0          # Limit price for the order
order_type = Client.ORDER_TYPE_MARKET  # 'LIMIT', 'MARKET', etc.

response = place_market_order(symbol, side, quantity, order_type)
print(response)
