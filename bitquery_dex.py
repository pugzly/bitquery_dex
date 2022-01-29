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


# change TOKEN contract address and name:
token_name = "CAKE"
token_list = {"TOKEN": "0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82",
              "BUSD": "0xe9e7cea3dedca5984780bafc599bd69add087d56",
              "WBNB": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"}



query = """
 query getData($base0: String, $base1: String, $quote0: String){
  ethereum(network: bsc) {
    tokenPrice: dexTrades(
      baseCurrency: {is: $base0}
      quoteCurrency: {is: $quote0}
    ) {
      quotePrice
    }
    busdPrice: dexTrades(
      baseCurrency: {is: $base1}
      quoteCurrency: {is: $quote0}
    ) {
      quotePrice
    }
  }
}
"""
params = {
  "base0"  : token_list["TOKEN"],
  "base1"  : token_list["BUSD"],
  "quote0" : token_list["WBNB"]
}

json     = {"query"     : query, "variables": params}
headers  = {"X-API-KEY" : API_KEY}

while True:
  response = requests.post(BASE_URL, json = json, headers = headers)
  if response.status_code == 200:
    jsonResp = response.json()
    tokenBNBprice = jsonResp['data']['ethereum']['tokenPrice'][0]['quotePrice']
    busdBNBprice = jsonResp['data']['ethereum']['busdPrice'][0]['quotePrice']
    tokenBUSDprice = float(tokenBNBprice) / float(busdBNBprice)

    timeNow = datetime.datetime.now()
    timeStampStr = timeNow.strftime("[%d-%b-%Y %H:%M:%S]")
    print(timeStampStr+" $"+token_name+" price in WBNB: "+"{:.12f}".format(tokenBNBprice)+";  $"+token_name+" price in BUSD: "+"{:.12f}".format(tokenBUSDprice))

  else:
    error = (f"Query failed and return code is {response.status_code}. {query}")
    raise Exception(error)

  # wait 10 seconds to save API calls
  time.sleep(10)
