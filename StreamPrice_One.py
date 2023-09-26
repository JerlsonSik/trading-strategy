import json
import websocket
import datetime

def ws_trades(): 
    socket = f'wss://stream.binance.com:9443/ws/ethusdt@trade'

    def on_message(wsapp,message):  
        json_message = json.loads(message)
        handle_trades(json_message)

    def on_error(wsapp,error):
        print(error)

    wsapp = websocket.WebSocketApp(socket, on_message=on_message, on_error=on_error)
    wsapp.run_forever()
    
def handle_trades(json_message):
    date_time = datetime.datetime.fromtimestamp(json_message['E']/1000).strftime('%Y-%m-%d %H:%M:%S')
    print("SYMBOL: "+json_message['s'])
    print("PRICE: "+json_message['p'])
    print("QTY: "+json_message['q'])
    print("TIMESTAMP: " + str(date_time))
    print("-----------------------")

ws_trades()