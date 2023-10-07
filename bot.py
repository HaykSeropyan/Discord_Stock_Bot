import discord

import requests

bot_token = "This is where you would put a secret token for the bot"
alpha_vantage_api_key = "this is the secret API Key for alpha vantage"
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)




@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

#This is all the event the bots will respond all are expanitory
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("$active"): #display the most active stocks based on volume
        await message.channel.send(active())

    if message.content.startswith('$losers'): #display the stocks with the largest negative price change
        await message.channel.send(losers())
                                  
    if message.content.startswith('$gainers'): #display the stocks with the largest positive price change
        await message.channel.send(gainers())

    if message.content.startswith('$info'): # display basic stock info(content cut down to reduce the size of the message).Example would be $info goog will display basic info on Google
        ticker = message.content.split(' ')[1]
        await message.channel.send(info(ticker))


    if message.content.startswith('$stock'): # displays the closing end of day price for a stock. Examp would be $stock goog will display the closing price of Google.
        ticker = message.content.split(' ')[1]
        price = get_stock_price(ticker)
        await message.channel.send(f'price of {ticker} is {price}')
#Functions. Eventually will be moved to a seperate file called functions so the code looks cleaner

def get_stock_price(ticker):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=5min&apikey={alpha_vantage_api_key}'
    response = requests.get(url)
    data = response.json()
    try:
        latest_data = data['Time Series (5min)']
        latest_timestamp = next(iter(latest_data))
        latest_price = latest_data[latest_timestamp]['4. close']
        return latest_price
    except KeyError:
        return 'Stock not found or API limit reached'
    
def gainers():
    url = f'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={alpha_vantage_api_key}'
    r = requests.get(url)
    data = r.json()
    message = " "

    for i in range(5):
        ticker = data['top_gainers'][i]['ticker']
        percent_change = data['top_gainers'][i]['change_percentage']
        new_ticker = f"GAINER {i +1 } ticker {ticker} went up {percent_change} today\n"
        message = message + new_ticker

    return message

def losers():
    url = f'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={alpha_vantage_api_key}'
    r = requests.get(url)
    data = r.json()
    message = " "

    for i in range(5):
        ticker = data['top_losers'][i]['ticker']
        percent_change = data['top_gainers'][i]['change_percentage']
        new_ticker = f"LOSERS {i + 1 } ticker {ticker} went down {percent_change} today\n"
        message = message + new_ticker

    return message

def active():
    url = f'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={alpha_vantage_api_key}'
    r = requests.get(url)
    data = r.json()
    message = " "

    for i in range(5):
        ticker = data['most_actively_traded'][i]['ticker']
        percent_change = data['top_gainers'][i]['change_percentage']
        new_ticker= f"ACTIVE {i + 1 } ticker {ticker} changed {percent_change} today\n"
        message = message + new_ticker
    
    return message

def info(ticker):
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={alpha_vantage_api_key}"
    r= requests.get(url)
    data = r.json()
    message = ""

    for items in data:
        if len(data[items]) < 100: #there is a limit to how long a message could be and anything message over 2000 charectors long will not be send and give you an error.
            info = items +' : ' + data[items] +"\n"
            message += info
        else:
             info = items +' : ' + data[items][:100] +"\n"
            message += info
    if message != "":
        return message
    else:
        return f'Can not get info for ticker {ticker}'
        
        
    


client.run(bot_token)
