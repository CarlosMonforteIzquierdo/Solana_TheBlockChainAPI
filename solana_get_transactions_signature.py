#Shows in descending order by date the transactions signature given a wallet address
from theblockchainapi import SolanaAPIResource, SolanaNetwork
from decouple import config
import json

API_KEY = config("BLOCKCHAIN_API_KEY")
SECRET_KEY = config("BLOCKCHAIN_API_SECRET")

BLOCKCHAIN_API_RESOURCE = SolanaAPIResource(
        api_key_id=API_KEY,
        api_secret_key=SECRET_KEY
    )

def main():
    wallet_address = "Eo44seMeJqJ6LtrAvvP5oYMQjvYtBAV1J5s3kzZqeGDz"
    print(f"Transactions for {wallet_address}")
    transactions = BLOCKCHAIN_API_RESOURCE.get_wallet_transactions(
        wallet_address,
        network=SolanaNetwork.MAINNET_BETA
    )

    for transaction in transactions:
        print(f"Transaction Signature: {transaction}")


if __name__ == '__main__':
    main()