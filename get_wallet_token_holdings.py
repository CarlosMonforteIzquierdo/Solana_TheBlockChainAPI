from theblockchainapi import SolanaAPIResource, SolanaNetwork,SolanaCurrencyUnit
from decouple import config

API_KEY = config("BLOCKCHAIN_API_KEY")
SECRET_KEY = config("BLOCKCHAIN_API_SECRET")
DEFAULT_UNIT = SolanaCurrencyUnit.SOL
DEFAULT_NETWORK = SolanaNetwork.MAINNET_BETA

BLOCKCHAIN_API_RESOURCE = SolanaAPIResource(
    api_key_id=API_KEY,
    api_secret_key=SECRET_KEY
)
wallet_address ="Eo44seMeJqJ6LtrAvvP5oYMQjvYtBAV1J5s3kzZqeGDz"

def get_token_holdings(wallet_address):
    return BLOCKCHAIN_API_RESOURCE.get_wallet_token_holdings(
        wallet_address,
        include_nfts=False,
        include_zero_balance_holdings=False,
        network=DEFAULT_NETWORK
    )

def main():
    token_holdings = get_token_holdings(wallet_address)
    print(f"Tokens: {token_holdings}")



if __name__ == '__main__':
    main()