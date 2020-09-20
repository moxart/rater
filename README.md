# Iranian Rial Exchange Rates
:moneybag: Access IRR exchange rates for 100+ currencies

### Getting Started
The **Exchange API** is a simple **HTTP REST API** for searching and retrieving live **Iranian Rial Exchange Rates** over the web.
This API is great as a data source for access IRR exchange rates for **100+ currencies** and coin prices and other applications where you want to show your users live in near real time.
To get started we're assuming you know how to make web requests in you chosen programming language.

#### Currencies Endpoint
Let's make a request to get live top currencies in the currency route right now. We'll use the `/currency` endpoint for this.

`curl https://raters.ir/exchange/api/currency`

![Raters](https://github.com/moxart/raters/blob/master/currency-usd.png)

This returns a **JSON** object with the all currencies results in an array we can iterate over.
If you want headlines just from a specific source, for example `USD | EUR | AMD | ...` rate, we can do that too.

`curl https://raters.ir/exchange/api/currency/usd`

#### Coins Endpoint

We'll use the `/coin` endpoint for this.

#### Specific Coin Rates

you can have access to the **Single** and **Commercial** coin rates with this endpoints:

`curl https://raters.ir/exchange/api/coin/{single|commercial}`

#### Specific Single & Commercial Rates

`curl https://raters.ir/exchange/api/coin/{single|commercial}/{coin-names}`
