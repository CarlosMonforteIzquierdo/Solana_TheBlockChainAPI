from theblockchainapi import SolanaAPIResource, SolanaNetwork, SolanaCurrencyUnit
from decouple import config

API_KEY = config("BLOCKCHAIN_API_KEY")
SECRET_KEY = config("BLOCKCHAIN_API_SECRET")

#Declare token we want to get balance of(in this case SOL) and the network solana
DEFAULT_UNIT = SolanaCurrencyUnit.SOL
DEFAULT_NETWORK = SolanaNetwork.MAINNET_BETA

BLOCKCHAIN_API_RESOURCE = SolanaAPIResource(
    api_key_id=API_KEY,
    api_secret_key=SECRET_KEY
)

def get_solana_balance(wallet_address):
    return BLOCKCHAIN_API_RESOURCE.get_balance(
        public_key=wallet_address,
        unit=DEFAULT_UNIT,
        network=DEFAULT_NETWORK
    )

def main():
    wallet_address = "Eo44seMeJqJ6LtrAvvP5oYMQjvYtBAV1J5s3kzZqeGDz"
    result= get_solana_balance(wallet_address)
    print("-" * 20)
    print(f"SOL Balance of {wallet_address}")
    print(result)
    print("-" * 20)

if __name__== '__main__':
    main()