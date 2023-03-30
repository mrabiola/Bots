import aiohttp, requests, json, asyncio
import nest_asyncio
nest_asyncio.apply()

def fetch_market_data():
    url ='https://ftx.com/api/markets'
    resp = requests.get(url).text
    result = json.loads(resp)
    if result['success']:
        data = {}
        for r in result['result']:
            name = r['name']
            data[name] = {}
            for k in r.keys():
                data [name] [k] = r[k]
        return data
    else:
        print('failed to retrieve market data...')

async def fetch_market_data_async():
    url = 'https://ftx.com/api/markets'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            resp = await response. text()
            result = json.loads(resp)
            if result['success']:
                data = {}
                for r in result['result']:
                    name = r['name']
                    data [name] = {}
                    for k in r.keys ():
                        data[name] [k] = r[k]

                        await asyncio.sleep (0)
                        return data
                    else:
                        print('failed to retrieve market data...')
##Run Cell Run Above | Debug Cell | Go to [13]

if __name__ == '__main__':
    data = fetch_market_data()
    print(
        'non-async, 24h change for BTC-PERP: ',
        data['BTC-PERP']['change24h']
        )

    try: loop = asyncio.get_running_loop().run_until_complete(fetch_market_data_async())
    except: loop = asyncio.get_event_loop().run_until_complete(fetch_market_data_async())

    data = loop
    print(
        'async, 24h change for BTC-PERP: ',
        data['BTC-PERP']['change24h']
        )
