from theblockchainapi import SolanaAPIResource, SolanaNetwork,SolanaCurrencyUnit,BlockchainAPIResource,Blockchain,BlockchainNetwork
from decouple import config
import requests

API_KEY = config("BLOCKCHAIN_API_KEY")
SECRET_KEY = config("BLOCKCHAIN_API_SECRET")
COIN_GECKO_API_KEY= config("COIN_GECKO_API_KEY")
DEFAULT_UNIT = SolanaCurrencyUnit.SOL
DEFAULT_NETWORK = SolanaNetwork.MAINNET_BETA

BLOCKCHAIN_API_RESOURCE = SolanaAPIResource(
    api_key_id=API_KEY,
    api_secret_key=SECRET_KEY
)

SOLANA_BLOCKCHAIN_API_RESOURCE = BlockchainAPIResource(
    api_key_id=API_KEY,
    api_secret_key=SECRET_KEY,
    blockchain=Blockchain.SOLANA,
    network=BlockchainNetwork.SolanaNetwork.MAINNET_BETA
)

def get_token_USD_price(token_address):
    url = "https://api.coingecko.com/api/v3/simple/token_price/solana"
    params = {
        "contract_addresses": token_address,
        "vs_currencies": "usd"
    }
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": COIN_GECKO_API_KEY
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Verifica que no haya errores HTTP
        data = response.json()
        token_data = data.get(token_address)
        
        return float(token_data.get("usd", 0.0)) if token_data else 0.0
    except requests.exceptions.RequestException:
        return 0.0

def get_token_name(token_address):
    url = f"https://api.coingecko.com/api/v3/coins/solana/contract/{token_address}"
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": COIN_GECKO_API_KEY
    } 
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Verifica errores HTTP
        data = response.json()
        return data.get("name", "Name not found")  # Devuelve el nombre del token o Name not found
    except requests.exceptions.RequestException:
        return "Name not found"  # Devuelve Name not found en caso de error

def get_token_holdings(wallet_address):
    return BLOCKCHAIN_API_RESOURCE.get_wallet_token_holdings(
        wallet_address,
        include_nfts=False,
        include_zero_balance_holdings=False,
        network=DEFAULT_NETWORK
    )

def main():
    wallet_address ="Eo44seMeJqJ6LtrAvvP5oYMQjvYtBAV1J5s3kzZqeGDz"
    token_holdings = get_token_holdings(wallet_address)
    
    print(f"Tokens held by {wallet_address}:")

    for token in token_holdings:
        mint_address = token.get("mint_address")
        token_name = get_token_name(mint_address)
        ui_amount = token.get("ui_amount", 0)
        amount_in_usd = ui_amount * get_token_USD_price(mint_address)

        print(f"Token: {token_name}")
        print(f"Mint Address: {mint_address}")
        print(f"Amount of tokens: {ui_amount}")
        print(f"Amount (in USD): ${amount_in_usd:.2f}")
        print("\n")
if __name__ == '__main__':
    main()