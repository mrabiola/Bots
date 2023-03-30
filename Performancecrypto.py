import asyncio
import aiohttp
from datetime import datetime, timedelta
from tabulate import tabulate
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

def get_filtered_coins(min_marketcap, max_marketcap):
    coins = cg.get_coins_markets(vs_currency="usd")
    filtered_coins = [
        coin for coin in coins
        if min_marketcap <= coin["market_cap"] <= max_marketcap
        and not (-0.5 <= coin.get("price_change_percentage_24h", 0) <= 0.5)
    ]
    return filtered_coins

async def fetch_historical_prices(coin_id, days, session):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days={days}&interval=daily"
    async with session.get(url) as response:
        historical_data = await response.json()
        if "prices" in historical_data:
            return {datetime.fromtimestamp(price[0] / 1000).date(): price[1] for price in historical_data["prices"]}
        else:
            return {}

async def get_historical_prices_async(coin_id, days):
    async with aiohttp.ClientSession() as session:
        return await fetch_historical_prices(coin_id, days, session)

def get_performance_data(coin, historical_prices):
    today = datetime.now().date()
    old_dates = [today - timedelta(days=n) for n in [3, 7, 14]]
    old_prices = [historical_prices.get(date, None) for date in old_dates]
    price_changes = [((coin["current_price"] - p) / p) * 100 if p is not None else 0 for p in old_prices]

    return [
        coin["symbol"],
        coin["current_price"],
        coin["market_cap"] / 1_000_000,
        coin["total_volume"] / 1_000_000,
        coin.get("price_change_percentage_24h", 0),
        *price_changes
    ]

async def main():
    min_marketcap = 250_000_000
    max_marketcap = 500_000_000
    filtered_coins = get_filtered_coins(min_marketcap, max_marketcap)

    data = []
    for coin in filtered_coins:
        historical_prices = await get_historical_prices_async(coin["id"], 15)
        performance_data = get_performance_data(coin, historical_prices)
        data.append(performance_data)

    headers = [
        'Symbol',
        'Price',
        'Market Cap (M)',
        'Volume (M)',
        '1-Day Change (%)',
        '3-Day Change (%)',
        '7-Day Change (%)',
        '14-Day Change (%)'
    ]

    sorted_data = sorted(data, key=lambda x: x[7], reverse=True)  # Sort based on 14-Day Change (%)
    top_10_data = sorted_data[:10]  # Slice the first 10 elements

    print(tabulate(top_10_data, headers=headers))

if __name__ == "__main__":
    asyncio.run(main())
