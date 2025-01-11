import requests

def test_treasury_yield(api_key):
    """
    Fetches 10-Year Treasury Yield data and prints the response.
    """
    url = f"https://financialmodelingprep.com/api/v4/economic?name=10YearTreasuryRate&apikey={api_key}"
    response = requests.get(url)
    print("\n10-Year Treasury Yield Data:")
    print(response.json())

def test_trade_balance(api_key):
    """
    Fetches Trade Balance data and prints the response.
    """
    url = f"https://financialmodelingprep.com/api/v4/economic?name=tradeBalance&apikey={api_key}"
    response = requests.get(url)
    print("\nTrade Balance Data:")
    print(response.json())

if __name__ == "__main__":
    # Replace YOUR_API_KEY with your actual API key or set it in your environment variables
    api_key = "RhFpZvxEyxCKXCFUYGD8u8mrCnpiBxtx"

    # Test each API endpoint
    test_treasury_yield(api_key)
    test_trade_balance(api_key)
