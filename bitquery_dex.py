"""
     Simple and minimal Python script to get Binance Smart Chain (BSC) token price expressed in BUSD, 
     using only data from dex liquidity pools, with the help of Bitquery API.

     To get Bitquery API key register as "Developer" at https://bitquery.io/
     FREE plan limits:
     Up to 100k monthly API calls
     Up to 10 API calls per minute.
     (As of 2022/01/26)
"""
import time, requests, json, datetime


API_KEY = "YOUR___API___KEY___HERE"
BASE_URL = "https://graphql.bitquery.io/"


token_list = {"CAKE": "0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82",
              "BUSD": "0xe9e7cea3dedca5984780bafc599bd69add087d56",
              "WBNB": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"}

# "token_list" is not used and is here only for reference.
# To receive price data for different token edit baseCurrency contract address in the "query" bellow

query = """
{
  ethereum(network: bsc) {
    cakePrice: dexTrades(
      baseCurrency: {is: "0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82"}
      quoteCurrency: {is: "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"}
    ) {
      quotePrice
    }
    busdPrice: dexTrades(
      baseCurrency: {is: "0xe9e7cea3dedca5984780bafc599bd69add087d56"}
      quoteCurrency: {is: "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"}
    ) {
      quotePrice
    }
  }
}
"""

json     = {"query"     : query}
headers  = {"X-API-KEY" : API_KEY}

while True:
  response = requests.post(BASE_URL, json = json, headers = headers)
  if response.status_code == 200:
    jsonResp = response.json()
    cakeBNBprice = jsonResp['data']['ethereum']['cakePrice'][0]['quotePrice']
    busdBNBprice = jsonResp['data']['ethereum']['busdPrice'][0]['quotePrice']
    cakeBUSDprice = float(cakeBNBprice) / float(busdBNBprice)

    timeNow = datetime.datetime.now()
    timeStampStr = timeNow.strftime("[%d-%b-%Y %H:%M:%S]")
    print(timeStampStr," $CAKE price in WBNB: ", "{:.12f}".format(cakeBNBprice), ";  $CAKE price in BUSD: ", "{:.12f}".format(cakeBUSDprice))

  else:
    error = (f"Query failed and return code is {response.status_code}. {query}")
    raise Exception(error)

  # wait 10 seconds to save API calls
  time.sleep(10)



