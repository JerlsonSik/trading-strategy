## trading-strategy

## Project Overview:
I am a part time trader who loves trading a lot. However, I knew deeply that human trading without the support of data and algorithms is more likely to fail. So, I developed this trading strategy with python that could trade automatically by the strategy that I have developed myself. 

There are 3 parts of the project. 
- First part: Drawing data from Binance API (Cryptocurrency broker) , modified and save it into a csv file.
- Second part: Developed multiple profit strategy with back testing library by using the historical data prepared before.
- Third part: Connected with Binance API and automated the developed trading strategy to AWS server and MySQL to run 24/7 and place data when signal triggered.

## Features:
- Connecting with Binance API and draw all historical data into a csv file.
- Using Backtesting library to generate testing result 
- Improved trading result by implementing technical trading knowledge into the strategy model 
- Connected with Binance API again to place order when signal triggered
- Connected to AWS server and MySQL to get real-time data and run the script 24/7 without missing any possible profitable trade

## What I learned:
- **Programming Skills**: Python skills such as NumPy, Pandas, Backtesting, API. Being able to realize my trading idea and knowledge into code.
- **Data Analysis: Analysis**: strategy result after back testing and improve the result by testing out more technical combination of indicators
- **AWS**: Deploy my strategy to cloud server to run automatically 
- **Database**: Read data from broker and save data into MySQL database
