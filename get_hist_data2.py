import mysql.connector
import time
from binance.client import Client
from strategy import SikStrat
import pandas as pd

# Replace with your Binance API key and secret
API_KEY = 't6dxBytsovc88DlFKHNb6sFmhgK6Pud7mMuNJ16JSLLjr5o8QkJV02FB8qd3iF8f'
API_SECRET = 'St8QBQ3kB8O4Ru3D9yO1aN0mNoeeCRbcyjYEORcF2IimPHyevWpDoZRqQjWPDPkQ'

# Initialize the Binance client
client = Client(API_KEY, API_SECRET)

# Replace with your MySQL database credentials
MYSQL_HOST = 'trading-database.cnwmpftujwax.us-east-2.rds.amazonaws.com'
MYSQL_USER = 'admin'
MYSQL_PASSWORD = 'jerlsonsik123'
MYSQL_DB = 'database1'

# Initialize the MySQL connection
db_connection = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB
)
db_cursor = db_connection.cursor()

database_name = "kline_data"
OPENTIME = 0
OPEN = 1
HIGH = 2
LOW = 3
CLOSE = 4
VOLUME = 5

def create_table():
    db_cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {database_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            symbol VARCHAR(10),
            timestamp BIGINT,
            open DECIMAL(20, 8),
            high DECIMAL(20, 8),
            low DECIMAL(20, 8),
            close DECIMAL(20, 8),
            volume DECIMAL(20, 8)
        )
    ''')
    db_connection.commit()

def insert_data(symbol, kline):
    db_cursor.execute(f'''
        SELECT * FROM {database_name} where timestamp = %s
    ''', (kline[OPENTIME],))

    result = db_cursor.fetchall()

    if not result:
        db_cursor.execute(f'''
            INSERT INTO {database_name} (symbol, timestamp, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (symbol, kline[OPENTIME], kline[OPEN], kline[HIGH], kline[LOW], kline[CLOSE], kline[VOLUME]))
        db_connection.commit()

def fetch_kline_data(symbol, interval, limit):
    klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
    return klines

def update_database(length):
    symbol = "ETHBUSD"       # Replace with the trading pair you want
    interval = Client.KLINE_INTERVAL_5MINUTE
    limit = length              # Number of klines to fetch at a time

    create_table()

    kline_data = fetch_kline_data(symbol, interval, limit)
    
    for kline in kline_data:
        insert_data(symbol, kline)

    print("Database updated.")

def retrieve_last_k_rows(k):
    db_cursor.execute(f'''
        SELECT * FROM kline_data
        ORDER BY timestamp DESC
        LIMIT {k}
    ''')
    rows = db_cursor.fetchall()
    return rows

if __name__ == "__main__":
    window = 60

    # update_database(window)

    while True:
        # update_database(5)
        # time.sleep(60)  # Wait for 1 minute before updating again

        last_k_rows  = retrieve_last_k_rows(window)
        columns = ["ID", "Symbol", "Timestamp", "Open", "High", "Low", "Close", "Volume"]
        df = pd.DataFrame(last_k_rows, columns=columns)
        strategy = SikStrat(df)

        trigger = strategy.trigger()

        if trigger["status"] == "BUY":
            print("BUY")
        elif trigger["status"] == "SELL":
            print("SELL")
        else:
            print("NOTHING")