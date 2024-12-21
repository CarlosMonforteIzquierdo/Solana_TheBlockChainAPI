from theblockchainapi import SolanaAPIResource, SolanaNetwork,SolanaCurrencyUnit,BlockchainAPIResource,Blockchain,BlockchainNetwork
from decouple import config

API_KEY = config("BLOCKCHAIN_API_KEY")
SECRET_KEY = config("BLOCKCHAIN_API_SECRET")
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

def get_token_holdings(wallet_address):
    return BLOCKCHAIN_API_RESOURCE.get_wallet_token_holdings(
        wallet_address,
        include_nfts=False,
        include_zero_balance_holdings=False,
        network=DEFAULT_NETWORK
    )

def get_token_name(mint_address):
    token_info = BLOCKCHAIN_API_RESOURCE.get_token_metadata(
        mint_address=mint_address,
        network=DEFAULT_NETWORK
    )
    return token_info.get("name", "Unknown Token")

def main():
    wallet_address ="Eo44seMeJqJ6LtrAvvP5oYMQjvYtBAV1J5s3kzZqeGDz"
    token_holdings = get_token_holdings(wallet_address)
    
    for token in token_holdings:
        mint_address = token["mint_address"]
        ui_amount = token["ui_amount"]
        token_name = get_token_name(mint_address)
        #Falta conectar con API de CoinGecko para obtener el precio en USD
        price_in_USD = 1.0
        amount_in_usd = ui_amount * price_in_USD

        print(f"Token Name: {token_name}")
        print(f"Mint Address: {mint_address}")
        print(f"UI Amount: {ui_amount}")
        print(f"Amount (in USD): ${amount_in_usd:.2f}")



if __name__ == '__main__':
    main()