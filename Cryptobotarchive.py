import discord
import os
#import http.server
#import socketserver
#import threading
import time
import asyncio
#import requests
#from replit import db
#from dotenv import load_dotenv
from discord import Intents
from flask import Flask
from threading import Thread
from pycoingecko import CoinGeckoAPI
from prettytable import PrettyTable

'''load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_TOKEN')'''

TOKEN = 'MTA4Nzc5OTIyNDcxMzg3MTQ4Mg.GwReTG.WnNnkD6vUwVulHk6QeHyCfXsstjGFm_wPvoa1o'
CHANNEL_ID = 1087800495470555146  # Replace with your channel ID as an integer

intents = Intents.default()
intents.messages = True
intents.reactions = True
intents.typing = False

client = discord.Client(intents=intents)
#client = discord.Client()
app = Flask(__name__)

@app.route('/')
def home():
    return 'CryptoBot is running!'

def run_flask_app():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

#def start_http_server(port):
    #handler = http.server.SimpleHTTPRequestHandler
    #httpd = socketserver.TCPServer(("", port), handler)
    #print(f"Serving on port {port}")
    #httpd.serve_forever()

def get_top_20_cryptocurrencies():
    cg = CoinGeckoAPI()
    top_20 = cg.get_coins_markets(vs_currency='usd', order='volume_desc', per_page=20)

    return top_20

def display_table(cryptocurrencies):
    table = PrettyTable()

    table.field_names = ["Rank", "Name", "Symbol", "Price (USD)", "Volume (24h)", "Market Cap"]

    for i, crypto in enumerate(cryptocurrencies, start=1):
        table.add_row([
            i,
            crypto['name'],
            crypto['symbol'].upper(),
            f"${crypto['current_price']:.2f}",
            f"${crypto['total_volume']:.2f}",
            f"${crypto['market_cap']:.2f}"
        ])

    return f"```\n{table}\n```"

async def send_crypto_data():
    while True:
        channel = client.get_channel(CHANNEL_ID)
        if channel:
            top_20_cryptocurrencies = get_top_20_cryptocurrencies()
            table = display_table(top_20_cryptocurrencies)

            # Split the table into smaller parts if it exceeds the character limit
            table_parts = [table[i:i + 1990] for i in range(0, len(table), 1990)]

            for part in table_parts:
                # Add markdown for the code block to each part
                content = f"```\n{part}\n```"
                await channel.send(content)

            await asyncio.sleep(3600)  # Wait for 1 hour (3600 seconds) before sending again
        else:
            print(f"Channel with ID {CHANNEL_ID} not found.")
            break

@client.event
async def on_ready():
    #port = int(os.environ.get("PORT", 8080))
    #threading.Thread(target=start_http_server, args=(port,)).start()
    print(f'{client.user} has connected to Discord!')
    thread = Thread(target=run_flask_app)
    thread.start()
    await send_crypto_data()

client.run(TOKEN)
